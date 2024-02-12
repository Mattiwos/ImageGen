from diffusers import StableDiffusionPipeline  # latest version transformers (clips)
import torch
import base64
from PIL import Image

class ImageGen:
    def __init__(self):
        self.model_id = "runwayml/stable-diffusion-v1-5"
        self.pipe = StableDiffusionPipeline.from_pretrained(self.model_id, torch_dtype=torch.float16, safety_checker=None)
        self.pipe.enable_model_cpu_offload()

    def generate(self, prompt="horse space walk"):
        try:
            image = self.pipe(prompt).images[0]  
            image = image.convert('RGB')

            # Convert the image to a byte array
            image_byte_array = image.tobytes()

            # Encode the byte array to base64
            base64_encoded_image = base64.b64encode(image_byte_array)

            # Convert the base64 bytes to a string
            base64_encoded_image_string = base64_encoded_image.decode('utf-8')

            # Format the base64 string as a data URL for HTML
            data_url = f"data:image/jpeg;base64,{base64_encoded_image_string}"
            return data_url

        except Exception as e:
            print(f"An error occurred: {e}")
            return None


if __name__ == '__main__':
    prompt = "horse space walk"
    gen = ImageGen()
    generated_image_url = gen.generate(prompt)
    if generated_image_url:
        print("Generated image URL:", generated_image_url)
    else:
        print("Failed to generate the image.")
