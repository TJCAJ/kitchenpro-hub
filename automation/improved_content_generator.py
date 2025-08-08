#!/usr/bin/env python3
import json
import os
import re
import datetime
import random
from pathlib import Path
from typing import Dict, List, Optional
import openai
import requests


class ImprovedKitchenContentGenerator:
    def __init__(self, site_root: str = "."):
        self.site_root = Path(site_root)
        self.config = {
            "site_name": "KitchenPro Hub",
            "amazon_tag": "aiincomehub03-20",
        }
        self.existing_pages = self.scan_existing_pages()
        try:
            openai.api_key = os.environ["OPENAI_API_KEY"]
            print("🔑 OpenAI API-nyckel laddad.")
        except KeyError:
            print(
                "❌ FEL: OPENAI_API_KEY hittades inte. Säkerställ att den är satt som en Secret i GitHub Actions."
            )
            exit(1)

    def scan_existing_pages(self) -> Dict[str, List[str]]:
        pages = {
            "kitchen-essentials": [],
            "cooking-appliances": [],
            "bakeware": [],
            "storage-solutions": [],
        }
        for html_file in self.site_root.rglob("*.html"):
            file_name, file_path = html_file.name, str(html_file)
            if any(
                k in file_name.lower()
                for k in ["chef-knife", "cutting-board", "cookware", "measuring"]
            ):
                pages["kitchen-essentials"].append(file_path)
            elif any(
                k in file_name.lower()
                for k in ["mixer", "processor", "instant-pot", "appliance"]
            ):
                pages["cooking-appliances"].append(file_path)
            elif any(
                k in file_name.lower()
                for k in ["baking", "cake", "mixing-bowl", "sheet"]
            ):
                pages["bakeware"].append(file_path)
            elif any(
                k in file_name.lower()
                for k in ["storage", "organizer", "container", "pantry"]
            ):
                pages["storage-solutions"].append(file_path)
        return pages

    def get_new_review_content(self, category: str) -> Optional[Dict]:
        db = {
            "kitchen-essentials": [
                {
                    "name": "Professional Damascus Steel Knife",
                    "price": "$120-180",
                    "rating": "4.9/5",
                    "highlights": ["Japanese Damascus steel", "Ergonomic handle"],
                    "pros": ["Exceptional sharpness", "Beautiful pattern"],
                    "cons": ["Higher price point", "Requires maintenance"],
                }
            ],
            "cooking-appliances": [
                {
                    "name": "Smart Air Fryer Pro 8QT",
                    "price": "$150-220",
                    "rating": "4.8/5",
                    "highlights": ["WiFi connectivity", "8 preset programs"],
                    "pros": ["Smart app control", "Large capacity"],
                    "cons": ["Takes counter space", "Learning curve"],
                }
            ],
            "bakeware": [
                {
                    "name": "Nordic Ware Baking Sheet Set",
                    "price": "$45-75",
                    "rating": "4.8/5",
                    "highlights": ["Even heat distribution", "Non-stick coating"],
                    "pros": ["Professional quality", "Easy cleanup"],
                    "cons": ["Premium pricing", "Shows wear"],
                }
            ],
            "storage-solutions": [
                {
                    "name": "Glass Food Storage Container Set",
                    "price": "$60-90",
                    "rating": "4.7/5",
                    "highlights": ["Borosilicate glass", "Airtight seals"],
                    "pros": ["BPA-free material", "Stackable design"],
                    "cons": ["Heavier than plastic", "Can break"],
                }
            ],
        }
        products = db.get(category, [])
        if not products:
            return None
        product = random.choice(products)
        return {
            "product": product,
            "amazon_link": f"https://www.amazon.com/s?k={product['name'].replace(' ', '+')}&tag={self.config['amazon_tag']}",
            "date": datetime.datetime.now().strftime("%B %d, %Y"),
            "category": category,
        }

    def generate_review_html_section(self, review_data: Dict, image_path: str) -> str:
        product = review_data["product"]
        return f"""<div class="new-review-section" style="background:#f8f9fa;border:2px solid #28a745;border-radius:12px;padding:2rem;margin:2rem 0;box-shadow:0 4px 6px rgba(0,0,0,0.1);"><h3 style="color:#2c3e50;margin-bottom:1.5rem;font-size:1.5rem;text-align:center;">⭐ New Top Pick: {product['name']}</h3><div class="review-image-container" style="text-align:center;margin-bottom:2rem;"><img src="{image_path}" alt="Professional product shot of {product['name']}" style="max-width:80%;height:auto;border-radius:8px;box-shadow:0 4px 8px rgba(0,0,0,0.15);border:1px solid #ddd;"/></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin:1.5rem 0;"><div><h4 style="color:#28a745;">✅ Key Highlights:</h4><ul style="padding-left:1.2rem;">{"".join(f"<li>{h}</li>" for h in product['highlights'])}</ul></div><div><h4>📊 Quick Stats:</h4><p><strong>Price:</strong> {product['price']}</p><p><strong>Rating:</strong> {product['rating']}</p></div></div><div style="text-align:center;margin-top:1.5rem;"><a href="{review_data['amazon_link']}" target="_blank" rel="nofollow" style="background:#ff9500;color:white;padding:12px 30px;text-decoration:none;border-radius:25px;font-weight:bold;font-size:1.1rem;">🛒 Check Price on Amazon →</a></div></div>"""

    def update_existing_page(self, page_path: str, category: str) -> bool:
        try:
            with open(page_path, "r", encoding="utf-8") as f:
                content = f.read()
            review_data = self.get_new_review_content(category)
            if not review_data:
                return False
            print(f"🎨 Genererar bild för '{review_data['product']['name']}'...")
            image_path = self.generate_and_save_image(review_data["product"]["name"])
            if not image_path:
                return False
            print(f"🖼️ Bild sparad till: {image_path}")
            new_html = self.generate_review_html_section(review_data, image_path)
            insertion_point = re.search(
                r"</section>|</article>|<footer>|</main>", content, re.IGNORECASE
            )
            if insertion_point:
                content = (
                    content[: insertion_point.start()]
                    + new_html
                    + content[insertion_point.start() :]
                )
            else:
                content = content.replace("</body>", new_html + "\n</body>")
            with open(page_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"❌ Fel vid uppdatering av {page_path}: {e}")
            return False

    def generate_product_image_prompt(self, product_name: str) -> str:
        return f"Professional product photo of a {product_name}, clean white background, high quality, commercial photography style, well lit, sharp focus, 4K"

    def generate_and_save_image(self, product_name: str) -> Optional[str]:
        try:
            prompt = self.generate_product_image_prompt(product_name)
            response = openai.Image.create(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size="1024x1024",
                quality="standard",
            )
            image_url = response.data[0].url
            image_data = requests.get(image_url).content
            image_dir = self.site_root / "assets" / "images"
            image_dir.mkdir(parents=True, exist_ok=True)
            safe_filename = re.sub(r"[^a-z0-9]+", "-", product_name.lower()).strip("-")
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            final_filename = f"{safe_filename}-{timestamp}.png"
            image_save_path = image_dir / final_filename
            with open(image_save_path, "wb") as f:
                f.write(image_data)
            return f"/assets/images/{final_filename}"
        except Exception as e:
            print(f"❌ Fel vid bildgenerering: {e}")
            return None

    def run_content_automation(self):
        print("🚀 Startar innehållsautomation...")
        day_of_year = datetime.datetime.now().timetuple().tm_yday
        categories = list(self.existing_pages.keys())
        selected_category = categories[day_of_year % len(categories)]
        pages_to_update = self.existing_pages.get(selected_category, [])
        if not pages_to_update:
            return
        for page_path in random.sample(pages_to_update, min(2, len(pages_to_update))):
            print(f"📝 Uppdaterar: {Path(page_path).name}")
            if self.update_existing_page(page_path, selected_category):
                print(f"✅ Uppdaterad: {Path(page_path).name}")


if __name__ == "__main__":
    ImprovedKitchenContentGenerator().run_content_automation()
