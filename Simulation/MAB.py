import numpy as np
import matplotlib.pyplot as plt

# Import des simulations
from V2V import V2V
from V2I import V2I

# On définit l'environnement du bandit - Multi-Armed Bandit (MAB)
class BanditEnvironment:
    def __init__(self, k):
        # On définit le nombre de bras de la machine
        self.k = k 

        # On enregistre les choix bras de la machine
        # UCB
        self.V2V_UCB = 0
        self.V2I_UCB = 0

        # Epsilon-Greedy
        self.V2V_Epsilon = 0
        self.V2I_Epsilon = 0

    
    # On définit la fonction de récompense
    def get_reward(self):
        # on calcule le reward pour chaque bras de la machine

        # Calcul pour chaque itération
        # V2V
        V2V_simulation = V2V(800, 0.05)             # PARAMETRES A CHANGER + mettre de l'aleatoire pour varier les résultats
        # Attention pour V2I si on met une distance trop grande distance et un trafic trop élevé, le temps de calcul est bcp bcp trop long donc réduire le trafic
        # Si on met une distance petite et trafic faible il n'y aura pas de voiture -> ERROR

        # V2I
        V2I_simulation = V2I(800, 0.5)              # PARAMETRES A CHANGER + mettre de l'aleatoire pour varier les résultats

        # On retourne le temps de transmission pour chaque bras de la machine
        return [V2V_simulation.get_time_delay(), V2I_simulation.latence]
    

# ALGORITHME Epsilon-Greedy
# Va regarder la récompense moyenne de chaque bras de la machine et va choisir le bras avec la meilleure récompense
def epsilon_greedy(env, k, T):
    n = [0] * k            # nombre de fois que chaque bras de la machine a été tiré
    rewards = [0] * k      # récompenses cumulées pour chaque bras
    est_means = [0] * k    # récompense moyenne estimée pour chaque bras
    regrets = []
    for t in range(T):
        # On définit le paramètre epsilon pour l'exploration
        with np.errstate(divide='ignore'):
            epsilon = np.power(t, -1/3) * np.power(k * np.log(t), 1/3)

        # Exploration-Exploitation Strategy
        if np.random.rand() < epsilon:          # Lancé de la pièce pour choisir entre exploration et exploitation
            # EXPLORATION
            arm = np.random.randint(k)
        else:
            # EXPLOITATION
            arm = np.argmin(est_means)        # Choisir le bras avec le PLUS PETIT TEMPS DE TRANSMISSION

        # On calcule la récompense pour chaque bras de la machine
        rewards_iteration = env.get_reward()

        reward = rewards_iteration[arm]        # On récupère le temps de transmission pour le bras choisi
        n[arm] += 1                            # On incrémente le nombre de fois que le bras choisi a été tiré
        rewards[arm] += reward                 # On ajoute la récompense observée aux récompenses cumulées pour le bras choisi
        est_means[arm] = rewards[arm] / n[arm] # On met à jour la récompense moyenne estimée pour le bras choisi

        # On regarde la récompense optimale parmi les 2 bras de la machine
        # ici on prend le min car on veut minimiser le temps de transmission
        optimal_reward = np.min([env.get_reward()[i] for i in range(k)])
        
        # On calcule le regret de cette itération
        regret = abs(optimal_reward - reward)
        regrets.append(regret)
        
        # on enregistre les choix bras de la machine
        if arm == 0:
            env.V2V_Epsilon += 1
        else:
            env.V2I_Epsilon += 1

    # Retourner le cumul des regrets
    # return np.cumsum(regrets)

    # on retourne la liste des regrets pour chaque itération
    return regrets


