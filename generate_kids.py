import os
import random
import csv
from datetime import datetime

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
    
    # Open CSV to save catalog metadata matching an Excel structure
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
            product_name = f"Kids Pure Linen Mandarin Collar Half-Sleeve Shirt ({age}, {shirt_color})"
            description = f"Keep your little one cool and stylish with this premium 100% pure linen shirt. Designed with a modern Mandarin collar and breathable half-sleeve style, featuring a unique {shirt_color} body and {sleeve_color} sleeve combination. Perfect for casual wear and special occasions."
            
            prompt = f"A high-definition fashion catalog photo of a cute {age} {gender} wearing a 100% pure linen half-sleeve shirt with a Mandarin collar. Main shirt color is {shirt_color} with {sleeve_color} half sleeves. Clean studio lighting, 8k resolution, minimalist background."
            
            # --- API IMAGE GENERATION HOOK ---
            # If utilizing OpenAI/DALL-E 3 or Stability AI, write the fetch implementation here 
            # and save raw image bytes to: os.path.join(output_dir, image_name)
            
            # Writing metadata row into the CSV table
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
