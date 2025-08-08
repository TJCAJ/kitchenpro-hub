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
            "amazon_tag": "aiincomehub03-20",
        }
        try:
            openai.api_key = os.environ["OPENAI_API_KEY"]
            print("🔑 OpenAI API-nyckel laddad.")
        except KeyError:
            print("❌ FEL: OPENAI_API_KEY hittades inte.")
            exit(1)

    def get_new_review_content(self, existing_content: str) -> Optional[Dict]:
        """Hämtar en ny produkt från en utökad databas, undviker dubbletter."""
        product_database = {
            "kitchen-essentials": [
                {
                    "name": "Professional Damascus Steel Knife",
                    "price": "$120-180",
                    "rating": 5,
                    "summary": "The ultimate chef's knife for precision and durability. A true kitchen workhorse that makes every cut a pleasure.",
                    "text": "This Damascus steel knife combines 67 layers of high-carbon steel to create a blade that is not only incredibly sharp but also stunningly beautiful. The ergonomic G10 handle provides a comfortable and secure grip for prolonged use.",
                    "pros": [
                        "Exceptional edge retention",
                        "Perfect weight balance",
                        "Resists corrosion and rust",
                    ],
                    "cons": [
                        "Premium price point",
                        "Requires hand washing and regular honing",
                    ],
                },
                {
                    "name": "Bamboo Cutting Board (3-Piece Set)",
                    "price": "$35-65",
                    "rating": 4,
                    "summary": "An eco-friendly and durable cutting surface that's gentle on your knives and naturally antimicrobial.",
                    "text": "Made from sustainable organic bamboo, this set of three boards covers all your chopping needs. The built-in juice grooves catch liquids, keeping your countertops clean during food prep.",
                    "pros": [
                        "Eco-friendly material",
                        "Easy to clean",
                        "Durable construction",
                        "Includes multiple sizes",
                    ],
                    "cons": [
                        "Needs occasional oil treatment",
                        "Can show deep knife marks over time",
                    ],
                },
            ],
            "cooking-appliances": [
                {
                    "name": "Smart Air Fryer Pro 8QT",
                    "price": "$150-220",
                    "rating": 5,
                    "summary": "Achieve crispy, delicious results with a fraction of the oil. Smart connectivity makes cooking easier than ever.",
                    "text": "With its large 8-quart capacity, this air fryer is perfect for families. The integrated smart app allows you to monitor and control cooking from your phone, with dozens of pre-set programs for perfect results.",
                    "pros": [
                        "Smart app control",
                        "Large capacity for families",
                        "Even and fast cooking",
                    ],
                    "cons": [
                        "Takes up significant counter space",
                        "Slight learning curve for custom recipes",
                    ],
                },
                {
                    "name": "Sous Vide Precision Cooker Nano",
                    "price": "$99-130",
                    "rating": 4,
                    "summary": "Restaurant-quality results at home. This compact sous vide cooker ensures perfectly cooked food every single time.",
                    "text": "The Nano brings precise temperature control to your kitchen, cooking food to the exact level of doneness you desire. It's smaller than its competitors, making it easy to store, and connects via Bluetooth to a user-friendly app.",
                    "pros": [
                        "Perfect, consistent results",
                        "Compact and easy to store",
                        "Simple to use with app",
                    ],
                    "cons": [
                        "Slower than traditional cooking",
                        "Requires a separate water container",
                    ],
                },
            ],
        }

        all_products = [
            product
            for category_products in product_database.values()
            for product in category_products
        ]
        available_products = [
            p for p in all_products if p["name"] not in existing_content
        ]

        if not available_products:
            print(
                "⚠️ Alla produkter finns redan på sidan. Ingen ny genereras denna gång."
            )
            return None

        product = random.choice(available_products)

        return {
            "product": product,
            "amazon_link": f"https://www.amazon.com/s?k={product['name'].replace(' ', '+')}&tag={self.config['amazon_tag']}",
        }

    def generate_review_html_section(self, review_data: Dict, image_path: str) -> str:
        """Genererar HTML som exakt matchar designen på reviews.html."""
        product = review_data["product"]

        # Funktion för att skapa stjärnor baserat på betyg
        def create_stars(rating: int):
            stars_html = ""
            for i in range(5):
                if i < rating:
                    stars_html += '<span class="star">★</span>\n'
                else:
                    stars_html += '<span class="star empty">★</span>\n'
            return stars_html

        return f"""
                <div class="review-card">
                    <img src="{image_path}" alt="Image of {product['name']}" class="review-image">
                    <div class="review-content">
                        <div class="review-header">
                            <h2 class="review-title">{product['name']}</h2>
                            <div class="star-rating">
                                {create_stars(product['rating'])}
                            </div>
                        </div>

                        <div class="review-summary">
                            "{product['summary']}"
                        </div>

                        <div class="review-text">
                            {product['text']}
                        </div>

                        <div class="pros-cons">
                            <div class="pros">
                                <h4>Pros</h4>
                                <ul>
                                    {"".join(f"<li>{pro}</li>" for pro in product['pros'])}
                                </ul>
                            </div>
                            <div class="cons">
                                <h4>Cons</h4>
                                <ul>
                                    {"".join(f"<li>{con}</li>" for con in product['cons'])}
                                </ul>
                            </div>
                        </div>

                        <div class="review-footer">
                            <span class="price-range">{product['price']}</span>
                            <a href="{review_data['amazon_link']}" class="buy-button" target="_blank" rel="nofollow">View on Amazon</a>
                        </div>
                    </div>
                </div>
                """

    def update_existing_page(self, page_path: str) -> bool:
        """Uppdaterar reviews.html genom att infoga en ny review-card i reviews-grid."""
        try:
            with open(page_path, "r", encoding="utf-8") as f:
                content = f.read()

            review_data = self.get_new_review_content(content)
            if not review_data:
                return False

            print(f"🎨 Genererar bild för '{review_data['product']['name']}'...")
            image_path = self.generate_and_save_image(review_data["product"]["name"])
            if not image_path:
                print("❌ Misslyckades generera bild.")
                return False
            print(f"🖼️ Bild sparad till: {image_path}")

            new_html_card = self.generate_review_html_section(review_data, image_path)

            # Säkrare injektion: Leta efter slutet på reviews-grid
            injection_marker = '<div class="reviews-grid">'
            if injection_marker in content:
                # Infoga det nya kortet precis efter öppningstaggen för grid
                content = content.replace(
                    injection_marker, injection_marker + "\n\n" + new_html_card, 1
                )
                print(f"✅ Nytt review-kort infogat i {Path(page_path).name}")
            else:
                print(
                    f"❌ Hittade inte '<div class=\"reviews-grid\">' i {Path(page_path).name}. Avbryter."
                )
                return False

            with open(page_path, "w", encoding="utf-8") as f:
                f.write(content)

            return True

        except Exception as e:
            print(f"❌ Fel vid uppdatering av {page_path}: {e}")
            return False

    def run_content_automation(self):
        """Kör huvudautomationen - fokuserar bara på reviews.html."""
        print("🚀 Startar innehållsautomation (Fokuserad på reviews.html)...")
        target_page_path = "reviews.html"

        if not (self.site_root / target_page_path).exists():
            print(f"❌ Målsidan '{target_page_path}' hittades inte. Avbryter.")
            return

        print(f"📝 Försöker uppdatera: {target_page_path}")
        if self.update_existing_page(target_page_path):
            print(f"✅ Uppdatering lyckades för: {target_page_path}")
        else:
            print(
                f"❌ Uppdatering misslyckades eller hoppades över för: {target_page_path}"
            )

    def generate_product_image_prompt(self, product_name: str) -> str:
        return f"Professional studio product photo of a {product_name}, on a clean white background, commercial photography, sharp focus, high detail, 4K"

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
            image_dir = self.site_root / "assets" / "images" / "reviews"
            image_dir.mkdir(parents=True, exist_ok=True)
            safe_filename = re.sub(r"[^a-z0-9]+", "-", product_name.lower()).strip("-")
            final_filename = f"{safe_filename}.png"
            image_save_path = image_dir / final_filename
            with open(image_save_path, "wb") as f:
                f.write(image_data)
            return f"/assets/images/reviews/{final_filename}"
        except Exception as e:
            print(f"❌ Fel vid bildgenerering: {e}")
            return None


if __name__ == "__main__":
    ImprovedKitchenContentGenerator(".").run_content_automation()