# ALGORITHME UCB
# Va regarder la récompense moyenne de chaque bras de la machine et va choisir le bras avec la meilleure récompense
# en prenant en compte l'incertitude sur la récompense moyenne
def ucb(env, k, T):
    n = [0] * k             # Nombre de fois que chaque bras de la machine a été tiré
    rewards = [0] * k       # Récompenses cumulées pour chaque bras
    est_means = [0] * k     # Récompense moyenne estimée pour chaque bras
    regrets = []
    for t in range(T):
        if t < k:
            # Jouer chaque bras k fois pour initialiser les estimations et les valeurs UCB
            reward_iteration = env.get_reward()
            reward = reward_iteration[t]
            n[t] += 1
            rewards[t] += reward
            est_means[t] = rewards[t] / n[t]
            regrets.append(0)
        else:
            reward_iteration = env.get_reward()  # Obtenir la récompense pour chaque bras de la machine

            # Choisir le bras avec la plus grande valeur UCB
            ucb_values = [est_means[i] + np.sqrt(2*np.log(t) / n[i]) for i in range(k)]  # Calculer les valeurs UCB pour chaque bras
            arm = np.argmin(ucb_values)  # Sélectionner le bras avec la PLUS PETITE VALEUR UCB

            reward = reward_iteration[arm]  # Obtenir la récompense pour le bras choisi

            n[arm] += 1  # Incrémenter le nombre de fois que le bras choisi a été tiré
            rewards[arm] += reward  # Ajouter la récompense observée aux récompenses cumulées pour le bras choisi
            est_means[arm] = rewards[arm] / n[arm]  # Mettre à jour la récompense moyenne estimée pour le bras choisi

            optimal_reward = np.min([reward_iteration[i] for i in range(k)])  # Calculer la récompense optimale parmi les bras de la machine

            regret = abs(optimal_reward - reward)  # Calculer le regret pour le bras choisi
            regrets.append(regret)                 # Ajouter le regret à la liste des regrets

            # Enregistrer les choix de bras de la machine
            if arm == 0:
                env.V2V_UCB += 1
            else:
                env.V2I_UCB += 1

    # Retourner le cumul des regrets
    # return np.cumsum(regrets)

    # on retourne la liste des regrets pour chaque itération
    return regrets


# Define a function to run the bandit algorithm and plot the results
def run_bandit(env, k, T):
    # Run epsilon-greedy and UCB algorithms and store the cumulative regrets
    eps_regrets = epsilon_greedy(env, k, T)
    ucb_regrets = ucb(env, k, T)

    # On calcule le pourcentage de choix de bras de la machine
    # UCB
    env.V2V_UCB = env.V2V_UCB / T
    env.V2I_UCB = env.V2I_UCB / T

    # Epsilon-Greedy
    env.V2V_Epsilon = env.V2V_Epsilon / T
    env.V2I_Epsilon = env.V2I_Epsilon / T
    
    # Plot the cumulative regrets for both algorithms
    # Add a title to the plot indicating the current T and k values
    plt.figure()
    plt.title(f"T = {T} l'horizon (nb itération) -> Cumule des regrets (Time Delay)")
    plt.plot(np.cumsum(eps_regrets), label="Epsilon-Greedy")
    plt.plot(np.cumsum(ucb_regrets), label="UCB")
    plt.xlabel("Time")
    plt.ylabel("Cumulate Regret (Time Delay)")
    plt.legend()
    plt.show()


    # Regret par itération
    plt.figure()
    plt.title(f"T = {T} l'horizon (nb itération) -> Regret (Time Delay) par itération")
    # Tracé des croix pour Epsilon-Greedy
    plt.scatter(range(len(eps_regrets)), eps_regrets, label="Epsilon-Greedy", marker='x')
    # Tracé des croix pour UCB
    plt.scatter(range(len(ucb_regrets)), ucb_regrets, label="UCB", marker='x')
    plt.xlabel("Time")
    plt.ylabel("Regret (Time Delay)")
    plt.legend()
    # Ajout du texte en bas du graphique
    plt.figtext(0.5, 0.05, f"V2V_UCB: {env.V2V_UCB} V2I_UCB: {env.V2I_UCB} \n V2V_Epsilon: {env.V2V_Epsilon} V2I_Epsilon: {env.V2I_Epsilon}", wrap=True, horizontalalignment='center', fontsize=12)

    plt.show()



# Define the values of T and k for each environment to be tested
T_values = [1000, 2000, 30000]
k = 2

# Loop over the different environments and run the bandit algorithm for each
for i in range(len(T_values)):
    print(i)
    # Create a new bandit environment for the current k value
    env = BanditEnvironment(k)
    
    # Run the bandit algorithm and plot the results
    run_bandit(env, k, T_values[i])
