from diffusers import StableDiffusionImg2ImgPipeline #latest version tranformers (clips)
from diffusers import AutoPipelineForImage2Image
import torch
from PIL import Image
import base64
import io
#import xformers

torch.cuda.empty_cache() #empty vram

class ImageEdit:
    def __init__(self):
        self.model_id = "runwayml/stable-diffusion-v1-5"
        self.detailed_model_id = "stabilityai/stable-diffusion-xl-base-1.0"
        #editImageGenerate = ImageEdit(AutoPipelineForImage2Image,"runwayml/stable-diffusion-v1-5");

    def preprocess(self, img):
        try:
            file = open(img, "rb")
            og_image = Image.open(file).convert("RGB")
            og_image = og_image.resize((768, 512))
            return og_image
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def generate(self, img, prompt="Didn't work sorry", strengthImg=0.8, guidance_scaleImg=7.5, stepsImg=50, negativeImg="", num_images=1):
        #self.pipe = StableDiffusionImg2ImgPipeline.from_pretrained(self.model_id_base, torch_dtype=torch.float16, safety_checker=None)
        model_input_img = self.preprocess(img)
        self.pipe = AutoPipelineForImage2Image.from_pretrained(self.model_id, torch_dtype=torch.float16, variant="fp16",use_safetensors=True)
        self.pipe = self.pipe.to("cuda")
        self.pipe.enable_model_cpu_offload()
        #self.pipe.enable_xformers_memory_efficient_attention()
        images = self.pipe(prompt=prompt, image=model_input_img,
                strength=strengthImg,
                guidance_scale=guidance_scaleImg,
                num_inference_steps=stepsImg,
                negative_prompt=negativeImg,
                num_images_per_prompt=num_images
            ).images
        #images[0].save("uploads/modified.jpg")
        return self.covertToimgageJpeg(images[0]);

    def generateDetailed(self, img, prompt="Didn't work sorry", strengthImg=0.8, guidance_scaleImg=7.5, stepsImg=50, negativeImg="", num_images=1):
        #self.pipe = StableDiffusionImg2ImgPipeline.from_pretrained(self.model_id_base, torch_dtype=torch.float16, safety_checker=None)
        model_input_img = self.preprocess(img)
        self.pipe = AutoPipelineForImage2Image.from_pretrained(self.model_id_detailed, torch_dtype=torch.float16, variant="fp16",use_safetensors=True)
        self.pipe = self.pipe.to("cuda")
        self.pipe.enable_model_cpu_offload()
        #self.pipe.enable_xformers_memory_efficient_attention()
        images = self.pipe(prompt=prompt, image=model_input_img,
                strength=strengthImg,
                guidance_scale=guidance_scaleImg,
                num_inference_steps=stepsImg,
                negative_prompt=negativeImg,
                num_images_per_prompt=num_images
            ).images
        #images[0].save("uploads/modified.jpg")
        return self.covertToimgageJpeg(images[0]);

    def covertToimgageJpeg(self, image):
        image = image.convert('RGB')
                        # Convert the image to a byte array
        with io.BytesIO() as buffer:
            image.save(buffer, format="JPEG")
            image_byte_array = buffer.getvalue()

            # Convert the image to a byte array
            # image_byte_array = image.tobytes()

            # Encode the byte array to base64
        base64_encoded_image = base64.b64encode(image_byte_array)

            # Convert the base64 bytes to a string
        base64_encoded_image_string = base64_encoded_image.decode('utf-8')

            # Format the base64 string as a data URL for HTML
        data_url = f"data:image/jpeg;base64,{base64_encoded_image_string}"
        return data_url