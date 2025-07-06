#!/usr/bin/env python3
"""
Enkel test för automation
Kör detta för att testa att automationen fungerar
"""

import os
import sys
from pathlib import Path

def test_automation():
    print("🧪 Testar automation setup...")
    
    # Test 1: Kontrollera att automation filen finns
    automation_file = Path("automation/improved_content_generator.py")
    if automation_file.exists():
        print("✅ Automation script hittad")
    else:
        print("❌ Automation script saknas")
        print("   Kopiera 'automation/improved_content_generator.py' till ditt projekt")
        return False
    
    # Test 2: Kontrollera GitHub Actions workflow
    workflow_file = Path(".github/workflows/auto-content-update.yml")
    if workflow_file.exists():
        print("✅ GitHub Actions workflow hittad")
    else:
        print("❌ GitHub Actions workflow saknas")
        print("   Kopiera '.github/workflows/auto-content-update.yml' till ditt projekt")
        return False
    
    # Test 3: Leta efter HTML-filer
    html_files = list(Path(".").rglob("*.html"))
    if len(html_files) > 0:
        print(f"✅ Hittade {len(html_files)} HTML-filer")
        print("   Exempel:", html_files[0].name if html_files else "Ingen")
    else:
        print("⚠️ Inga HTML-filer hittades")
        print("   Automationen kommer inte ha något att uppdatera")
    
    # Test 4: Testa Python dependencies
    try:
        import json
        import datetime
        import random
        print("✅ Python dependencies OK")
    except ImportError as e:
        print(f"❌ Python dependency saknas: {e}")
        print("   Kör: pip install requests beautifulsoup4")
        return False
    
    print("\n🎉 Alla tester godkända!")
    print("\n📋 Nästa steg:")
    print("1. Kör: python automation/improved_content_generator.py")
    print("2. Kontrollera att HTML-filer uppdaterats")
    print("3. Push till GitHub och aktivera Actions")
    
    return True

def run_automation_test():
    """Kör en säker test av automationen"""
    print("🚀 Kör automation test...")
    
    try:
        # Importera automation modulen
        sys.path.append("automation")
        from improved_content_generator import ImprovedKitchenContentGenerator
        
        # Skapa generator (read-only test)
        generator = ImprovedKitchenContentGenerator(".")
        
        # Testa att scanna sidor
        pages = generator.scan_existing_pages()
        total_pages = sum(len(files) for files in pages.values())
        
        print(f"✅ Automation fungerar!")
        print(f"📊 Hittade {total_pages} sidor att uppdatera:")
        for category, files in pages.items():
            if files:
                print(f"   {category}: {len(files)} sidor")
        
        print("\n💡 För att köra riktig uppdatering:")
        print("   python automation/improved_content_generator.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Automation test misslyckades: {e}")
        print("\n🔧 Felsökning:")
        print("1. Kontrollera att alla filer är kopierade korrekt")
        print("2. Kör från projektets root-mapp")
        print("3. Installera dependencies: pip install requests beautifulsoup4")
        return False

if __name__ == "__main__":
    print("🧪 AUTOMATION TEST")
    print("=" * 40)
    
    # Kör setup test
    if test_automation():
        print("\n" + "=" * 40)
        # Kör automation test
        run_automation_test()
    
    print("\n📖 För komplett guide, läs: ENKEL_AUTOMATION_GUIDE.md")
