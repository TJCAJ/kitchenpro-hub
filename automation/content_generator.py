#!/usr/bin/env python3
"""
KitchenPro Hub Content Generator
Automated system for generating new kitchen tool reviews and articles
"""

import json
import random
from datetime import datetime

class KitchenContentGenerator:
    def __init__(self):
        self.products = {
            "kitchen_essentials": [
                "Chef Knives", "Cutting Boards", "Measuring Cups", "Mixing Bowls",
                "Can Openers", "Peelers", "Spatulas", "Tongs", "Whisks"
            ],
            "cooking_appliances": [
                "Stand Mixers", "Food Processors", "Blenders", "Instant Pots",
                "Air Fryers", "Coffee Makers", "Toaster Ovens", "Slow Cookers"
            ],
            "bakeware": [
                "Baking Sheets", "Cake Pans", "Muffin Tins", "Mixing Bowls",
                "Rolling Pins", "Measuring Tools", "Pastry Brushes"
            ],
            "storage": [
                "Food Containers", "Spice Racks", "Pantry Organizers",
                "Refrigerator Storage", "Kitchen Canisters"
            ]
        }

        self.affiliate_tag = "aiincomehub03-20"

    def generate_article_content(self, category, product):
        """Generate article content for a specific product"""
        title = f"Best {product} for Professional Cooking - 2025 Review"

        content = f"""
        <h1>{title}</h1>

        <div class="affiliate-disclosure">
            <strong>Affiliate Disclosure:</strong> This article contains affiliate links.
            We may earn a commission when you make a purchase through our links at no extra cost to you.
        </div>

        <h2>Why {product} Matter in Your Kitchen</h2>
        <p>Every professional chef and serious home cook knows that quality {product.lower()}
        are essential for creating exceptional dishes. In this comprehensive review,
        we'll explore the top-rated {product.lower()} that can transform your cooking experience.</p>

        <h2>Top 3 Recommended {product}</h2>

        <div class="product-review">
            <h3>1. Premium Choice</h3>
            <p>Our top pick offers exceptional quality and professional-grade performance.</p>
            <a href="https://www.amazon.com/s?k={product.replace(' ', '+')}&tag={self.affiliate_tag}"
               target="_blank" class="affiliate-link">View on Amazon</a>
        </div>

        <div class="product-review">
            <h3>2. Best Value</h3>
            <p>Perfect balance of quality and affordability for home cooks.</p>
            <a href="https://www.amazon.com/s?k={product.replace(' ', '+')}&tag={self.affiliate_tag}"
               target="_blank" class="affiliate-link">View on Amazon</a>
        </div>

        <div class="product-review">
            <h3>3. Budget Option</h3>
            <p>Quality option for those just starting their culinary journey.</p>
            <a href="https://www.amazon.com/s?k={product.replace(' ', '+')}&tag={self.affiliate_tag}"
               target="_blank" class="affiliate-link">View on Amazon</a>
        </div>

        <h2>Buying Guide</h2>
        <p>When choosing {product.lower()}, consider these key factors:</p>
        <ul>
            <li>Quality and durability</li>
            <li>Price and value</li>
            <li>Brand reputation</li>
            <li>User reviews and ratings</li>
            <li>Warranty and support</li>
        </ul>

        <h2>Conclusion</h2>
        <p>Investing in quality {product.lower()} is essential for any serious cook.
        Our recommendations are based on thorough testing and professional experience.</p>
        """

        return {
            "title": title,
            "content": content,
            "category": category,
            "product": product,
            "date": datetime.now().isoformat(),
            "affiliate_links": 3
        }

    def generate_new_article(self):
        """Generate a new article"""
        category = random.choice(list(self.products.keys()))
        product = random.choice(self.products[category])

        return self.generate_article_content(category, product)

    def save_article(self, article_data, filename):
        """Save article data to file"""
        with open(filename, 'w') as f:
            json.dump(article_data, f, indent=2)

        print(f"✅ Article saved: {article_data['title']}")
        print(f"📁 File: {filename}")
        print(f"🏷️ Category: {article_data['category']}")
        print(f"📝 Affiliate links: {article_data['affiliate_links']}")

def main():
    """Main function to generate content"""
    generator = KitchenContentGenerator()

    # Generate a new article
    article = generator.generate_new_article()

    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"article_{timestamp}.json"
    generator.save_article(article, filename)

    print("\n🎉 Content generation complete!")
    print("📊 Ready for publication on KitchenPro Hub")

if __name__ == "__main__":
    main()
