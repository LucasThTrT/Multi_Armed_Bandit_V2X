from V2V import V2V

Pas_distance = 200

#Modélisation V2I simpliste
# le coefficient X dans la formule t = X*D pour la latence dans un réseau 5G sans congestion est d'environ 0,064 nanosecondes par mètre.
# il est important de noter que cette valeur ne tient compte que du temps de traitement des données et du temps de propagation des ondes électromagnétiques,
# et qu'elle ne tient pas compte des autres facteurs  comme la congestion du réseau.


# def calculate_latency_V2I(i):
    # return 0.064*(10,5**-6) * i * Pas_distance

# Simulation of V2V communication
#V2V(distance, traffic_density)
for i in range(15,30):
    V2V_simulation = V2V(Pas_distance * i, 0.01)
    print("Distance: ", Pas_distance * i)
    print("Traffic density: ", 0.05)
    print("V2V_simulation: ", V2V_simulation.best_transmission)
    print("final latency: ", V2V_simulation.best_transmission)
    print("----------------------")
    print("V2I_simulation: ")
    # print("final latency ", calculate_latency_V2I(i))
    print("---------------------------------------------------")
    # if V2V_simulation.best_transmission[1] < calculate_latency_V2I(i):
    #     print("V2V has best latency for distance ", Pas_distance * i, "m")
    # else:
    #     print("V2I has best latency for distance ", Pas_distance * i, "m")
    print("---------------------------------------------------")

