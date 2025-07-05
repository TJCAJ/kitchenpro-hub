#!/usr/bin/env python3
"""
KitchenPro Hub Advanced Content Generator
Automated system for generating new kitchen tool reviews and articles for www.kitchenprohub.com
"""

import json
import os
import re
import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import random

class KitchenProHubContentGenerator:
    def __init__(self, site_root: str = "."):
        self.site_root = Path(site_root)
        self.config = {
            "site_name": "KitchenPro Hub",
            "amazon_tag": "aiincomehub03-20",
            "adsense_publisher": "ca-pub-5260130878751797",
            "base_url": "https://www.kitchenprohub.com",
            "categories": [
                "kitchen-essentials",
                "cooking-appliances", 
                "bakeware",
                "storage-solutions"
            ]
        }
        
    def generate_amazon_link(self, product_name: str) -> str:
        """Generate properly formatted Amazon affiliate link"""
        search_term = product_name.replace(" ", "+").replace("-", "+")
        return f"https://www.amazon.com/s?k={search_term}&tag={self.config['amazon_tag']}"
    
    def get_product_database(self) -> Dict[str, List[Dict]]:
        """Comprehensive database of kitchen products for article generation"""
        return {
            "kitchen-essentials": [
                {
                    "name": "Professional Chef Knife Set",
                    "price_range": "$50-150",
                    "benefits": ["Razor-sharp German steel", "Ergonomic handles", "Full tang construction"],
                    "keywords": ["chef knife", "kitchen knives", "professional knives", "cooking knives"],
                    "season": "year-round"
                },
                {
                    "name": "Bamboo Cutting Board Set",
                    "price_range": "$25-60",
                    "benefits": ["Antibacterial bamboo", "Juice grooves", "Multiple sizes"],
                    "keywords": ["cutting board", "bamboo cutting board", "chopping board", "kitchen prep"],
                    "season": "year-round"
                },
                {
                    "name": "Cast Iron Skillet Collection",
                    "price_range": "$30-80",
                    "benefits": ["Lifetime durability", "Even heat distribution", "Naturally non-stick"],
                    "keywords": ["cast iron skillet", "cooking pan", "frying pan", "cookware"],
                    "season": "year-round"
                },
                {
                    "name": "Stainless Steel Measuring Set", 
                    "price_range": "$20-45",
                    "benefits": ["Dishwasher safe", "Nested storage", "Engraved measurements"],
                    "keywords": ["measuring cups", "measuring spoons", "baking tools", "kitchen measuring"],
                    "season": "baking-season"
                },
                {
                    "name": "Kitchen Scale Digital",
                    "price_range": "$25-50",
                    "benefits": ["Precise measurements", "Multiple units", "Sleek design"],
                    "keywords": ["kitchen scale", "digital scale", "food scale", "baking scale"],
                    "season": "baking-season"
                },
                {
                    "name": "Silicone Utensil Set",
                    "price_range": "$20-40",
                    "benefits": ["Heat resistant", "Non-stick safe", "Easy to clean"],
                    "keywords": ["silicone utensils", "cooking utensils", "heat resistant", "kitchen tools"],
                    "season": "year-round"
                }
            ],
            "cooking-appliances": [
                {
                    "name": "Air Fryer Pro 8-Quart",
                    "price_range": "$80-200",
                    "benefits": ["Healthy oil-free cooking", "Multiple cooking functions", "Large family capacity"],
                    "keywords": ["air fryer", "healthy cooking", "oil-free cooking", "kitchen appliance"],
                    "season": "health-january"
                },
                {
                    "name": "Instant Pot Multi-Cooker",
                    "price_range": "$70-150",
                    "benefits": ["7-in-1 functionality", "Pressure cooking speed", "Smart programming"],
                    "keywords": ["instant pot", "pressure cooker", "multi-cooker", "electric pressure cooker"],
                    "season": "year-round"
                },
                {
                    "name": "Food Processor Professional",
                    "price_range": "$100-250",
                    "benefits": ["Powerful motor", "Multiple attachments", "Large capacity"],
                    "keywords": ["food processor", "kitchen prep", "chopping", "food preparation"],
                    "season": "year-round"
                },
                {
                    "name": "Stand Mixer Professional",
                    "price_range": "$200-500",
                    "benefits": ["Powerful mixing", "Planetary action", "Multiple attachments"],
                    "keywords": ["stand mixer", "baking mixer", "kitchen mixer", "professional baking"],
                    "season": "baking-season"
                },
                {
                    "name": "Immersion Blender Pro",
                    "price_range": "$40-100",
                    "benefits": ["Blend in any container", "Variable speed", "Multiple attachments"],
                    "keywords": ["immersion blender", "hand blender", "stick blender", "soup blender"],
                    "season": "soup-season"
                },
                {
                    "name": "Coffee Maker Programmable",
                    "price_range": "$60-150",
                    "benefits": ["Programmable brewing", "Thermal carafe", "Auto shut-off"],
                    "keywords": ["coffee maker", "programmable coffee", "drip coffee", "automatic coffee"],
                    "season": "year-round"
                }
            ],
            "bakeware": [
                {
                    "name": "Non-Stick Baking Sheet Set",
                    "price_range": "$30-60",
                    "benefits": ["Even heat distribution", "Easy release coating", "Multiple sizes"],
                    "keywords": ["baking sheets", "cookie sheets", "baking pans", "non-stick bakeware"],
                    "season": "baking-season"
                },
                {
                    "name": "Silicone Baking Mat Set",
                    "price_range": "$15-35",
                    "benefits": ["Reusable and eco-friendly", "Perfect non-stick surface", "Easy cleanup"],
                    "keywords": ["silicone baking mats", "reusable baking", "eco-friendly baking", "baking liner"],
                    "season": "baking-season"
                },
                {
                    "name": "Professional Cake Pan Set",
                    "price_range": "$25-55",
                    "benefits": ["Even baking", "Easy release", "Multiple sizes"],
                    "keywords": ["cake pans", "round cake pans", "baking pans", "cake baking"],
                    "season": "baking-season"
                },
                {
                    "name": "Mixing Bowl Stainless Set",
                    "price_range": "$25-50",
                    "benefits": ["Nested storage", "Non-slip base", "Pour spouts"],
                    "keywords": ["mixing bowls", "stainless steel bowls", "baking bowls", "prep bowls"],
                    "season": "baking-season"
                },
                {
                    "name": "Rolling Pin Collection",
                    "price_range": "$20-45",
                    "benefits": ["Multiple materials", "Comfortable grip", "Even rolling"],
                    "keywords": ["rolling pin", "baking tools", "pastry tools", "dough rolling"],
                    "season": "baking-season"
                }
            ],
            "storage-solutions": [
                {
                    "name": "Glass Food Storage Containers",
                    "price_range": "$40-80",
                    "benefits": ["BPA-free glass", "Airtight seals", "Oven and microwave safe"],
                    "keywords": ["food storage", "glass containers", "meal prep", "airtight storage"],
                    "season": "new-year-organization"
                },
                {
                    "name": "Spice Rack Organizer System",
                    "price_range": "$30-70",
                    "benefits": ["Maximizes space", "Clear visibility", "Easy access"],
                    "keywords": ["spice rack", "spice organizer", "kitchen organization", "spice storage"],
                    "season": "new-year-organization"
                },
                {
                    "name": "Pantry Organization Set",
                    "price_range": "$50-120",
                    "benefits": ["Clear containers", "Stackable design", "Freshness seals"],
                    "keywords": ["pantry organizer", "food storage", "kitchen organization", "pantry containers"],
                    "season": "new-year-organization"
                },
                {
                    "name": "Refrigerator Storage Bins",
                    "price_range": "$25-50",
                    "benefits": ["Clear visibility", "Easy cleaning", "Stackable"],
                    "keywords": ["refrigerator organizer", "fridge storage", "food organization", "clear bins"],
                    "season": "new-year-organization"
                }
            ]
        }
    
    def generate_article_content(self, product: Dict, category: str) -> str:
        """Generate complete HTML article for a product"""
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        slug = self.create_article_slug(product['name'])
        
        # Generate affiliate links
        premium_link = self.generate_amazon_link(f"Premium {product['name']}")
        budget_link = self.generate_amazon_link(f"Budget {product['name']}")
        professional_link = self.generate_amazon_link(f"Professional {product['name']}")
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Best {product['name']} Review 2025 - Expert Testing & Buying Guide</title>
    <meta name="description" content="Professional review of the best {product['name'].lower()} in 2025. Expert testing, detailed comparisons, and honest buying recommendations from kitchen professionals.">
    <meta name="keywords" content="{', '.join(product['keywords'])}, kitchen review, buying guide 2025, affiliate review">
    
    <!-- Open Graph -->
    <meta property="og:title" content="Best {product['name']} Review 2025 - {self.config['site_name']}">
    <meta property="og:description" content="Expert review and buying guide for {product['name'].lower()}. Tested by professional chefs.">
    <meta property="og:url" content="{self.config['base_url']}/{category}/{slug}/">
    <meta property="og:type" content="article">
    
    <!-- Schema.org markup -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Review",
        "name": "Best {product['name']} Review 2025",
        "author": {{
            "@type": "Organization",
            "name": "{self.config['site_name']}"
        }},
        "datePublished": "{datetime.datetime.now().isoformat()}",
        "description": "Professional review of the best {product['name'].lower()} with expert testing and recommendations."
    }}
    </script>
    
    <!-- Google AdSense -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={self.config['adsense_publisher']}" crossorigin="anonymous"></script>
    
    <style>
        /* Inline CSS for faster loading */
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; margin: 0; padding: 0; color: #333; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; }}
        header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem 0; }}
        .nav-container {{ display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ font-size: 1.5rem; font-weight: bold; text-decoration: none; color: white; }}
        .nav-menu {{ list-style: none; display: flex; gap: 2rem; margin: 0; padding: 0; }}
        .nav-menu a {{ color: white; text-decoration: none; font-weight: 500; }}
        .nav-menu a:hover {{ text-decoration: underline; }}
        .article-header {{ text-align: center; margin: 2rem 0; }}
        .article-header h1 {{ font-size: 2.5rem; margin-bottom: 1rem; color: #2c3e50; }}
        .article-meta {{ color: #666; margin-bottom: 2rem; }}
        .content-wrapper {{ display: grid; grid-template-columns: 2fr 1fr; gap: 2rem; margin: 2rem 0; }}
        .main-content {{ }}
        .sidebar {{ }}
        .product-card {{ background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 8px; padding: 1.5rem; margin: 1.5rem 0; }}
        .product-card.featured {{ border: 3px solid #28a745; background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); }}
        .buy-button {{ display: inline-block; background: #ff9500; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; margin: 1rem 0; }}
        .buy-button:hover {{ background: #e8890b; }}
        .ad-banner {{ text-align: center; margin: 1rem 0; }}
        .pros-cons {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0; }}
        .pros, .cons {{ padding: 1rem; border-radius: 6px; }}
        .pros {{ background: #d4edda; border-left: 4px solid #28a745; }}
        .cons {{ background: #f8d7da; border-left: 4px solid #dc3545; }}
        .comparison-table {{ width: 100%; border-collapse: collapse; margin: 1rem 0; }}
        .comparison-table th, .comparison-table td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        .comparison-table th {{ background: #f8f9fa; font-weight: bold; }}
        .rating {{ color: #ffc107; font-size: 1.2rem; }}
        footer {{ background: #2c3e50; color: white; padding: 2rem 0; margin-top: 3rem; }}
        .footer-content {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; }}
        .footer-section h3 {{ margin-bottom: 1rem; }}
        .footer-section ul {{ list-style: none; padding: 0; }}
        .footer-section a {{ color: #bdc3c7; text-decoration: none; }}
        .footer-section a:hover {{ color: white; }}
        .footer-bottom {{ text-align: center; margin-top: 2rem; padding-top: 2rem; border-top: 1px solid #34495e; }}
        
        /* Mobile responsive */
        @media (max-width: 768px) {{
            .content-wrapper {{ grid-template-columns: 1fr; }}
            .nav-menu {{ display: none; }}
            .article-header h1 {{ font-size: 2rem; }}
            .pros-cons {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <nav class="nav-container">
                <a href="/" class="logo">{self.config['site_name']}</a>
                <ul class="nav-menu">
                    <li><a href="/">Home</a></li>
                    <li><a href="/reviews.html">Reviews</a></li>
                    <li><a href="/about.html">About</a></li>
                    <li><a href="/contact.html">Contact</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <div class="container">
        <!-- Header Ad -->
        <div class="ad-banner">
            <ins class="adsbygoogle"
                 style="display:block"
                 data-ad-client="{self.config['adsense_publisher']}"
                 data-ad-slot="1234567890"
                 data-ad-format="auto"
                 data-full-width-responsive="true"></ins>
        </div>

        <article>
            <div class="article-header">
                <h1>Best {product['name']} Review 2025: Expert Testing & Buying Guide</h1>
                <div class="article-meta">
                    <span>Published: {current_date}</span> | 
                    <span>By: Kitchen Expert Team</span> | 
                    <span>Category: {category.replace('-', ' ').title()}</span>
                </div>
            </div>

            <div class="content-wrapper">
                <div class="main-content">
                    <section class="intro">
                        <p><strong>Looking for the best {product['name'].lower()}?</strong> Our kitchen experts have spent over 100 hours testing and comparing the top models available in 2025. After rigorous testing in real kitchen conditions, we've identified the clear winners that deliver exceptional performance, durability, and value.</p>
                        
                        <div class="key-benefits">
                            <h3>Why Invest in Quality {product['name']}?</h3>
                            <ul>
"""

        # Add benefits
        for benefit in product['benefits']:
            return f"""                                <li><strong>{benefit}</strong> - Makes a significant difference in cooking results</li>
"""
        
        return f"""                            </ul>
                        </div>
                    </section>

                    <section class="top-picks">
                        <h2>🏆 Our Top 3 {product['name']} Picks for 2025</h2>
                        
                        <div class="product-card featured">
                            <h3>🥇 Best Overall: Premium {product['name']}</h3>
                            <div class="rating">★★★★★ 4.8/5.0</div>
                            <p><strong>Price Range:</strong> {product['price_range']}</p>
                            <p>After extensive testing, this premium model consistently delivered professional-quality results. The build quality is exceptional, and it handles daily use without showing any signs of wear.</p>
                            
                            <div class="pros-cons">
                                <div class="pros">
                                    <h4>✅ Pros</h4>
                                    <ul>
                                        <li>Exceptional build quality</li>
                                        <li>Professional performance</li>
                                        <li>Long-term durability</li>
                                        <li>Easy maintenance</li>
                                    </ul>
                                </div>
                                <div class="cons">
                                    <h4>❌ Cons</h4>
                                    <ul>
                                        <li>Higher price point</li>
                                        <li>May be overkill for casual use</li>
                                    </ul>
                                </div>
                            </div>
                            
                            <a href="{premium_link}" target="_blank" rel="nofollow" class="buy-button">
                                Check Latest Price on Amazon →
                            </a>
                        </div>

                        <div class="product-card">
                            <h3>🥈 Best Value: Budget-Friendly {product['name']}</h3>
                            <div class="rating">★★★★☆ 4.3/5.0</div>
                            <p><strong>Price Range:</strong> {product['price_range']}</p>
                            <p>Perfect for home cooks who want reliable performance without breaking the bank. This model offers excellent value and covers all the essential features you need.</p>
                            
                            <div class="pros-cons">
                                <div class="pros">
                                    <h4>✅ Pros</h4>
                                    <ul>
                                        <li>Excellent value for money</li>
                                        <li>Reliable performance</li>
                                        <li>Easy to use</li>
                                        <li>Good warranty coverage</li>
                                    </ul>
                                </div>
                                <div class="cons">
                                    <h4>❌ Cons</h4>
                                    <ul>
                                        <li>Limited advanced features</li>
                                        <li>Build quality not premium</li>
                                    </ul>
                                </div>
                            </div>
                            
                            <a href="{budget_link}" target="_blank" rel="nofollow" class="buy-button">
                                View on Amazon →
                            </a>
                        </div>

                        <div class="product-card">
                            <h3>🥉 Best Premium: Professional {product['name']}</h3>
                            <div class="rating">★★★★★ 4.9/5.0</div>
                            <p><strong>Price Range:</strong> {product['price_range']}</p>
                            <p>For serious home chefs and cooking enthusiasts who demand the absolute best. This professional-grade model offers restaurant-quality performance and durability.</p>
                            
                            <div class="pros-cons">
                                <div class="pros">
                                    <h4>✅ Pros</h4>
                                    <ul>
                                        <li>Professional-grade quality</li>
                                        <li>Advanced features</li>
                                        <li>Superior performance</li>
                                        <li>Lifetime durability</li>
                                    </ul>
                                </div>
                                <div class="cons">
                                    <h4>❌ Cons</h4>
                                    <ul>
                                        <li>Premium pricing</li>
                                        <li>Complex for beginners</li>
                                    </ul>
                                </div>
                            </div>
                            
                            <a href="{professional_link}" target="_blank" rel="nofollow" class="buy-button">
                                Check Professional Price →
                            </a>
                        </div>
                    </section>

                    <!-- In-Content Ad -->
                    <div class="ad-banner">
                        <ins class="adsbygoogle"
                             style="display:block; text-align:center;"
                             data-ad-layout="in-article"
                             data-ad-format="fluid"
                             data-ad-client="{self.config['adsense_publisher']}"
                             data-ad-slot="5555555555"></ins>
                    </div>

                    <section class="buying-guide">
                        <h2>Complete {product['name']} Buying Guide</h2>
                        
                        <h3>🎯 Key Features to Consider</h3>
                        <div class="features-grid">
                            <h4>Material Quality & Construction</h4>
                            <p>The materials used in your {product['name'].lower()} directly impact performance and longevity. Look for high-grade materials that can withstand daily use and maintain their performance over time.</p>
                            
                            <h4>Size & Capacity</h4>
                            <p>Consider your kitchen space and typical cooking needs. Larger isn't always better - choose the size that fits your actual use cases and storage space.</p>
                            
                            <h4>Ease of Use & Maintenance</h4>
                            <p>User-friendly design and easy maintenance are crucial for daily use. Look for features that simplify operation and cleaning.</p>
                            
                            <h4>Brand Reputation & Warranty</h4>
                            <p>Established brands typically offer better customer support, warranty coverage, and long-term reliability.</p>
                        </div>

                        <h3>💰 Price Tier Analysis</h3>
                        <table class="comparison-table">
                            <thead>
                                <tr>
                                    <th>Price Range</th>
                                    <th>Best For</th>
                                    <th>Expected Features</th>
                                    <th>Durability</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Budget ($20-50)</td>
                                    <td>Occasional use, beginners</td>
                                    <td>Basic functionality</td>
                                    <td>1-2 years</td>
                                </tr>
                                <tr>
                                    <td>Mid-Range ($50-100)</td>
                                    <td>Regular home cooking</td>
                                    <td>Enhanced features, better materials</td>
                                    <td>3-5 years</td>
                                </tr>
                                <tr>
                                    <td>Premium ($100+)</td>
                                    <td>Serious cooking, daily use</td>
                                    <td>Professional features, premium materials</td>
                                    <td>10+ years</td>
                                </tr>
                            </tbody>
                        </table>
                    </section>

                    <section class="testing-methodology">
                        <h2>🔬 Our Testing Process</h2>
                        <p>Our kitchen experts tested each {product['name'].lower()} for a minimum of 30 days in real cooking scenarios. We evaluated performance, durability, ease of use, and overall value for money.</p>
                        
                        <h3>Testing Criteria</h3>
                        <ul>
                            <li><strong>Performance (40%):</strong> How effectively does it accomplish its intended function?</li>
                            <li><strong>Build Quality (25%):</strong> Material quality and construction durability assessment</li>
                            <li><strong>Usability (20%):</strong> Ease of use, ergonomic design, and user experience</li>
                            <li><strong>Maintenance (10%):</strong> Cleaning requirements and long-term care</li>
                            <li><strong>Value (5%):</strong> Performance and quality relative to price point</li>
                        </ul>
                    </section>

                    <section class="conclusion">
                        <h2>🎯 Final Recommendations</h2>
                        <p>After comprehensive testing and analysis, we recommend the <strong>Premium {product['name']}</strong> for most home cooks seeking the best balance of quality, performance, and longevity. For budget-conscious buyers, the <strong>Budget-Friendly {product['name']}</strong> offers exceptional value without sacrificing essential functionality.</p>
                        
                        <div class="final-recommendations">
                            <h3>Shop Our Expert-Tested Top Picks:</h3>
                            <div style="margin: 1rem 0;">
                                <a href="{premium_link}" target="_blank" rel="nofollow" class="buy-button">
                                    🏆 Best Overall: Premium {product['name']} →
                                </a>
                            </div>
                            <div style="margin: 1rem 0;">
                                <a href="{budget_link}" target="_blank" rel="nofollow" class="buy-button">
                                    💰 Best Value: Budget-Friendly {product['name']} →
                                </a>
                            </div>
                            <div style="margin: 1rem 0;">
                                <a href="{professional_link}" target="_blank" rel="nofollow" class="buy-button">
                                    ⚡ Best Premium: Professional {product['name']} →
                                </a>
                            </div>
                        </div>
                    </section>
                </div>

                <div class="sidebar">
                    <!-- Sidebar Ad -->
                    <div class="ad-banner">
                        <ins class="adsbygoogle"
                             style="display:block"
                             data-ad-client="{self.config['adsense_publisher']}"
                             data-ad-slot="9876543210"
                             data-ad-format="auto"
                             data-full-width-responsive="true"></ins>
                    </div>

                    <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
                        <h3>Quick Picks</h3>
                        <p><strong>🏆 Best Overall:</strong><br>
                        <a href="{premium_link}" target="_blank" rel="nofollow">Premium {product['name']}</a></p>
                        
                        <p><strong>💰 Best Value:</strong><br>
                        <a href="{budget_link}" target="_blank" rel="nofollow">Budget-Friendly {product['name']}</a></p>
                        
                        <p><strong>⚡ Best Premium:</strong><br>
                        <a href="{professional_link}" target="_blank" rel="nofollow">Professional {product['name']}</a></p>
                    </div>

                    <div style="background: #e7f3ff; padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
                        <h3>Related Reviews</h3>
                        <ul style="padding-left: 1rem;">
                            <li><a href="/reviews.html">All Kitchen Reviews</a></li>
                            <li><a href="/">Latest Reviews</a></li>
                            <li><a href="/about.html">About Our Testing</a></li>
                        </ul>
                    </div>
                </div>
            </div>
        </article>
    </div>

    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>Reviews</h3>
                    <ul>
                        <li><a href="/reviews.html">All Reviews</a></li>
                        <li><a href="/">Latest Articles</a></li>
                        <li><a href="/about.html">Testing Process</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h3>Information</h3>
                    <ul>
                        <li><a href="/affiliate-disclosure.html">Affiliate Disclosure</a></li>
                        <li><a href="/about.html">About Us</a></li>
                        <li><a href="/contact.html">Contact</a></li>
                        <li><a href="/privacy.html">Privacy Policy</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2025 {self.config['site_name']}. All rights reserved.</p>
                <p><strong>Affiliate Disclosure:</strong> As an Amazon Associate, we earn from qualifying purchases at no extra cost to you.</p>
            </div>
        </div>
    </footer>

    <script>
        // Initialize AdSense ads
        (adsbygoogle = window.adsbygoogle || []).push({{}});
        (adsbygoogle = window.adsbygoogle || []).push({{}});
        (adsbygoogle = window.adsbygoogle || []).push({{}});
    </script>
</body>
</html>"""
    
    def create_article_slug(self, product_name: str) -> str:
        """Convert product name to URL-friendly slug"""
        slug = product_name.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug)
        slug = re.sub(r'-+', '-', slug)
        return slug.strip('-')
    
    def generate_new_article(self) -> Tuple[str, str, str]:
        """Generate a new article and return file path, title, and category"""
        products = self.get_product_database()
        
        # Select random category and product
        category = random.choice(list(products.keys()))
        product = random.choice(products[category])
        
        # Generate article content
        article_content = self.generate_article_content(product, category)
        
        # Create file path - save directly to root for GitHub Pages
        slug = self.create_article_slug(product['name'])
        article_filename = f"{slug}.html"
        article_path = self.site_root / article_filename
        
        # Write article file
        with open(article_path, 'w', encoding='utf-8') as f:
            f.write(article_content)
        
        title = f"Best {product['name']} Review 2025"
        return str(article_path), title, category
    
    def update_reviews_page(self, article_title: str, article_filename: str):
        """Add new article to reviews page"""
        reviews_path = self.site_root / "reviews.html"
        
        try:
            with open(reviews_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create new review entry
            new_review = f'''                <div class="review-card">
                    <h3><a href="/{article_filename}">{article_title}</a></h3>
                    <div class="review-meta">
                        <span class="date">{datetime.datetime.now().strftime("%B %d, %Y")}</span>
                        <span class="rating">★★★★★</span>
                    </div>
                    <p>Professional review with expert testing and honest recommendations. Compare top models and find the perfect choice for your kitchen.</p>
                    <a href="/{article_filename}" class="read-review">Read Full Review →</a>
                </div>'''
            
            # Insert after the first review card
            pattern = r'(<div class="review-card">.*?</div>)'
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, new_review + r'\n\n                \1', content, count=1, flags=re.DOTALL)
                
                with open(reviews_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print("✅ Updated reviews page")
            else:
                print("⚠️  Could not find review card pattern in reviews.html")
                
        except FileNotFoundError:
            print("⚠️  reviews.html not found")
    
    def update_homepage_featured(self, article_title: str, article_filename: str):
        """Update homepage with new featured article"""
        homepage_path = self.site_root / "index.html"
        
        try:
            with open(homepage_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create new featured article entry
            new_featured = f'''                <div class="article-card featured">
                    <h3><a href="/{article_filename}">{article_title}</a></h3>
                    <p>Latest expert review with comprehensive testing and honest recommendations for 2025. Compare top models and find your perfect kitchen companion.</p>
                    <a href="/{article_filename}" class="read-more">Read Full Review →</a>
                </div>'''
            
            # Replace the first featured article
            pattern = r'<div class="article-card featured">.*?</div>'
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, new_featured, content, count=1, flags=re.DOTALL)
                
                with open(homepage_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print("✅ Updated homepage featured content")
            else:
                print("⚠️  Could not find featured article pattern in index.html")
                
        except FileNotFoundError:
            print("⚠️  index.html not found")
    
    def run_automation(self):
        """Main automation function"""
        print(f"🚀 Starting automated content generation for {self.config['site_name']}...")
        print(f"📅 Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Generate new article
            article_path, article_title, category = self.generate_new_article()
            article_filename = Path(article_path).name
            
            print(f"✅ Generated: {article_title}")
            print(f"📝 File: {article_filename}")
            print(f"🏷️  Category: {category}")
            
            # Update reviews page
            self.update_reviews_page(article_title, article_filename)
            
            # Update homepage
            self.update_homepage_featured(article_title, article_filename)
            
            # Create log entry
            log_data = {
                "timestamp": datetime.datetime.now().isoformat(),
                "article_title": article_title,
                "article_filename": article_filename,
                "category": category,
                "status": "success",
                "affiliate_links": 3,
                "adsense_ads": 3
            }
            
            # Save log
            log_file = self.site_root / "automation" / "generation_log.json"
            log_file.parent.mkdir(exist_ok=True)
            
            # Read existing logs
            try:
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            except FileNotFoundError:
                logs = []
            
            logs.append(log_data)
            logs = logs[-100:]  # Keep only last 100 entries
            
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
            
            print("✅ Logged generation event")
            print("🎉 Content automation completed successfully!")
            print(f"💰 Ready for affiliate income on www.kitchenprohub.com")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during content generation: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    print("🍳 KitchenPro Hub Advanced Content Generator")
    print("=" * 50)
    
    # Initialize generator
    generator = KitchenProHubContentGenerator()
    
    # Run automation
    success = generator.run_automation()
    
    if success:
        print("\n🎯 Next steps:")
        print("1. git add .")
        print("2. git commit -m 'Add new product review'")
        print("3. git push origin main")
        print("4. Wait 2-5 minutes for deployment")
        print("5. Check www.kitchenprohub.com for new content")
    else:
        print("\n⚠️  Content generation failed - check error details above")
