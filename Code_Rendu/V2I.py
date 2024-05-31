# This communication V2I is based on cellular networks
# The Quality of Service (QoS) will depend on the distance between the transmitter and the receiver and the network load

import random
import time
import math

class V2I:
    def __init__(self, distance, network_load):
        # Parameters

        # Scenario
        self.distance = distance
        self.distance_infra = 400 #distance entre le véhicule et l'infrastructure moyenne en zone urbaine en France
        self.network_load = network_load                                                                     # Network load in percentage

        # To Define
        self.max_range = 10000000                                                                               # Max propagation Range in meters
        self.facteur_attenuation = 2                                                                        # Facteur d'atténuation de la communication = 2 sans obstacle
        self.distance_de_reference = 100
        self.Probabilite_de_perte_de_paquet_de_reference = 0.1

        # SIMULATION
        self.Alert_Packet_size = 1000 # Bits -> DENM (Decentralized Environmental Notification Message)
        self.debit = 50                # Mbit/s -> cellular networks (traitement des données radio)
        self.debit_UE = 20             # Mbit/s -> débit emiision des données radio

        # Time
        self.emmission_time = self.Alert_Packet_size/self.debit                                                      # Emission time in seconds

        # Admitted
        self.propagation_speed = 3 * 10 ** 8                                                                # Propagation speed in meters per second (Propagation speed in the air of an electromagnetic wave (WIFI))

        # For the simulation
        self.time_of_simulation = 0
        self.latence = 0

        self.run()

    def calculate_latency_V2I(self):
        """
        Calcule la latence de transmission d'un message d'une infrastructure vers un véhicule en fonction de la distance,
        de la taille du message et de la charge réseau.

        Returns:
        float: La latence de transmission en secondes.
        """
        #Temps de traitement des données côté users
        processing_time_UE = self.Alert_Packet_size / (self.debit_UE*10**6)  # 20 Mbps de débit de traitement pour l'UE

        # Temps de traitement des données côté infrastructure
        processing_time_infra = self.Alert_Packet_size / (self.debit*10**6)  # 50 Mbps de capacité de traitement pour l'infrastructure

        # Temps de propagation du signal
        propagation_time = self.distance / self.propagation_speed

        # Temps de transmission du message  (APPROXIMATION)
        a = 0.0001   
        b = 0.00001
        c = 0.0001
        d = 0.02
        transmission_time =  a * math.exp(b * (self.distance_infra + self.distance)) + c * math.log(d * self.distance + 1)
        ## cete formule est une approximation de la formule de transmission du message en fonction de la distance, lorsque la distance est courte les délais sont très faibles car même gnb..
        ## pour des distances plus longues, les délais augmentent exponentiellement, car on doit passer par le coeur de réseau


        # Temps d'attente dans la file d'attente (dépend de la charge réseau)
        queue_delay = (self.network_load) * (2*processing_time_infra + propagation_time + transmission_time + 2*processing_time_UE)

        # Calcul de la latence totale
        self.latence = 2*processing_time_infra + 2*processing_time_UE + propagation_time + transmission_time + queue_delay

        return

    def run(self):
        # On commence la simulation
        # Time start
        start = time.time()
        # Appel de la méthode calculate_latency_V2I pour récupérer la latence
        self.calculate_latency_V2I()
        self.time_of_simulation = time.time() - start