import network   # handles connecting to WiFi
import urequests # handles making and servicing network requests
import requests
from machine import Pin
import json
import utime

# Connect to the mobile hotspot
def connect_to_hotspot(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        pass
    print("Connected to the hotspot:", ssid)

# Fill in your phone's hotspot name (SSID) and password here:
hotspot_ssid = 'OPPO A54s'
hotspot_password = 't6rdwgek'

# Connect to the mobile hotspot
connect_to_hotspot(hotspot_ssid, hotspot_password)

# Example 1. Make a GET request for google.com and print HTML
# Print the html content from google.com
print("1. Querying google.com:")
r = urequests.get("http://www.google.com")
print(r.content)
r.close()

# Example 2. urequests can also handle basic json support! Let's get the current time from a server
print("\n\n2. Querying the current GMT+1 time:")
r = urequests.get("http://date.jsontest.com") # Server that returns the current GMT+0 time.
print(r.json())

WEBHOOK_URL = "https://discord.com/api/webhooks/1240687411650887700/gO5tXiFL2_V30PtE56_oQs3j81_bBIs-_w7Kqap6T-RDE37ASO-b_V0gwvDuwRKAdPXd"

def send_message(message):
    data = {
        "content": "GOAL !!!!"
    }
    try:
        response = requests.post(WEBHOOK_URL, data=json.dumps(data), headers={"Content-Type": "application/json"})
        if response.status_code != 204:
            error_message = "Erreur {} lors de l'envoi du message: {}".format(response.status_code, response.text)
            print(error_message)  # Afficher l'erreur dans la console
            raise ValueError(error_message)  # Lever une exception avec le message d'erreur détaillé
    except Exception as e:
        print("Une erreur s'est produite lors de l'envoi du message:", e)


# Définition du pin du bouton poussoir
PIN_BOUTON = 16

# Initialisation du pin du bouton en tant qu'entrée avec une résistance de pull-up interne
bouton = Pin(PIN_BOUTON, Pin.IN, Pin.PULL_UP)

# Variables pour suivre l'état précédent du bouton et le moment où il a été pressé pour la première fois
etat_precedent = 1
moment_appui_initial = 0
moment_dernier_buts = 0

CONSTANTE_DISTANCE_M = 0.1  # Constante de distance parcourue en centimètres
DELAI_ENTRE_BUTS_MS = 1000  # Délai entre chaque but en millisecondes

print("En attente d'événements sur le bouton...")

# Compteur pour le nombre de buts marqués
compteur_buts = 0

# Boucle principale
while True:
    etat_actuel = bouton.value()  # Lire l'état actuel du bouton

    # Vérifier s'il y a eu un changement d'état du bouton
    if etat_actuel != etat_precedent:
        if etat_actuel == 0:  # Si le bouton est enfoncé
            print("Bouton enfoncé")
            moment_appui_initial = utime.ticks_ms()  # Enregistrer le moment où le bouton a été pressé
        else:  # Si le bouton est relâché
            print("Bouton relâché")
            if moment_appui_initial != 0:  # Si le bouton a été pressé au moins une fois
                moment_relachement = utime.ticks_ms()  # Enregistrer le moment où le bouton est relâché
                duree_ecoulee_ms = utime.ticks_diff(moment_relachement, moment_appui_initial)  # Calculer la durée écoulée en millisecondes
                duree_ecoulee_s = duree_ecoulee_ms / 1000  # Convertir la durée en secondes
                print("Durée écoulée: {:.3f} secondes".format(duree_ecoulee_s))  # Affichage en secondes avec précision millisecondes
                
                # Calcul de la vitesse comme si le bouton était une balle passant dans un but
                distance_goal_m = 0.1  # Distance entre le début et la fin du "goal" en mètres
                vitesse_ms = distance_goal_m / duree_ecoulee_s  # Calcul de la vitesse en m/s
                vitesse_kmh = vitesse_ms * 3.6  # Conversion de m/s en km/h
                print("Vitesse: {:.2f} m/s ({:.2f} km/h)".format(vitesse_ms, vitesse_kmh))  # Affichage de la vitesse
                
                moment_appui_initial = 0  # Réinitialiser le moment de l'appui initial
                
                # Vérifier si le délai entre ce but et le dernier but est suffisamment long
                if utime.ticks_diff(moment_relachement, moment_dernier_buts) > DELAI_ENTRE_BUTS_MS:
                    # Ajouter un but
                    compteur_buts += 1
                    print("But marqué ! Total: {}".format(compteur_buts))
                    moment_dernier_buts = moment_relachement  # Mettre à jour le moment du dernier but
                    #send_message("But marqué ! Vitesse: {:.2f} m/s ({:.2f} km/h). Total: {}".format(vitesse_ms, vitesse_kmh, compteur_buts))                
                else:
                    print("GAMMELLE ! But annulé.")
                    compteur_buts -= 1
                    #send_message("GAMMELLE ! But annulé.")

        etat_precedent = etat_actuel  # Mettre à jour l'état précédent

