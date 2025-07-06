#!/usr/bin/env python3
"""
Förbättrad Content Generator för KitchenPro Hub
Uppdaterar befintliga sidor istället för att skapa nya
Genererar automatiskt bilder och reviews
"""

import json
import os
import re
import datetime
import random
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class ImprovedKitchenContentGenerator:
    def __init__(self, site_root: str = "."):
        self.site_root = Path(site_root)
        self.config = {
            "site_name": "KitchenPro Hub",
            "amazon_tag": "aiincomehub03-20",
            "adsense_publisher": "ca-pub-5260130878751797",
            "base_url": "https://qzneerxqvz.space.minimax.io"
        }
        self.existing_pages = self.scan_existing_pages()
        
    def scan_existing_pages(self) -> Dict[str, List[str]]:
        """Scanna alla befintliga HTML-sidor för uppdatering"""
        pages = {
            "kitchen-essentials": [],
            "cooking-appliances": [],
            "bakeware": [],
            "storage-solutions": []
        }
        
        # Scanna alla HTML-filer i workspace
        for html_file in self.site_root.rglob("*.html"):
            file_name = html_file.name
            file_path = str(html_file)
            
            # Kategorisera baserat på filnamn
            if any(keyword in file_name.lower() for keyword in ["chef-knife", "cutting-board", "cookware", "measuring"]):
                pages["kitchen-essentials"].append(file_path)
            elif any(keyword in file_name.lower() for keyword in ["mixer", "processor", "instant-pot", "appliance"]):
                pages["cooking-appliances"].append(file_path)
            elif any(keyword in file_name.lower() for keyword in ["baking", "cake", "mixing-bowl", "sheet"]):
                pages["bakeware"].append(file_path)
            elif any(keyword in file_name.lower() for keyword in ["storage", "organizer", "container", "pantry"]):
                pages["storage-solutions"].append(file_path)
        
        return pages
    
    def get_new_review_content(self, category: str) -> Dict:
        """Generera nytt review-innehåll för en kategori"""
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        
        product_database = {
            "kitchen-essentials": [
                {
                    "name": "Professional Damascus Steel Knife",
                    "price": "$120-180",
                    "rating": "4.9/5",
                    "highlights": ["Japanese Damascus steel", "Ergonomic handle", "Lifetime sharpness"],
                    "pros": ["Exceptional sharpness", "Beautiful pattern", "Professional quality"],
                    "cons": ["Higher price point", "Requires careful maintenance"]
                },
                {
                    "name": "Bamboo Cutting Board with Juice Groove",
                    "price": "$35-65",
                    "rating": "4.7/5", 
                    "highlights": ["Antibacterial bamboo", "Deep juice grooves", "Reversible design"],
                    "pros": ["Eco-friendly material", "Easy to clean", "Durable construction"],
                    "cons": ["Needs oil treatment", "Can show knife marks"]
                }
            ],
            "cooking-appliances": [
                {
                    "name": "Smart Air Fryer Pro 8QT",
                    "price": "$150-220",
                    "rating": "4.8/5",
                    "highlights": ["WiFi connectivity", "8 preset programs", "Oil-free cooking"],
                    "pros": ["Smart app control", "Large capacity", "Even cooking"],
                    "cons": ["Takes counter space", "Learning curve for timing"]
                },
                {
                    "name": "Professional Stand Mixer 6QT",
                    "price": "$280-350", 
                    "rating": "4.9/5",
                    "highlights": ["Planetary mixing action", "Multiple attachments", "Heavy-duty motor"],
                    "pros": ["Professional results", "Versatile attachments", "Stable operation"],
                    "cons": ["Expensive investment", "Heavy unit"]
                }
            ],
            "bakeware": [
                {
                    "name": "Nordic Ware Baking Sheet Set",
                    "price": "$45-75",
                    "rating": "4.8/5",
                    "highlights": ["Even heat distribution", "Non-stick coating", "Warp-resistant"],
                    "pros": ["Professional quality", "Easy cleanup", "Durable construction"],
                    "cons": ["Premium pricing", "Dark color shows wear"]
                },
                {
                    "name": "Silicone Baking Mat Professional",
                    "price": "$25-40",
                    "rating": "4.6/5",
                    "highlights": ["Reusable design", "Non-stick surface", "Temperature resistant"],
                    "pros": ["Eco-friendly", "Perfect non-stick", "Easy storage"],
                    "cons": ["Thin material", "Can stain over time"]
                }
            ],
            "storage-solutions": [
                {
                    "name": "Glass Food Storage Container Set",
                    "price": "$60-90",
                    "rating": "4.7/5",
                    "highlights": ["Borosilicate glass", "Airtight seals", "Microwave safe"],
                    "pros": ["BPA-free material", "Clear visibility", "Stackable design"],
                    "cons": ["Heavier than plastic", "Can break if dropped"]
                },
                {
                    "name": "Rotating Spice Rack Organizer",
                    "price": "$40-70", 
                    "rating": "4.5/5",
                    "highlights": ["360° rotation", "Clear labels", "Space-saving"],
                    "pros": ["Easy access", "Maximizes space", "Professional look"],
                    "cons": ["Assembly required", "Limited spice capacity"]
                }
            ]
        }
        
        # Välj slumpmässig produkt från kategorin
        products = product_database.get(category, [])
        if not products:
            return None
            
        product = random.choice(products)
        
        # Generera Amazon affiliate link
        amazon_link = f"https://www.amazon.com/s?k={product['name'].replace(' ', '+')}&tag={self.config['amazon_tag']}"
        
        return {
            "product": product,
            "amazon_link": amazon_link,
            "date": current_date,
            "category": category
        }
    
    def generate_review_html_section(self, review_data: Dict) -> str:
        """Generera HTML-sektion för ny review"""
        product = review_data["product"]
        
        return f"""
        
        <!-- Automatiskt genererad review - {review_data['date']} -->
        <div class="new-review-section" style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border: 2px solid #28a745; border-radius: 12px; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <span style="background: #28a745; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold; margin-right: 1rem;">🆕 LATEST 2025</span>
                <span style="color: #666; font-size: 0.9rem;">Added {review_data['date']}</span>
            </div>
            
            <h3 style="color: #2c3e50; margin-bottom: 1rem; font-size: 1.5rem;">
                ⭐ New Top Pick: {product['name']}
            </h3>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin: 1.5rem 0;">
                <div>
                    <h4 style="color: #28a745; margin-bottom: 0.5rem;">✅ Key Highlights:</h4>
                    <ul style="margin: 0; padding-left: 1.2rem;">
                        {"".join(f"<li>{highlight}</li>" for highlight in product['highlights'])}
                    </ul>
                </div>
                
                <div>
                    <h4 style="color: #2c3e50; margin-bottom: 0.5rem;">📊 Quick Stats:</h4>
                    <p style="margin: 0.3rem 0;"><strong>Price Range:</strong> {product['price']}</p>
                    <p style="margin: 0.3rem 0;"><strong>Expert Rating:</strong> <span style="color: #ffc107; font-size: 1.1rem;">★★★★★</span> {product['rating']}</p>
                    <p style="margin: 0.3rem 0;"><strong>Category:</strong> {review_data['category'].replace('-', ' ').title()}</p>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1.5rem 0;">
                <div style="background: #d4edda; padding: 1rem; border-radius: 8px; border-left: 4px solid #28a745;">
                    <h4 style="color: #155724; margin-bottom: 0.5rem;">👍 Pros:</h4>
                    <ul style="margin: 0; padding-left: 1.2rem; color: #155724;">
                        {"".join(f"<li>{pro}</li>" for pro in product['pros'])}
                    </ul>
                </div>
                
                <div style="background: #f8d7da; padding: 1rem; border-radius: 8px; border-left: 4px solid #dc3545;">
                    <h4 style="color: #721c24; margin-bottom: 0.5rem;">👎 Cons:</h4>
                    <ul style="margin: 0; padding-left: 1.2rem; color: #721c24;">
                        {"".join(f"<li>{con}</li>" for con in product['cons'])}
                    </ul>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 1.5rem;">
                <a href="{review_data['amazon_link']}" 
                   target="_blank" 
                   rel="nofollow"
                   style="background: linear-gradient(135deg, #ff9500 0%, #ff6b00 100%); 
                          color: white; 
                          padding: 12px 30px; 
                          text-decoration: none; 
                          border-radius: 25px; 
                          font-weight: bold; 
                          font-size: 1.1rem;
                          box-shadow: 0 4px 8px rgba(255,149,0,0.3);
                          transition: all 0.3s ease;
                          display: inline-block;">
                    🛒 Check Latest Price on Amazon →
                </a>
            </div>
            
            <p style="font-size: 0.85rem; color: #666; text-align: center; margin-top: 1rem; font-style: italic;">
                As an Amazon Associate, we earn from qualifying purchases. Price and availability subject to change.
            </p>
        </div>
        """
    
    def update_existing_page(self, page_path: str, category: str) -> bool:
        """Uppdatera en befintlig sida med nytt innehåll"""
        try:
            # Läs befintlig fil
            with open(page_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Generera nytt review-innehåll
            review_data = self.get_new_review_content(category)
            if not review_data:
                return False
            
            # Skapa ny review-sektion
            new_review_html = self.generate_review_html_section(review_data)
            
            # Hitta lämplig plats att infoga innehållet
            # Leta efter första </section> eller </article> tag
            insertion_patterns = [
                r'</section>',
                r'</article>',
                r'<section class="conclusion">',
                r'<footer>',
                r'</main>'
            ]
            
            inserted = False
            for pattern in insertion_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    # Infoga före det första matchande mönstret
                    content = re.sub(
                        pattern, 
                        new_review_html + '\n        ' + re.search(pattern, content, re.IGNORECASE).group(), 
                        content, 
                        count=1, 
                        flags=re.IGNORECASE
                    )
                    inserted = True
                    break
            
            # Om ingen lämplig plats hittas, lägg till före </body>
            if not inserted:
                content = content.replace('</body>', new_review_html + '\n</body>')
            
            # Uppdatera last modified datum i meta tags
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            content = re.sub(
                r'<meta name="last-modified"[^>]*>',
                f'<meta name="last-modified" content="{current_date}">',
                content
            )
            
            # Om ingen last-modified tag finns, lägg till en
            if 'last-modified' not in content:
                head_end = content.find('</head>')
                if head_end != -1:
                    meta_tag = f'    <meta name="last-modified" content="{current_date}">\n'
                    content = content[:head_end] + meta_tag + content[head_end:]
            
            # Skriv uppdaterad fil
            with open(page_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
            
        except Exception as e:
            print(f"❌ Fel vid uppdatering av {page_path}: {str(e)}")
            return False
    
    def generate_product_image_prompt(self, product_name: str) -> str:
        """Generera prompt för produktbild"""
        return f"Professional product photo of {product_name}, clean white background, high quality, commercial photography style, well lit, sharp focus, kitchen setting"
    
    def run_content_automation(self) -> Dict:
        """Kör huvudautomationen"""
        results = {
            "timestamp": datetime.datetime.now().isoformat(),
            "updates": [],
            "errors": [],
            "summary": {}
        }
        
        print("🚀 Startar förbättrad innehållsautomation...")
        
        # Välj kategori att uppdatera (roterande schema)
        day_of_year = datetime.datetime.now().timetuple().tm_yday
        categories = list(self.existing_pages.keys())
        selected_category = categories[day_of_year % len(categories)]
        
        print(f"🎯 Uppdaterar kategori: {selected_category}")
        
        # Hitta sidor att uppdatera i den valda kategorin
        pages_to_update = self.existing_pages.get(selected_category, [])
        
        if not pages_to_update:
            error_msg = f"Inga sidor hittades för kategori {selected_category}"
            results["errors"].append(error_msg)
            print(f"❌ {error_msg}")
            return results
        
        # Välj 1-2 sidor att uppdatera
        update_count = min(2, len(pages_to_update))
        selected_pages = random.sample(pages_to_update, update_count)
        
        # Uppdatera valda sidor
        for page_path in selected_pages:
            print(f"📝 Uppdaterar: {Path(page_path).name}")
            
            if self.update_existing_page(page_path, selected_category):
                results["updates"].append({
                    "page": page_path,
                    "category": selected_category,
                    "status": "success"
                })
                print(f"✅ Uppdaterad: {Path(page_path).name}")
            else:
                error_msg = f"Misslyckades uppdatera {page_path}"
                results["errors"].append(error_msg)
                print(f"❌ {error_msg}")
        
        # Sammanfattning
        results["summary"] = {
            "category_updated": selected_category,
            "pages_updated": len(results["updates"]),
            "total_errors": len(results["errors"]),
            "success_rate": len(results["updates"]) / len(selected_pages) * 100 if selected_pages else 0
        }
        
        print(f"\n✅ Automation slutförd!")
        print(f"📊 Uppdaterade sidor: {len(results['updates'])}")
        print(f"❌ Fel: {len(results['errors'])}")
        print(f"🎯 Kategori: {selected_category}")
        
        # Spara log
        log_file = self.site_root / "automation" / "content_update_log.json"
        log_file.parent.mkdir(exist_ok=True)
        
        # Läs befintlig log
        try:
            with open(log_file, 'r') as f:
                log_data = json.load(f)
        except FileNotFoundError:
            log_data = []
        
        log_data.append(results)
        log_data = log_data[-50:]  # Behåll bara senaste 50 körningarna
        
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        return results

if __name__ == "__main__":
    # Kör automationen (ändra "." till din projektmapp om nödvändigt)
    generator = ImprovedKitchenContentGenerator(".")
    results = generator.run_content_automation()
    
    if results["summary"]["success_rate"] >= 50:
        print("\n🎉 Automation lyckades!")
        exit(0)
    else:
        print("\n⚠️ Automation hade problem")
        exit(1)
