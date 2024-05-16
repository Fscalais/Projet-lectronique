import machine
import time

# Définir les broches GPIO à surveiller
PIN_18 = 18
PIN_16 = 16

# Configurer les broches GPIO en tant que broches d'entrée
pin_18 = machine.Pin(PIN_18, machine.Pin.IN)
pin_16 = machine.Pin(PIN_16, machine.Pin.IN)

# Variables pour stocker les états précédents des broches
prev_state_18 = pin_18.value()
prev_state_16 = pin_16.value()

# Boucle pour détecter les changements d'état des broches GPIO
while True:
    # Lire l'état actuel des broches
    current_state_18 = pin_18.value()
    current_state_16 = pin_16.value()
    
    # Vérifier s'il y a un changement d'état sur la broche 18
    if current_state_18 != prev_state_18:
        print("Changement d'état sur la broche 18 : ", current_state_18)
        prev_state_18 = current_state_18
    
    # Vérifier s'il y a un changement d'état sur la broche 16
    if current_state_16 != prev_state_16:
        print("Changement d'état sur la broche 16 : ", current_state_16)
        prev_state_16 = current_state_16
    
    time.sleep(0.1)  # Attendre un court instant avant de vérifier à nouveau les broches