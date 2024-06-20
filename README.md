# ImageGen

Google Slide to explain the project:
[Google Slide Link](https://docs.google.com/presentation/d/1j9p2AJRoSKvfFMJctIMrCz8k4yI_4En-MglBUonv0_s/edit?usp=sharing)

## How to Run the Frontend

Navigate to the `frontend` directory and install dependencies, then start the development server:

```bash
cd frontend
npm install
npm start
```

Open [http://localhost:3000/](http://localhost:3000/) in your browser to access the webpage.

## How to Run the Backend

Navigate to the `backend` directory, install Python dependencies, and start the backend server:

```bash
cd backend
python -m pip install -r requirements.txt
python main.py
```

This will create a backend REST API running on port 5000, which is used to interact with the upload page in the React frontend.

## Testing Upload and Responses

Visit [http://localhost:3000/ImageGen](http://localhost:3000/ImageGen):
- Click and select a file, then click upload.
- Make sure to have the console open to see logs of requests sent and responses.
- The files should be uploaded to the backend's `uploads` folder. Ensure that data is being received correctly.

## Utilizing Machine Learning and Backend

You can add your machine learning models to the backend and test your functionality. Replace responses with altered images or other relevant data. The Models used were Stable Diffusion and BLIP models. These models were researched and sourced from HuggingFace

## API Documentation

You can find the documentation for the backend APIs in the [docs/API.md](docs/API.md) file.

## Side Note

This project utilizes a basic frontend boilerplate based on Facebook's Create React App. You can find more information about it [here](https://github.com/facebook/create-react-app).
