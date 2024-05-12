from V2V import V2V

# Simulation of V2V communication
#V2V(distance, traffic_density)
for i in range(5, 13):
    V2V_simulation = V2V(200*i, 0.05)
    print("Distance: ", 200*i)
    print("Traffic density: ", 0.05)
    print("V2V_simulation: ", V2V_simulation.best_transmission)
    print("Time of simulation: ", V2V_simulation.time_of_simulation)
    print("---------------------------------------------------")