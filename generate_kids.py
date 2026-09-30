import os
import random
import csv
import time
from datetime import datetime
import urllib.parse
import requests

TOTAL_IMAGES = 20
AGES = ["2-3 years", "3-4 years", "4-5 years", "5-6 years", "6-7 years"]
GENDERS = ["boy", "girl"]
SHIRT_COLORS = ["Crisp White", "Pastel Blue", "Mint Green", "Soft Yellow", "Beige", "Lavender", "Coral Pink"]
SLEEVE_COLORS = ["Contrasting Blue", "Matching Linen", "Dark Grey", "Beige", "White"]

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
            
            # Prompt matching your reference style
            prompt_text = (
                f"Outdoor lifestyle photography of a happy smiling {age} {gender} walking in a garden. "
                f"Wearing a 100% pure linen half-sleeve shirt with a Mandarin collar. "
                f"Main shirt body is {shirt_color} with contrasting {sleeve_color} half sleeves. "
                f"Natural soft sunlight, high definition, 8k resolution."
            )
            
            encoded_prompt = urllib.parse.quote(prompt_text)
            api_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=600&height=800&nologo=true"
            
            print(f"-> Generating image {i}/{TOTAL_IMAGES}...")
            
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            
            # Attempt to download the image from the free API
            try:
                response = requests.get(api_url, headers=headers, timeout=60)
                
                if response.status_code == 200 and len(response.content) > 2000:
                    with open(image_path, 'wb') as img_file:
                        img_file.write(response.content)
                    print(f"-> SUCCESS: Saved {image_name}")
                else:
                    print(f"-> WARNING: Image {i} failed (Status: {response.status_code}). Skipping file creation.")
            except Exception as e:
                print(f"-> ERROR downloading image {i}: {str(e)}")
            
            # Write data row to CSV
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
            
            # Brief pause between requests to prevent server timeouts
            time.sleep(3)
            
    print(f"Batch completed successfully! Files saved in {output_dir}")

if __name__ == "__main__":
    run_daily_automation()
