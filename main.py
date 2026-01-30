import requests
import csv
import os
from datetime import datetime

URL_PARKING = "https://portail-api-data.montpellier3m.fr/offstreetparking?limit=1000"
URL_BIKE = "https://portail-api-data.montpellier3m.fr/bikestation?limit=1000"

FICHIER_CSV = "historique_parkings.csv"

def get_data(url):
    """Récupère les données JSON depuis l'API"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Erreur de connexion : {e}")
    return []

def sauvegarder_csv(parkings, velos):
    """Sauvegarde les données dans un fichier CSV compatible Excel (point-virgule)"""
    file_exists = os.path.isfile(FICHIER_CSV)
    
    with open(FICHIER_CSV, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        
        if not file_exists:
            writer.writerow(['Date', 'Heure', 'Type', 'Nom', 'Places_Libres', 'Places_Totales'])
        
        maintenant = datetime.now()
        date_str = maintenant.strftime("%Y-%m-%d")
        heure_str = maintenant.strftime("%H:%M")

        for p in parkings:
            nom = p.get("name", {}).get("value", "Inconnu")
            libres = p.get("availableSpotNumber", {}).get("value", 0)
            total = p.get("totalSpotNumber", {}).get("value", 0)
            writer.writerow([date_str, heure_str, 'Voiture', nom, libres, total])

        for v in velos:
            adresse = v.get("address", {}).get("value", {}).get("streetAddress", "Inconnu")
            libres = v.get("freeSlotNumber", {}).get("value", 0)
            total = v.get("totalSlotNumber", {}).get("value", 0)
            writer.writerow([date_str, heure_str, 'Velo', adresse, libres, total])

if __name__ == "__main__":
    print("Récupération des données en cours...")
    data_p = get_data(URL_PARKING)
    data_v = get_data(URL_BIKE)

    if data_p or data_v:
        sauvegarder_csv(data_p, data_v)
        print("Succès : Données ajoutées au CSV.")
    else:

        print("Erreur : Impossible de récupérer les données.")

