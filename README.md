# Projet MAB

# Simulation V2X
Ce code va simuler l'envoi d'alertes entre un Véhicule (V) et un utilisateur en danger (X) dans des conditions différentes.

La communication va se faire de 2 manières différentes :
    - V2V : L'alerte est envoyée par la voie hertzienne directement entre le Véhicule et l'utilisateur Vulenerable (V).
    - V2I : L'alerte passe d'abord par l'infrastructure (I) 5G pour être ensuite envoyée à l'utilisateur.

Cette simulation va permettre de relever les QoS de ces 2 manières pour ensuite faire de l'apprentissage à notre MAB.
On relève comme QoS :
    - La latence -> Semble être l'élément le plus important par intuition.
    - La fiabilité.
    - On pourrait aussi prendre en compte l'état du réseau, mais pour le moment nous restons sur 2 facteurs.
