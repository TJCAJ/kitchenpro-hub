# ERSÄTT DIN GAMLA run_content_automation MED DENNA NYA VERSION
    def run_content_automation(self):
        """
        Kör huvudautomationen.
        FOKUSERAD VERSION: Uppdaterar endast en specifik sida, t.ex. reviews.html.
        """
        print("🚀 Startar innehållsautomation (Fokuserad på en sida)...")

        # Steg 1: Definiera målet
        target_page_path = "reviews.html"
        target_file = self.site_root / target_page_path

        if not target_file.exists():
            print(f"❌ Målsidan '{target_page_path}' hittades inte. Avbryter.")
            return

        # Steg 2: Välj en slumpmässig kategori att skapa innehåll för
        # (Vi hämtar kategorierna direkt från produktdatabasen för flexibilitet)
        product_database = self.get_new_review_content.__defaults__[0] # Ett knep för att komma åt databasen
        available_categories = list(product_database.keys())
        if not available_categories:
            print("❌ Hittade inga kategorier i produktdatabasen. Avbryter.")
            return

        selected_category = random.choice(available_categories)
        print(f"🎯 Vald kategori för nytt innehåll: {selected_category}")

        # Steg 3: Anropa uppdateringsfunktionen för den specifika sidan
        print(f"📝 Försöker uppdatera: {target_page_path}")
        if self.update_existing_page(str(target_file), selected_category):
            print(f"✅ Uppdatering lyckades för: {target_page_path}")
        else:
            print(f"❌ Uppdatering misslyckades för: {target_page_path}")