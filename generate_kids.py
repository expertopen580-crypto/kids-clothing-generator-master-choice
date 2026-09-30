import os
import random
import csv
import time
from datetime import datetime
import requests

# Retrieve Leonardo API key from environment (set via GitHub Secrets)
LEONARDO_API_KEY = os.environ.get("LEONARDO_API_KEY")
API_URL = "https://cloud.leonardo.ai/api/rest/v1"

TOTAL_IMAGES = 5  # Keep at 5 for testing; change to 20 when ready
AGES = ["2-3 years", "3-4 years", "4-5 years", "5-6 years", "6-7 years"]
GENDERS = ["boy", "girl"]
SHIRT_COLORS = ["Crisp White", "Pastel Blue", "Mint Green", "Soft Yellow", "Beige"]
SLEEVE_COLORS = ["Contrasting Blue", "Matching Linen", "Dark Grey", "Beige"]

def generate_leonardo_image(prompt, save_path):
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {LEONARDO_API_KEY}"
    }
    
    # Step 1: Create generation job
    payload = {
        "prompt": prompt,
        "modelId": "aa77f04e-3eec-4b70-9bc0-a3abd02693f3", # Leonardo Phoenix or standard model ID
        "width": 768,
        "height": 1024,
        "num_images": 1
    }
    
    response = requests.post(f"{API_URL}/generations", json=payload, headers=headers)
    if response.status_code != 200:
        print(f"-> Failed to initiate generation: {response.text}")
        return False
        
    data = response.json()
    generation_id = data.get("sdGenerationJob", {}).get("generationId")
    
    if not generation_id:
        print("-> Did not receive a generation ID from Leonardo.")
        return False
        
    # Step 2: Poll for completion
    print(f"-> Polling Leonardo for job ID {generation_id}...")
    for _ in xrange(15) if 'xrange' in globals() else range(15): # Poll up to 15 times (~45 seconds)
        time.sleep(4)
        status_res = requests.get(f"{API_URL}/generations/{generation_id}", headers=headers)
        if status_res.status_code == 200:
            gen_data = status_res.json().get("generations_by_pk", {})
            status = gen_data.get("status")
            
            if status == "COMPLETE":
                images = gen_data.get("generated_images", [])
                if images:
                    image_url = images[0].get("url")
                    # Download the image file
                    img_data = requests.get(image_url).content
                    with open(save_path, "wb") as handler:
                        handler.write(img_data)
                    return True
            elif status == "FAILED":
                print("-> Leonardo generation job failed.")
                return False
        
    print("-> Generation timed out.")
    return False

def run_daily_automation():
    if not LEONARDO_API_KEY:
        raise ValueError("LEONARDO_API_KEY environment variable is missing!")
        
    today_str = datetime.now().strftime('%Y-%m-%d')
    output_dir = f"./output_{today_str}"
    images_dir = os.path.join(output_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    
    csv_file_path = os.path.join(output_dir, f"catalog_{today_str}.csv")
    
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ["Image Name", "Age Group", "Gender", "Shirt Color", "Sleeve Color", "Fabric", "Selling Price", "Original Price", "Product Name", "Catalog Description"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        print(f"Starting generation of {TOTAL_IMAGES} items using Leonardo AI...")
        
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
            
            print(f"-> Processing item {i}/{TOTAL_IMAGES} via Leonardo...")
            success = generate_leonardo_image(prompt, image_path)
            
            if success:
                print(f"-> SUCCESS: Saved {image_filename} inside images/")
            else:
                print(f"-> WARNING: Skipped saving image for item {i}")
            
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
            
    print(f"Batch completed! Files stored in {output_dir}")

if __name__ == "__main__":
    run_daily_automation()
