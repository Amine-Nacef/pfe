import requests
from bs4 import BeautifulSoup
import os
import requests
from bs4 import BeautifulSoup
import os
import json

dossier_images = "images_scrapées"
os.makedirs(dossier_images, exist_ok=True)

fichier_liens = os.path.join(dossier_images, "liens_extraits.txt")

png_links = []
jpg_links = []
autres_liens = []

def extraire_liens(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erreur lors de la récupération de la page {url}")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    if not table:
        print(f"Aucun tableau trouvé sur {url}")
        return
    
    for row in table.find_all("tr"):
        for col in row.find_all("td"):
            img_tag = col.find("a", href=True)
            if img_tag:
                lien = img_tag["href"]
                if lien.endswith(".png"):
                    png_links.append(lien)
                elif lien.endswith(".jpg") or lien.endswith(".jpeg"):
                    jpg_links.append(lien)
                else:
                    autres_liens.append(lien)

def telecharger_images(liste_liens, dossier, extension):
    for index, img_url in enumerate(liste_liens):
        if not img_url.startswith("http"):
            img_url = url.rstrip("/") + "/" + img_url.lstrip("/")

        print(f"Téléchargement de : {img_url}")
        try:
            img_data = requests.get(img_url).content
            img_name = os.path.join(dossier, f"image_{index}.{extension}")
            with open(img_name, "wb") as f:
                f.write(img_data)
        except Exception as e:
            print(f"Erreur lors du téléchargement de {img_url} : {e}")

for page in range(1, 4):
    url = f"https://buckets.grayhatwarfare.com/files?keywords=air%20algerie&page={page}"
    extraire_liens(url)

# Téléchargement des images PNG et JPG
telecharger_images(png_links, dossier_images, "png")
telecharger_images(jpg_links, dossier_images, "jpg")

# Sauvegarde des autres liens extraits
with open(fichier_liens, "w") as f:
    for lien in autres_liens:
        f.write(lien + "\n")

print(f"{len(png_links)} fichiers .png téléchargés avec succès dans '{dossier_images}' !")
print(f"{len(jpg_links)} fichiers .jpg téléchargés avec succès dans '{dossier_images}' !")
print(f"{len(autres_liens)} liens enregistrés dans '{fichier_liens}'")

# Export des données en JSON
donnees_export = {
    "png_links": png_links,
    "jpg_links": jpg_links,
    "autres_liens": autres_liens,
    "stats": {
        "total_images_png": len(png_links),
        "total_images_jpg": len(jpg_links),
        "total_liens": len(autres_liens)
    }
}

fichier_json = os.path.join(dossier_images, "export.json")
with open(fichier_json, "w", encoding="utf-8") as f:
    json.dump(donnees_export, f, ensure_ascii=False, indent=2)

print(f"\nFichier JSON d'export créé : {fichier_json}")

dossier_images = "images_scrapées"
os.makedirs(dossier_images, exist_ok=True)

fichier_liens = os.path.join(dossier_images, "liens_extraits.txt")

response = requests.get(url)
if response.status_code != 200:
    print("Erreur lors de la récupération de la page")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table")
if not table:
    print("Aucun tableau trouvé")
    exit()

png_links = []
jpg_links = []
autres_liens = []

for row in table.find_all("tr"):
    for col in row.find_all("td"):
        img_tag = col.find("a", href=True)
        if img_tag:
            lien = img_tag["href"]
            if lien.endswith(".png"):
                png_links.append(lien)
            elif lien.endswith(".jpg") or lien.endswith(".jpeg"):
                jpg_links.append(lien)
            else:
                autres_liens.append(lien)

# Fonction de téléchargement des images
def telecharger_images(liste_liens, dossier, extension):
    for index, img_url in enumerate(liste_liens):
        if not img_url.startswith("http"):
            img_url = url.rstrip("/") + "/" + img_url.lstrip("/")

        print(f"Téléchargement de : {img_url}")

        try:
            img_data = requests.get(img_url).content
            img_name = os.path.join(dossier, f"image_{index}.{extension}")

            with open(img_name, "wb") as f:
                f.write(img_data)

        except Exception as e:
            print(f"Erreur lors du téléchargement de {img_url} : {e}")

# Téléchargement des images PNG et JPG
telecharger_images(png_links, dossier_images, "png")
telecharger_images(jpg_links, dossier_images, "jpg")

# Sauvegarde des autres liens extraits
with open(fichier_liens, "w") as f:
    for lien in autres_liens:
        f.write(lien + "\n")

print(f"{len(png_links)} fichiers .png téléchargés avec succès dans '{dossier_images}' !")
print(f"{len(jpg_links)} fichiers .jpg téléchargés avec succès dans '{dossier_images}' !")
print(f"{len(autres_liens)} liens enregistrés dans '{fichier_liens}'")

# Export des données en JSON
donnees_export = {
    "png_links": png_links,
    "jpg_links": jpg_links,
    "autres_liens": autres_liens,
    "stats": {
        "total_images_png": len(png_links),
        "total_images_jpg": len(jpg_links),
        "total_liens": len(autres_liens)
    }
}

fichier_json = os.path.join(dossier_images, "export.json")
with open(fichier_json, "w", encoding="utf-8") as f:
    json.dump(donnees_export, f, ensure_ascii=False, indent=2)

print(f"\nFichier JSON d'export créé : {fichier_json}")
