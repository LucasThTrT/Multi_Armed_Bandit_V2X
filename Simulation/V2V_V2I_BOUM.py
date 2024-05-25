import csv
from V2V import V2V
from V2I import V2I

Pas_distance = 200

for i in range(1, 10):
    #V2V(distance, traffic_density)
    V2V_simulation = V2V(Pas_distance * i, 0.05)
    #V2I(distance, traffic_load_infra)
    V2I_simulation = V2I(Pas_distance * i, 0.5)
    print("Distance: ", Pas_distance * i)
    print("Traffic density: ", 0.05)
    print("V2V_simulation: ", V2V_simulation.best_transmission)
    print("final latency: ", V2V_simulation.best_transmission[1])
    print("----------------------")
    print("V2I_simulation: ")
    distance = Pas_distance * i,
    print("final latency ", V2I_simulation.latence)
    print("---------------------------------------------------")
    if V2V_simulation.best_transmission[1] < V2I_simulation.latence:
        print("V2V has best latency for distance ", Pas_distance * i, "m")
    else:
        print("V2I has best latency for distance ", Pas_distance * i, "m")
    print("---------------------------------------------------")


    # Save metrics to CSV file
    filename = "simu_metrics.csv"
    header = []
    data = [Pas_distance*i, V2I_simulation.latence, V2V_simulation.best_transmission[1]]

    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerow(data)