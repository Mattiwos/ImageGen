from PIL import Image
import requests
import torch
from torchvision import transforms
from torchvision.transforms.functional import InterpolationMode


   

class captionGen:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def load_demo_image(self,image_size,device,imageurl):
        #replace with url we can use s3
        raw_image = Image.open(imageurl).convert('RGB')   

        w,h = raw_image.size
        # Image.open(raw_image.resize((w//5,h//5)))
        
        transform = transforms.Compose([
            transforms.Resize((image_size,image_size),interpolation=InterpolationMode.BICUBIC),
            transforms.ToTensor(),
            transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711))
            ]) 
        image = transform(raw_image).unsqueeze(0).to(device)   
        return image
    #change to imagepath
    def predict(self, imageurl):
        from models.blip import blip_decoder

        image_size = 384
        image = self.load_demo_image(image_size=image_size, device=self.device,imageurl=imageurl)

        model_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_base_capfilt_large.pth'
            
        model = blip_decoder(pretrained=model_url, image_size=image_size, vit='base')
        model.eval()
        model = model.to(self.device)

        with torch.no_grad():
            # beam search
            caption = model.generate(image, sample=False, num_beams=3, max_length=20, min_length=5) 
            # nucleus sampling
            # caption = model.generate(image, sample=True, top_p=0.9, max_length=20, min_length=5) 
            print('caption: '+caption[0])
            return caption[0]