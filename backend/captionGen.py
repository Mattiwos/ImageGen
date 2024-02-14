import requests
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration, AutoModelForCausalLM, AutoTokenizer

# Check if CUDA (GPU support) is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class captionGen:
    def __init__(self):
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to(device)

    def predict(self, imageurl):
        raw_image = Image.open(imageurl).convert('RGB')
        text = "a photo of"
        inputs = self.processor(raw_image, text, return_tensors="pt").to(device)

        out = self.model.generate(**inputs)
        return self.processor.decode(out[0], skip_special_tokens=True)

    def makeFunny(self, caption):
        print("Using device: " + str(device))
        tokenizer = AutoTokenizer.from_pretrained("HuggingFaceH4/zephyr-7b-beta")
        model = AutoModelForCausalLM.from_pretrained("HuggingFaceH4/zephyr-7b-beta", torch_dtype=torch.float16).to(device)
        text = "What is a short witty and funny instagram caption for an image of, " + caption + "  and make sure not to add extra information:"
        input_ids = tokenizer.encode(text, return_tensors="pt").to(device)

        output = model.generate(
            input_ids,
            max_length=140,  # Increase or decrease this value for longer or shorter captions
            num_return_sequences=1,  # Generate multiple sequences for diversity
            temperature=0.9,  # Adjust the temperature for more diverse outputs
            top_k=50,  # Adjust the top_k parameter for diversity
            top_p=0.95,  # Adjust the top_p parameter for diversity
            repetition_penalty=2.0,  # Penalize repetition for more diverse outputs
            do_sample=True  # Sample from the distribution instead of greedy decoding
        )

        generated_joke = tokenizer.decode(output[0], skip_special_tokens=True)
        return generated_joke.replace(text, '')

if __name__ == '__main__':
   location = "/Users/mattiwosbelachew/Repos/github.com/CSE115A/ImageModels/backend/uploads/wildcamping.jpg"
   gen = captionGen()
   caption = gen.predict(location)
   print("Predicted caption:", caption)
   funnycaption = gen.makeFunny(caption)
   print("Funny caption:", funnycaption)
