import datetime
from flask import Flask, jsonify, request, session
from pymongo import MongoClient, ReturnDocument
import json
from PIL import Image
from imageGen import ImageGen
from imageEdit import ImageEdit
from queue import Queue
import threading
import uuid
import jwt
from bson import json_util
from bson.objectid import ObjectId

import base64
from captionGen import captionGen
# from PIL import Image #uncomment if u want to see images pop up

from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash


import os

# task_queue = Queue()
# tasks_done = [];
# def process_queue():
#     while True:
#         task = task_queue.get()
#         if task is None:
#             break
#         try:
#             task()
#         except Exception as e:
#             print(f"Error processing task: {e}")
#         finally:
#             task_queue.task_done()

# thread = threading.Thread(target=process_queue)
# thread.start()

# def add_task_to_queue(task):
#     task_queue.put(task)


# Connect to MongoDB
client = MongoClient('mongodb+srv://imagegen:KF7pSnJVxSZIfyIU@imagegen.jz2d0rr.mongodb.net/?retryWrites=true&w=majority&appName=ImageGen')
db = client['ImageGen']
users_collection = db['users']
images_collection = db['images']


UPLOAD_FOLDER = 'uploads'
GENERATED_FOLDER = 'generated';


app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['GENERATED_FOLDER'] = GENERATED_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#Used to debug the server and determine wether it is running
@app.route("/")
def hello_world():
    print("Hit")
    return "Connection Established"

#This function is used to determine if the user is logged in and authinticated
@app.route('/get_user_info', methods=['GET','POST'])
def get_user_info():
  token = request.headers.get('Authorization') #Get the token from the request headers
  print("Token: " + str(token))
  if not token:#If the token is not present return an error
    return jsonify({'error': 'Unauthorized No Token'}), 401

  try:#Try to decode the token and get the user information from the token
    token = token.split()[1]  # Remove 'Bearer' from the token
    payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    username = payload['username']
    
    user = users_collection.find_one({'username': username}) #Get the user from the database
    if user: #If the user is found return the user information
      return jsonify({'username': user['username'], 'email': user.get('email', '')}), 200
    else: #If the user is not found return an error
      return jsonify({'error': 'User not found'}), 404

  except jwt.ExpiredSignatureError: #If the token is expired return an error
    return jsonify({'error': 'Token expired'}), 401
  except jwt.InvalidTokenError: #If the token is invalid return an error
    return jsonify({'error': 'Invalid token'}), 401
    

#This function is used to get a user private images from the database
@app.route('/getArchivedImages', methods=['GET','POST'])
def get_Archived_Images():
  token = request.headers.get('Authorization') #Get the token from the request headers
  print("Token: " + str(token))
  if not token: #If the token is not present return an error
    return jsonify({'error': 'Unauthorized No Token'}), 401

  try:
    token = token.split()[1]  # Remove 'Bearer' from the token
    payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256']) #Decode the token and get the user information from the token
    username = payload['username']
    
    images_data = list(images_collection.find({'username': username}))  # attempts to find all images with the user's username
    # Convert ObjectId to strings for each document
    for image in images_data: #Convert the object id to a string so it can be jsonified without errors
        image['_id'] = str(image['_id'])

    if images_data: #If the user is found return all the images it found to the user
      return jsonify({'message': 'Got Public Images', 'images': images_data}), 200
    else: #If the user is not found return an error
      return jsonify({'error': 'User not found'}), 404

  except jwt.ExpiredSignatureError: #If the token is expired return an error
    return jsonify({'error': 'Token expired'}), 401
  except jwt.InvalidTokenError: #If the token is invalid return an error
    return jsonify({'error': 'Invalid token'}), 401

#This function is used to turn sepecific images publc or private
@app.route('/toggleImagePrivacy/<image_id>', methods=['PUT'])
def toggleImagePrivacy(image_id): #Get the image id from the url (from POST request)
  token = request.headers.get('Authorization') #Get the token from the request headers
  print("Token: " + str(token))
  if not token: #If the token is not present return an error
    return jsonify({'error': 'Unauthorized No Token'}), 401

  try:
    print("Beginning to toggle image privacy")
    token = token.split()[1]  # Remove 'Bearer' from the token
    payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    username = payload['username'] # Extract the current user's username from JWT token
    # Extract the current user's username from JWT token

    print("Current User: " + str(username))
    # Check if the image exists in MongoDB
    image = images_collection.find_one({"_id": ObjectId(image_id)})
    if not image:
        return jsonify({"error": "Image not found"}), 404
    
    data = request.get_json()
    is_public = data.get('isPublic') # Get the isPublic value from the request body
    # Update the privacy status of the image in MongoDB
    update_query = {"$set": {"public": is_public}} # Set the 'public' field to the value of isPublic
    if 'public' not in image:  # If the 'public' field doesn't exist, add it
        update_query = {"$set": {"public": is_public}}
    updated_image = images_collection.find_one_and_update( #Update the image in the database
            {"_id": ObjectId(image_id)},
            update_query,
            return_document=ReturnDocument.AFTER
    )
    # Return a success message with the updated privacy status
    return jsonify({"message": f"Privacy status of image {image_id} updated successfully","public": is_public}), 200

  except jwt.ExpiredSignatureError: #If the token is expired return an error
    return jsonify({'error': 'Token expired'}), 401 # Return an error if the token is expired
  except jwt.InvalidTokenError: #If the token is invalid return an error
    return jsonify({'error': 'Invalid token'}), 401 # Return an error if the token is invalid
  
