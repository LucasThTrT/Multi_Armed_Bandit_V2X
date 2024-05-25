# This communication V2V is based on VANETs (Vehicular Ad Hoc Networks)
# The Quality of Service (QoS) will depend on the distance between the transmitter and the receiver and the traffic density in the area

import random
import time


class V2V:
    def __init__(self, distance, traffic_density):
        # Parameters

        # Scenario
        self.distance = distance                                                                            # Distance between the transmitter and the receiver in meters
        self.traffic_density = traffic_density                                                              # Traffic density in the area in percentage

        # To Define
        self.max_range = 1000                                                                               # Max propagation Range in meters
        self.facteur_attenuation = 2                                                                        # Facteur d'atténuation de la communication = 2 sans obstacle
        self.distance_de_reference = 100
        self.Probabilite_de_perte_de_paquet_de_reference = 0.1     

        # SIMULATION
        Alert_Packet_size = 100*8 # Bits -> BSM (Basic Safety Message)
        debits = 5                # Mbit/s -> DSRC (Dedicated Short Range Communication)

        CW = 15                                                                                             # Contention Window
        time_slot = 0.00001                                                                                 # Time slot in seconds

        # Time 
        self.emmission_time = Alert_Packet_size/debits                                                      # Emission time in seconds                            
        self.retransmission_delay = CW*time_slot                                                            # Retransmission delay in seconds      
        self.computing_time = 0.0005 #0.00005                                                               # Computing time in seconds for the "router" vehicule = SIFS (Short Interframe Space)
        # L'intervalle inter-trame court (short interframe space ou SIFS en anglais), est le temps (en microsecondes) nécessaire à une interface sans-fil pour traiter une trame et répondre avec une trame de réponse.

        # Admitted
        self.propagation_speed = 3 * 10 ** 8                                                                # Propagation speed in meters per second (Propagation speed in the air of an electromagnetic wave (WIFI))
        self.vehicle_length = 4.2                                                                           # Mean vehicle length in meters (in France)
        self.minimal_space_between_vehicles = 1                                                             # Minimal space between vehicles in meters (in France)

        # For the simulation
        self.best_transmission = [False, 0, 0, []]
        self.time_of_simulation = 0

        self.number_of_vehicles = int((self.distance // (self.vehicle_length + self.minimal_space_between_vehicles)) * self.traffic_density)
        # print("Number of vehicles: ", self.number_of_vehicles)

        # Estimation of the space between vehicles
        self.space_between_vehicles = round((self.distance - (self.number_of_vehicles * (self.vehicle_length))) / self.number_of_vehicles,1)
        # print("Space between vehicles: ", self.space_between_vehicles)

        # print("Place prise par les véhicules: ", self.number_of_vehicles * (self.vehicle_length + self.space_between_vehicles))
        self.run()


    # Simulation of V2Vehicle communication
    def V2Vehicle_simulation(self, actual_vehicle, next_vehicle):  
            transmission_validated = 0
            packet_lost = 0

            # We calculate the distance of communication
            distance_of_communication = (next_vehicle - actual_vehicle) * (self.space_between_vehicles + self.vehicle_length) - self.vehicle_length

            if distance_of_communication > self.max_range:  # If the distance is bigger than the max range
                return transmission_validated, 0, 0               # The communication is not possible
            
            else:
                # We calculate the time delay & the number of packets lost
                # If the next vehicle is the last one 
                if next_vehicle == self.number_of_vehicles: 
                    time_delay_for_compute = 0

                # If the next vehicle is not the last one -> we add the computing time of the vehicule calculation 
                else:
                    time_delay_for_compute = self.computing_time

                # We calculate the time delay & the number of packets lost
                time_delay = (self.space_between_vehicles / self.propagation_speed) + self.computing_time  # Time delay if no packet is lost
                
                 # if we lose the packet -> we retransmit the packet and we add the retransmission delay
                while (random.random() > (1-(1-self.Probabilite_de_perte_de_paquet_de_reference)**((distance_of_communication/self.distance_de_reference)**self.facteur_attenuation))):
                    packet_lost += 1
                    time_delay += (self.space_between_vehicles / self.propagation_speed) + self.retransmission_delay

                transmission_validated = 1
                return transmission_validated, time_delay, packet_lost


    # Simulation of V2Vehicle communication
    def V2V_simulation(self, transmission_validated, time_delay, packet_lost,actual_vehicle, n_jump, chemin_actuel=[]):
        # On va tester toutes les possibilités de saut
        # On vérifie si on est arrivé à la destination
        if actual_vehicle == n_jump:

            # On compare avec la meilleure transmission en mémoire
            # Si la transmission actuelle est meilleure, on la garde
            # ou si la meilleure transmission n'est pas encore définie
            if ((transmission_validated) and (time_delay < self.best_transmission[1])) or (not self.best_transmission[0]):
                self.best_transmission = [transmission_validated, time_delay, packet_lost, chemin_actuel + [actual_vehicle]]

            # TEST
            #print("++++++++++++++++++++++++++++++++++++++++++++++")
            #print(chemin_actuel + [actual_vehicle])
            #print("Transmission validated: ", transmission_validated)
            #print("Time delay: ", time_delay)
            #print("Packet lost: ", packet_lost)
            #print("++++++++++++++++++++++++++++++++++++++++++++++")
            #print("Best transmission: ", self.best_transmission)

            return 

        # Sinon, on explore les deux options : aller directement à la prochaine étape ou passer par un point intermédiaire
        for i in range(actual_vehicle + 1, n_jump + 1):

            # Simulation de la communication V2V
            new_transmission_validated, new_time_delay, new_packet_lost = self.V2Vehicle_simulation(actual_vehicle, i)

            # Si la communication n'est pas possible, on arrête
            if not new_transmission_validated:
                # On met la transmission à False pour avoir un best_transmission[0] = False donc on ne garde pas ce chemin
                transmission_validated = False
                # print("Transmission not validated ->> ", chemin_actuel + [actual_vehicle] + [i])
            
            time_delay += new_time_delay
            packet_lost += new_packet_lost

            # Ajouter l'étape actuelle au chemin
            # jump vers i
            chemin_actuel.append(actual_vehicle)

            # Explorer le chemin directement à l'étape suivante
            self.V2V_simulation(transmission_validated, time_delay, packet_lost, i, n_jump, chemin_actuel)

            # Retirer l'étape actuelle pour explorer d'autres chemins
            # jump sans passer par i
            chemin_actuel.pop()

            # On retire le temps de communication et le nombre de paquets perdus
            time_delay -= new_time_delay
            packet_lost -= new_packet_lost
            # si transmission_validated = False, on arrête la simulation de ce chemin
            # Car si avec un saut n est pas possible, alors avec n+1 sauts non plus !
            
    
    def run(self):
        # On commence la simulation
        # Time start
        start = time.time()
        self.V2V_simulation(True,0, 0, 0, self.number_of_vehicles, [])
        self.time_of_simulation = time.time() - start

    def get_time_delay(self):
        return self.best_transmission[1]
    

# Exemple d'utilisation 

# distance = 1050
# traffic_density = 0.05
# v2v = V2V(distance, traffic_density)
# print(v2v.best_transmission)
# print("Distance: ", v2v.distance)
# print("Number of vehicles: ", v2v.number_of_vehicles)
# print("Space between vehicles: ", v2v.space_between_vehicles)
# print("Place prise par les véhicules: ", v2v.number_of_vehicles * (v2v.vehicle_length + v2v.space_between_vehicles))