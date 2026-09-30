import os
import random
import csv
import time
import base64
from datetime import datetime
from openai import OpenAI

client = OpenAI()

TOTAL_IMAGES = 5  # Change to 20 when ready
AGES = ["2-3 years", "3-4 years", "4-5 years", "5-6 years", "6-7 years"]
GENDERS = ["boy", "girl"]
SHIRT_COLORS = ["Crisp White", "Pastel Blue", "Mint Green", "Soft Yellow", "Beige"]
SLEEVE_COLORS = ["Contrasting Blue", "Matching Linen", "Dark Grey", "Beige"]

def run_daily_automation():
    today_str = datetime.now().strftime('%Y-%m-%d')
    output_dir = f"./output_{today_str}"
    images_dir = os.path.join(output_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    
    csv_file_path = os.path.join(output_dir, f"catalog_{today_str}.csv")
    
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ["Image Name", "Age Group", "Gender", "Shirt Color", "Sleeve Color", "Fabric", "Selling Price", "Original Price", "Product Name", "Catalog Description"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        print(f"Starting generation of {TOTAL_IMAGES} items using OpenAI response tools...")
        
        for i in range(1, TOTAL_IMAGES + 1):
            age = random.choice(AGES)
            gender = random.choice(GENDERS)
            shirt_color = random.choice(SHIRT_COLORS)
            sleeve_color = random.choice(SLEEVE_COLORS)
            
            image_filename = f"kids_linen_shirt_{i}.png"
            image_path = os.path.join(images_dir, image_filename)
            
            product_name = f"Kids Pure Linen Mandarin Collar Half-Sleeve Shirt ({age}, {shirt_color})"
            description = f"Keep your little one cool and stylish with this premium 100% pure linen shirt. Designed with a modern Mandarin collar and breathable half-sleeve style, featuring a {shirt_color} body and {sleeve_color} sleeve combination."
            
            prompt = (
                f"Outdoor lifestyle photography of a happy smiling {age} {gender} walking in a garden. "
                f"Wearing a 100% pure linen half-sleeve shirt with a Mandarin collar. "
                f"Main shirt body is {shirt_color} with contrasting {sleeve_color} half sleeves. "
                f"Natural soft sunlight, high definition, 8k resolution."
            )
            
            print(f"-> Generating image {i} via API call...")
            
            try:
                response = client.responses.create(
                    model="gpt-6-astra",
                    input=prompt,
                    tools=[
                        {"type": "image_generation", "model": "gpt-image-2.5-sunburst", "action": "generate"}
                    ]
                )
                
                # Extract base64 image results from the response output
                image_data = [
                    output.result
                    for output in response.output
                    if output.type == "image_generation_call"
                ]
                
                if image_data:
                    image_base64 = image_data[0]
                    with open(image_path, "wb") as f:
                        f.write(base64.b64decode(image_base64))
                    print(f"-> SUCCESS: Saved {image_filename} into images/")
                else:
                    print(f"-> WARNING: No image data returned for item {i}")
                    
            except Exception as e:
                print(f"-> ERROR on item {i}: {str(e)}")
            
            writer.writerow({
                "Image Name": f"images/{image_filename}",
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
            
            time.sleep(2)
            
    print(f"Batch generation completed! Catalog stored in {output_dir}")

if __name__ == "__main__":
    run_daily_automation()
