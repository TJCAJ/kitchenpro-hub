#!/usr/bin/env python3
import os
import json
from pathlib import Path
from typing import Dict, Optional
import openai
import random


class JsonContentGenerator:
    def __init__(self, site_root: str = "."):
        self.site_root = Path(site_root)
        self.json_db_path = self.site_root / "_data" / "products.json"

        try:
            # Använder den nya OpenAI-biblioteksversionen (v1.x+)
            self.client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
            print("🔑 OpenAI client skapad.")
        except KeyError:
            print("❌ FEL: OPENAI_API_KEY hittades inte.")
            exit(1)

    def get_existing_product_names(self) -> list:
        """Läser databasen och returnerar en lista med alla produktnamn."""
        if not self.json_db_path.exists():
            return []
        with open(self.json_db_path, "r", encoding="utf-8") as f:
            products = json.load(f)
        return [p.get("productName", "").lower() for p in products]

    def generate_new_product_idea(
        self, category: str, existing_names: list
    ) -> Optional[str]:
        """Genererar en ny produktidé som inte redan finns."""
        print(f"🧠 Tänker ut en ny produktidé för kategorin '{category}'...")
        topic_ideas = {
            "bakeware": [
                "Professional Bundt Pan",
                "Silicone Baking Mat Set",
                "Adjustable Rolling Pin",
            ],
            "kitchen-essentials": [
                "High-Precision Digital Kitchen Scale",
                "Premium Stainless Steel Tongs",
                "Microplane Zester/Grater",
            ],
            "cooking-appliances": [
                "High-Performance Immersion Blender",
                "Countertop Electric Grill",
                "Programmable Slow Cooker",
            ],
            "storage-solutions": [
                "Modular Airtight Pantry Containers",
                "Expandable Drawer Organizer",
                "Heavy-Duty Vacuum Sealer",
            ],
        }

        available_topics = [
            t for t in topic_ideas.get(category, []) if t.lower() not in existing_names
        ]
        if not available_topics:
            print(
                f"⚠️ Inga nya produktidéer hittades för '{category}'. Alla verkar redan finnas."
            )
            return None

        chosen_topic = random.choice(available_topics)
        print(f"💡 Vald produktidé: {chosen_topic}")
        return chosen_topic

    def generate_product_data_from_ai(
        self, product_name: str, category: str
    ) -> Optional[Dict]:
        """Ber AI:n att generera all data för en specifik produkt i JSON-format."""
        print(f"✍️ Genererar data för '{product_name}'...")
        system_prompt = "You are an expert content creator for KitchenPro Hub, a kitchen supply review website. You generate structured data for product reviews. The output must be a valid JSON object."
        user_prompt = f"""
        Generate a detailed product review object for the product "{product_name}". The JSON object must have these exact keys:
        - "productName": "{product_name}" (string)
        - "category": "{category}" (string)
        - "image": "/images/products/{category}/{product_name.lower().replace(' ', '-')}.jpg" (a placeholder image path, string)
        - "rating": an integer from 3 to 5
        - "price": a price range string, e.g., "$50-75"
        - "summary": a compelling one-sentence summary quote
        - "text": a detailed review paragraph of 2-3 sentences
        - "pros": a list of 3 string bullet points
        - "cons": a list of 2 string bullet points
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
            )
            product_data = json.loads(response.choices[0].message.content)
            print("✅ Produktdata genererad.")
            return product_data
        except Exception as e:
            print(f"❌ Fel vid generering av produktdata: {e}")
            return None

    def run(self):
        """Huvudfunktionen som kör hela processen."""
        print("🚀 Startar automation för att uppdatera produktdatabasen...")

        # 1. Läs befintlig data
        self.json_db_path.parent.mkdir(
            exist_ok=True
        )  # Skapar _data-mappen om den inte finns
        if self.json_db_path.exists():
            with open(self.json_db_path, "r", encoding="utf-8") as f:
                all_products = json.load(f)
        else:
            all_products = []

        existing_names = [p.get("productName", "").lower() for p in all_products]

        # 2. Välj en kategori och generera en ny produktidé
        categories = [
            "bakeware",
            "kitchen-essentials",
            "cooking-appliances",
            "storage-solutions",
        ]
        chosen_category = random.choice(categories)
        new_product_name = self.generate_new_product_idea(
            chosen_category, existing_names
        )

        if not new_product_name:
            print("✅ Processen avslutad, ingen ny produkt att lägga till.")
            return

        # 3. Generera datan för den nya produkten
        new_product_data = self.generate_product_data_from_ai(
            new_product_name, chosen_category
        )
        if not new_product_data:
            print("❌ Processen avbruten, kunde inte generera produktdata.")
            return

        # 4. Lägg till den nya produkten i listan och spara filen
        all_products.append(new_product_data)
        with open(self.json_db_path, "w", encoding="utf-8") as f:
            json.dump(all_products, f, indent=2, ensure_ascii=False)

        print(
            f"💾 Databasen uppdaterad! Ny produkt '{new_product_name}' har lagts till i '{self.json_db_path}'."
        )


if __name__ == "__main__":
    JsonContentGenerator().run()
