import os
import random
import csv
from datetime import datetime
import requests
from openai import OpenAI

# Initialize OpenAI Client using GitHub Secret
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("CRITICAL: OPENAI_API_KEY is missing from GitHub Secrets!")

client = OpenAI(api_key=api_key)

TOTAL_IMAGES = 5  # Keep at 5 for quick testing
AGES = ["2-3 years", "3-4 years", "4-5 years", "5-6 years", "6-7 years"]
GENDERS = ["boy", "girl"]
SHIRT_COLORS = ["Crisp White", "Pastel Blue", "Mint Green", "Soft Yellow", "Beige"]
SLEEVE_COLORS = ["Contrasting Blue", "Matching Linen", "Dark Grey", "Beige"]

def run_daily_automation():
    today_str = datetime.now().strftime('%Y-%m-%d')
    output_dir = f"./output_{today_str}"
    os.makedirs(output_dir, exist_ok=True)
    
    csv_file_path = os.path.join(output_dir, f"catalog_{today_str}.csv")
    
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ["Image Name", "Age Group", "Gender", "Shirt Color", "Sleeve Color", "Fabric", "Selling Price", "Original Price", "Product Name", "Catalog Description"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        print(f"Starting generation of {TOTAL_IMAGES} items...")
        
        for i in range(1, TOTAL_IMAGES + 1):
            age = random.choice(AGES)
            gender = random.choice(GENDERS)
            shirt_color = random.choice(SHIRT_COLORS)
            sleeve_color = random.choice(SLEEVE_COLORS)
            
            image_name = f"kids_linen_shirt_{i}.png"
            image_path = os.path.join(output_dir, image_name)
            
            product_name = f"Kids Pure Linen Mandarin Collar Half-Sleeve Shirt ({age}, {shirt_color})"
            description = f"Keep your little one cool and stylish with this premium 100% pure linen shirt. Designed with a modern Mandarin collar and breathable half-sleeve style, featuring a {shirt_color} body and {sleeve_color} sleeve combination."
            
            prompt = (
                f"Authentic outdoor lifestyle photography of a happy smiling {age} {gender} walking in a lush green garden. "
                f"The child is wearing a premium 100% pure linen half-sleeve shirt with a modern Mandarin collar. "
                f"The main shirt body is {shirt_color} with contrasting {sleeve_color} half sleeves. "
                f"Natural soft sunlight, realistic skin textures, high definition, sharp focus, fashion catalog look, 8k resolution."
            )
            
            print(f"-> Generating image {i}: {prompt}")
            
            # NO try...except block here. If OpenAI fails, the workflow will stop and show the exact error.
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            image_url = response.data[0].url
            image_data = requests.get(image_url).content
            
            with open(image_path, 'wb') as img_file:
                img_file.write(image_data)
            
            print(f"-> SUCCESS: Downloaded and saved {image_name}")
            
            writer.writerow({
                "Image Name": image_name,
                "Age Group": age,
                "Gender": gender,
                "Shirt Color": shirt_color,
                "Sleeve Color": sleeve_color,
                "Fabric": "100% Pure Linen",
                "Selling Price": "₹599",
                "Original Price": "₹999",
                "Product Name": product_name,
                "Catalog Description": description
            })
            
    print(f"Batch completed successfully! Files saved in {output_dir}")

if __name__ == "__main__":
    run_daily_automation()