@app.route("/getImages",  methods=['GET'])
def getImages():
    limit = 100  # Set your desired limit here
    images_data = list(images_collection.find({"public":True}).limit(limit))  # Fetch documents with the specified limit
    
    # Convert ObjectId to strings for each document
    for image in images_data:
        image['_id'] = str(image['_id'])
    
    return jsonify({'message': 'Got Public Images', 'images': images_data}),200

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        hashed_password = generate_password_hash(password)
        
        if users_collection.find_one({'username': username}):
            res = {'response': 'Username already exists!'}
            return jsonify(res), 400

        else:
            users_collection.insert_one({'username': username, 'password': hashed_password, 'email': email})
            # Set the user's username in the session
            # session['username'] = username
            payload = {
                'username': username,
                # Other data if needed (user_id, roles, etc.)
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30) # Expiration
            }
            token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
            res = {'response': 'Signed Up Successful','token': token}
            return jsonify(res), 200
    
    res = {'response': 'Wrong method'}
    return jsonify(res), 405

@app.route('/signout', methods=['POST'])
def signout():
    if request.method == 'POST':
        # Remove user from session
        session.pop('user', None)
        res = {'response': 'Signed Out Successful'}
        return jsonify(res)
    else:
        res = {'response': 'Wrong method'}
        return jsonify(res)
    
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        user = users_collection.find_one({'username': username})

        if user and check_password_hash(user['password'], password):
            payload = {
                'username': username,
                # Other data if needed (user_id, roles, etc.)
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30) # Expiration
            }
            token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

            res = {'response': 'Login Successful', 'token': token}
            return jsonify(res), 200
        else:
            res = {'response': 'Invalid username or password'}
            return jsonify(res), 401


    
@app.route("/imageTotext", methods=['post'])
def imageToText():
    try:
        try: 
          imagecaption = request.form.get('caption');
          print("Caption to use: " + str(imagecaption));
        except Exception as e:
          print("Unable to determine caption");
        
        uploaded_files = request.files.getlist('file') 
        caption = captionGen()
        for file in uploaded_files:
          print("Saving File Name: "+file.filename);
          file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename));
          # pil_img = Image.open(file); #uncommet to see images pop up
          # pil_img.show();
          secure_filename(file.filename);
          pathurl = os.path.join(app.config['UPLOAD_FOLDER'],file.filename);
          print(pathurl)
          captionGenerated = caption.predict(pathurl)


        res = {'message': 'File uploaded successfully',"caption":captionGenerated}
        res_message = jsonify(res);
        return res_message;

    except Exception as e:
        print(str(e));
        return jsonify({'error': str(e)}), 500
    

@app.route("/generateLLM", methods=['post'])
def generateLLM():
    try:
        try: 
          captionGenerated = request.form.get('captionGenerated');
          tone = request.form.get('tone');
          print("Generated from BLIP and being passed to LLM: " + str(captionGenerated));
          print("With Tone:" + str(tone));
        except Exception as e:
          print("Unable to determine caption");
        
        
        caption = captionGen()
        funnycaption = caption.createCaption(captionGenerated, tone);
        ##image.save("/.")
        res = {'message': 'File uploaded successfully',"result":funnycaption}
        res_message = jsonify(res);
        return res_message;

    except Exception as e:
        print(str(e));
        return jsonify({'error': str(e)}), 500
    
@app.route("/generate", methods=['post'])
def generate_image():
    try:
        prompt = request.form.get('prompt');
        model = request.form.get('model');
        guidance = request.form.get('guidance');
        inferenceSteps = request.form.get('inferenceSteps');
  #  formData.append('guidance', guidance);
  #         formData.append('inferenceSteps', inferenceSteps);
        print("Recieved prompt: " + prompt)
        generator = ImageGen();
        # image = generator.generate(prompt);
        images = []
        if model == 'runwayml/stable-diffusion-v1-5':
          images.append({'image_data': generator.generate(prompt=prompt,guidance=guidance,inferenceSteps=inferenceSteps)});
        else: 
          images.append({'image_data': generator.generateDetailed(prompt=prompt,guidance=guidance,inferenceSteps=inferenceSteps)});
        
        return jsonify({'message': 'File uploaded successfully','prompt':prompt,'images':images});
        
    except Exception as e:
        print(str(e));
        return jsonify({'error': str(e)}), 500

@app.route("/editImage", methods=['post'])
def edit_image():
    try:  
        uploaded_files = request.files.getlist('file') 
        for file in uploaded_files:
          print("Saving File Name: "+file.filename);
          file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename));
          secure_filename(file.filename);
          pathurl = os.path.join(app.config['UPLOAD_FOLDER'],file.filename);

        prompt = request.form.get('prompt');
        print("Recieved prompt: " + prompt)
        editImageGenerate = ImageEdit();
        # def generate(self, img, prompt="Didn't work sorry"):
           
        # image = generator.generate(prompt);
        images = []
        for i in range(1):
          images.append({'image_data': editImageGenerate.generate(pathurl, prompt)});
        
        return jsonify({'message': 'File uploaded successfully','prompt':prompt,'images':images});

    except Exception as e:
        print(str(e));
        return jsonify({'error': str(e)}), 500
  
if __name__ == '__main__':
   app.run(port=5000, debug=True, threaded=True)







    
