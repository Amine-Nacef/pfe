import requests
from bs4 import BeautifulSoup
import os
import json
source="WikiLeaks"
def scraper_wikileaks(base_url, pages):
    dossier_sortie = "scrap_result"
    try:
        os.makedirs(dossier_sortie, exist_ok=True)
    except Exception as e:
        print(f"Erreur lors de la création du dossier : {e}")
        return
    
    fichier_resultat = os.path.join(dossier_sortie, "resultats_scrap.txt")
    fichier_json = os.path.join(dossier_sortie, "donnees.json")
    
    resultats = []
    
    for page in range(1, pages + 1):
        url = f"{base_url}&page={page}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Erreur lors de la récupération de la page {page}: {e}")
            continue
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        for result in soup.find_all("div", class_="result"):
            lien = result.find("a", href=True)
            date = result.find("div", class_="date")
            date_span = date.find("span") if date else None
            titre = result.find("h4")
            
            lien_text = lien["href"].strip() if lien else "Aucun lien"
            date_text = date_span.text.strip() if date_span else "Aucune date"
            titre_text = titre.text.strip() if titre else "Aucun titre"
            
            resultats.append((lien_text, date_text, titre_text,source))
    
    try:
        with open(fichier_resultat, "w", encoding="utf-8") as f:
            for lien, date, titre in resultats:
                f.write(f"Lien : {lien}\n")
                f.write(f"Date : {date}\n")
                f.write(f"Titre : {titre}\n")
                f.write(f"Source : {source}\n")
                f.write("-" * 50 + "\n")
    except Exception as e:
        print(f"Erreur lors de l'écriture du fichier texte : {e}")
    
    try:
        resultats_json = [{"lien": lien, "date": date, "titre": titre, "source": source} for lien, date, titre, source in resultats]
        with open(fichier_json, "w", encoding="utf-8") as f:
            json.dump(resultats_json, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erreur lors de l'écriture du fichier JSON : {e}")
    
    print(f"\n{len(resultats)} éléments enregistrés dans '{fichier_resultat}'")
    print(f"\nFichier JSON généré : {fichier_json}")
    print(f"\nDossier des résultats : {os.path.abspath(dossier_sortie)}")

base_url = "https://search.wikileaks.org/advanced?q=air+algerie"
scraper_wikileaks(base_url, 21)