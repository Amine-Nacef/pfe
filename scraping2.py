import requests
from bs4 import BeautifulSoup
import os
import json

url = "https://search.wikileaks.org/?q=air+algerie"  # Remplace par l'URL cible

dossier_sortie = "scrap_result"
os.makedirs(dossier_sortie, exist_ok=True)

fichier_resultat = os.path.join(dossier_sortie, "resultats_scrap.txt")

response = requests.get(url)
if response.status_code != 200:
    print("Erreur lors de la récupération de la page")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

resultats = []

for result in soup.find_all("div", class_="result"):
    lien = result.find("a", href=True)
    date = result.find("div", class_="date")
    date_span = date.find("span") if date else None  # Récupérer <span> dans <div class="date">
    extrait = result.find("div", class_="excerpt")

    lien_text = lien["href"] if lien else "Aucun lien"
    date_text = date_span.text.strip() if date_span else "Aucune date"  # Extraire le texte du <span>
    extrait_text = extrait.text.strip() if extrait else "Aucun extrait"

    resultats.append((lien_text, date_text, extrait_text))

print("\n=== Résultats Scrappés ===")
for lien, date, extrait in resultats:
    print(f"Lien : {lien}")
    print(f"Date : {date}")
    print(f"Extrait : {extrait}")
    print("-" * 50)

with open(fichier_resultat, "w") as f:
    for lien, date, extrait in resultats:
        f.write(f"Lien : {lien}\n")
        f.write(f"Date : {date}\n")
        f.write(f"Extrait : {extrait}\n")
        f.write("-" * 50 + "\n")

print(f"\n{len(resultats)} éléments enregistrés dans '{fichier_resultat}'")

# Génération du fichier JSON
resultats_json = [{"lien": lien, "date": date, "extrait": extrait} for lien, date, extrait in resultats]

fichier_json = os.path.join(dossier_sortie, "donnees.json")
with open(fichier_json, "w", encoding="utf-8") as f:
    json.dump(resultats_json, f, ensure_ascii=False, indent=2)

print(f"\nFichier JSON généré : {fichier_json}")
