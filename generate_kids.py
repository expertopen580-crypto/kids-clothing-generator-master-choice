import os
import random
import csv
from datetime import datetime
import requests
from openai import OpenAI

# Initialize OpenAI Client (reads OPENAI_API_KEY from GitHub Secrets automatically)
client = OpenAI()

TOTAL_IMAGES = 20
AGES = ["2-3 years", "3-4 years", "4-5 years", "5-6 years", "6-7 years"]
GENDERS = ["boy", "girl"]
SHIRT_COLORS = ["Pastel Blue", "Mint Green", "Soft Yellow", "Coral Pink", "Lavender", "Beige", "Navy Blue", "Crisp White", "Charcoal Grey", "Peach"]
SLEEVE_COLORS = ["Contrasting White", "Matching Linen", "Dark Grey", "Navy Blue", "Beige"]

def run_daily_automation():
    today_str = datetime.now().strftime('%Y-%m-%d')
    output_dir = f"./output_{today_str}"
    os.makedirs(output_dir, exist_ok=True)
    
    csv_file_path = os.path.join(output_dir, f"catalog_{today_str}.csv")
    
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ["Image Name", "Age Group", "Gender", "Shirt Color", "Sleeve Color", "Fabric", "Selling Price", "Original Price", "Product Name", "Catalog Description"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        print(f"Starting daily generation of {TOTAL_IMAGES} items...")
        
        for i in range(1, TOTAL_IMAGES + 1):
            age = random.choice(AGES)
            gender = random.choice(GENDERS)
            shirt_color = random.choice(SHIRT_COLORS)
            sleeve_color = random.choice(SLEEVE_COLORS)
            
            image_name = f"kids_linen_shirt_{i}.png"
            image_path = os.path.join(output_dir, image_name)
            
            product_name = f"Kids Pure Linen Mandarin Collar Half-Sleeve Shirt ({age}, {shirt_color})"
            description = f"Keep your little one cool and stylish with this premium 100% pure linen shirt. Designed with a modern Mandarin collar and breathable half-sleeve style, featuring a unique {shirt_color} body and {sleeve_color} sleeve combination."
            
            prompt = f"A high-definition studio fashion catalog photo of a cute {age} {gender} wearing a 100% pure linen half-sleeve shirt with a Mandarin collar. Main shirt color is {shirt_color} with {sleeve_color} half sleeves. Clean studio lighting, 8k resolution, minimalist background."
            
            print(f"Generating image {i}/{TOTAL_IMAGES}: {prompt}")
            
            try:
                # Call OpenAI Image Generation API (supports DALL-E 3 / gpt-image models)
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024", # OpenAI standard size; you can resize later if strict 600x800 is required
                    quality="standard",
                    n=1
                )
                
                image_url = response.data[0].url
                
                # Download and save the binary image file locally
                image_data = requests.get(image_url).content
                with open(image_path, 'wb') as img_file:
                    img_file.write(image_data)
                
                print(f"Successfully saved {image_name}")
                
            except Exception as e:
                print(f"Error generating image {i}: {e}")
            
            # Write metadata row into the CSV table
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
            
    print(f"Batch generation completed successfully! CSV table created at {csv_file_path}")

if __name__ == "__main__":
    run_daily_automation()
