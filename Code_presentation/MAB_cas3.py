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
    def get_reward_1(self):
        # ETUDE 1 & 2
        # On fait peut varier l'environnement on reste dans des conditions "loin" ou "proche" de l'utilisateur

        # ETUDE 3
        # On commence pendant la moitier de l'itération dans un environnement "loin" et l'autre moitié dans un environnement "prêt"
        # Pour faire apparaitre le temps de transition entre 2 politiques et les limites à cause de la moyenne
        # et voir quel algorithme est s'adapte le mieux aux changements d'environnement

        # ETUDE 4
        # On fait varier complétement alétatoirement les paramètres de la simulation
        # Comme si on émettait que des messages d'alerte très rarement (donc entre 2 envois on change facilement d'environnement)
        # Illustre la nullité du MAB dans ce cas

        # REMARQUE 
        # Je fais varier tout au long la charge et le trafic de manière aléatoire.
        # On pourra aussi étudier cette impact de fort changement après.


        # Distance de la communication qu'on fait varier
        distance = np.random.randint(1100, 1300) # loi uniforme entre 1000 et 3000 qui retourne un entier

        # Trafic qu'on fait varier
        traffic = np.random.uniform(0, 0.005) # loi uniforme entre 0 et 0.10
        
        # Charge du réseau V2I qu'on fait varier
        charge = np.random.uniform(0, 1) # loi uniforme entre 0 et 1

        # on calcule le reward pour chaque bras de la machine

        # Calcul pour chaque itération
        # V2V
        V2V_simulation = V2V(distance, 0.05)             # PARAMETRES A CHANGER + mettre de l'aleatoire pour varier les résultats
        # Attention pour V2I si on met une distance trop grande distance et un trafic trop élevé, le temps de calcul est bcp bcp trop long donc réduire le trafic
        # Si on met une distance petite et trafic faible il n'y aura pas de voiture -> ERROR

        # V2I
        V2I_simulation = V2I(distance, 0.5)              # PARAMETRES A CHANGER + mettre de l'aleatoire pour varier les résultats

        # On retourne le temps de transmission pour chaque bras de la machine
        return [V2V_simulation.get_time_delay(), V2I_simulation.latence]
    
    def get_reward_2(self):
        # ETUDE 1 & 2
        # On fait peut varier l'environnement on reste dans des conditions "loin" ou "proche" de l'utilisateur

        # ETUDE 3
        # On commence pendant la moitier de l'itération dans un environnement "loin" et l'autre moitié dans un environnement "prêt"
        # Pour faire apparaitre le temps de transition entre 2 politiques et les limites à cause de la moyenne
        # et voir quel algorithme est s'adapte le mieux aux changements d'environnement

        # ETUDE 4
        # On fait varier complétement alétatoirement les paramètres de la simulation
        # Comme si on émettait que des messages d'alerte très rarement (donc entre 2 envois on change facilement d'environnement)
        # Illustre la nullité du MAB dans ce cas

        # REMARQUE 
        # Je fais varier tout au long la charge et le trafic de manière aléatoire.
        # On pourra aussi étudier cette impact de fort changement après.


        # Distance de la communication qu'on fait varier
        distance = np.random.randint(200, 500) # loi uniforme entre 1000 et 3000 qui retourne un entier

        # Trafic qu'on fait varier
        traffic = np.random.uniform(0, 0.005) # loi uniforme entre 0 et 0.10
        
        # Charge du réseau V2I qu'on fait varier
        charge = np.random.uniform(0, 1) # loi uniforme entre 0 et 1

        # on calcule le reward pour chaque bras de la machine

        # Calcul pour chaque itération
        # V2V
        V2V_simulation = V2V(distance, 0.05)             # PARAMETRES A CHANGER + mettre de l'aleatoire pour varier les résultats
        # Attention pour V2I si on met une distance trop grande distance et un trafic trop élevé, le temps de calcul est bcp bcp trop long donc réduire le trafic
        # Si on met une distance petite et trafic faible il n'y aura pas de voiture -> ERROR

        # V2I
        V2I_simulation = V2I(distance, 0.5)              # PARAMETRES A CHANGER + mettre de l'aleatoire pour varier les résultats

        # On retourne le temps de transmission pour chaque bras de la machine
        return [V2V_simulation.get_time_delay(), V2I_simulation.latence]
    

# ALGORITHME Epsilon-Greedy
# Va regarder la récompense moyenne de chaque bras de la machine et va choisir le bras avec la meilleure récompense
def epsilon_greedy(env, k, T):
    n = [0] * k            # nombre de fois que chaque bras de la machine a été tiré
    rewards = [0] * k      # récompenses cumulées pour chaque bras
    est_means = [0] * k    # récompense moyenne estimée pour chaque bras
    regrets = []
    total = 0
    for t in range(T):
        if t < T*0.10 :
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
            rewards_iteration = env.get_reward_1()
            # total = total + (rewards_iteration[0]+rewards_iteration[1])/2
            reward = rewards_iteration[arm]        # On récupère le temps de transmission pour le bras choisi
            n[arm] += 1                            # On incrémente le nombre de fois que le bras choisi a été tiré
            rewards[arm] += reward                 # On ajoute la récompense observée aux récompenses cumulées pour le bras choisi
            est_means[arm] = rewards[arm] / n[arm] # On met à jour la récompense moyenne estimée pour le bras choisi
    
            # On regarde la récompense optimale parmi les 2 bras de la machine
            # ici on prend le min car on veut minimiser le temps de transmission
            optimal_reward = np.min([rewards_iteration[i] for i in range(k)])
            
            # On calcule le regret de cette itération
            regret = abs(optimal_reward - reward)
            regrets.append(regret)
            
            # on enregistre les choix bras de la machine
            if arm == 0:
                env.V2V_Epsilon += 1
            else:
                env.V2I_Epsilon += 1
        #temps_moyen = total/T
        #print(temps_moyen)
        # Retourner le cumul des regrets
        # return np.cumsum(regrets)

        else:
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
            rewards_iteration = env.get_reward_2()
            # total = total + (rewards_iteration[0]+rewards_iteration[1])/2
            reward = rewards_iteration[arm]        # On récupère le temps de transmission pour le bras choisi
            n[arm] += 1                            # On incrémente le nombre de fois que le bras choisi a été tiré
            rewards[arm] += reward                 # On ajoute la récompense observée aux récompenses cumulées pour le bras choisi
            est_means[arm] = rewards[arm] / n[arm] # On met à jour la récompense moyenne estimée pour le bras choisi
    
            # On regarde la récompense optimale parmi les 2 bras de la machine
            # ici on prend le min car on veut minimiser le temps de transmission
            optimal_reward = np.min([rewards_iteration[i] for i in range(k)])
            
            # On calcule le regret de cette itération
            regret = abs(optimal_reward - reward)
            regrets.append(regret)
            
            # on enregistre les choix bras de la machine
            if arm == 0:
                env.V2V_Epsilon += 1
            else:
                env.V2I_Epsilon += 1
    # on retourne la liste des regrets pour chaque itération
    return regrets


# ALGORITHME UCB
# Va regarder la récompense moyenne de chaque bras de la machine et va choisir le bras avec la meilleure récompense
# en prenant en compte l'incertitude sur la récompense moyenne
def ucb(env, k, T):
    n = [0] * k             # Nombre de fois que chaque bras de la machine a été tiré
    tps_moyen = 0.0009214     # temps moyen 
    rewards = [0] * k       # Récompenses cumulées pour chaque bras
    est_means = [0] * k     # Récompense moyenne estimée pour chaque bras
    regrets = []
    for t in range(T):
        if t < 0.10*T :
            if t < k:
                # Jouer chaque bras k fois pour initialiser les estimations et les valeurs UCB
                reward_iteration = env.get_reward_1()
                reward = reward_iteration[t]/tps_moyen
                n[t] += 1
                rewards[t] += reward
                est_means[t] = rewards[t] / n[t]
                regrets.append(0)
            else:
                reward_iteration = env.get_reward_1()  # Obtenir la récompense pour chaque bras de la machine
                # Choisir le bras avec la plus grande valeur UCB
                ucb_values = [est_means[i] for i in range(k)]  # Calculer les valeurs UCB pour chaque brass
                # print(ucb_values)
                arm = np.argmin(ucb_values)  # Sélectionner le bras avec la PLUS PETITE VALEUR UCB
    
                reward = reward_iteration[arm]/tps_moyen  # Obtenir la récompense pour le bras choisi
    
                n[arm] += 1  # Incrémenter le nombre de fois que le bras choisi a été tiré
                rewards[arm] += reward  # Ajouter la récompense observée aux récompenses cumulées pour le bras choisi
                est_means[arm] = rewards[arm] / n[arm]  # Mettre à jour la récompense moyenne estimée pour le bras choisi
    
                optimal_reward = np.min([reward_iteration[i] for i in range(k)])  # Calculer la récompense optimale parmi les bras de la machine
    
                regret = abs(optimal_reward - reward_iteration[arm])  # Calculer le regret pour le bras choisi
                regrets.append(regret)                 # Ajouter le regret à la liste des regrets
    
                # Enregistrer les choix de bras de la machine
                if arm == 0:
                    env.V2V_UCB += 1
                else:
                    env.V2I_UCB += 1
    
        else:
            if t < k:
                # Jouer chaque bras k fois pour initialiser les estimations et les valeurs UCB
                reward_iteration = env.get_reward_2()
                reward = reward_iteration[t]/tps_moyen
                n[t] += 1
                rewards[t] += reward
                est_means[t] = rewards[t] / n[t]
                regrets.append(0)
            else:
                reward_iteration = env.get_reward_2()  # Obtenir la récompense pour chaque bras de la machine
                # Choisir le bras avec la plus grande valeur UCB
                ucb_values = [est_means[i] for i in range(k)]  # Calculer les valeurs UCB pour chaque brass
                #print(ucb_values)
                arm = np.argmin(ucb_values)  # Sélectionner le bras avec la PLUS PETITE VALEUR UCB
    
                reward = reward_iteration[arm]/tps_moyen  # Obtenir la récompense pour le bras choisi
    
                n[arm] += 1  # Incrémenter le nombre de fois que le bras choisi a été tiré
                rewards[arm] += reward  # Ajouter la récompense observée aux récompenses cumulées pour le bras choisi
                est_means[arm] = rewards[arm] / n[arm]  # Mettre à jour la récompense moyenne estimée pour le bras choisi
    
                optimal_reward = np.min([reward_iteration[i] for i in range(k)])  # Calculer la récompense optimale parmi les bras de la machine
    
                regret = abs(optimal_reward - reward_iteration[arm])  # Calculer le regret pour le bras choisi
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
    print("ok regret EPS")
    ucb_regrets = ucb(env, k, T)
    print("ok regret UCB")
    # On calcule le pourcentage de choix de bras de la machine
    # UCB
    pourcentage_V2V_UCB = env.V2V_UCB / T

    pourcentage_V2I_UCB = env.V2I_UCB / T
    print("pourcentage UCB")
    # Epsilon-Greedy
    pourcentage_V2V_Epsilon = env.V2V_Epsilon / T
    pourcentage_V2I_Epsilon = env.V2I_Epsilon / T
    print("pourcentage EPS")
    # Plot the cumulative regrets for both algorithms
    # Add a title to the plot indicating the current T and k values
    plt.figure(1)
    plt.title(f"T = {T} l'horizon (nb itération) -> Cumule des regrets (Time Delay)")
    plt.plot(np.cumsum(eps_regrets), label="Epsilon-Greedy")
    plt.plot(np.cumsum(ucb_regrets), label="UCB")
    plt.xlabel("Time")
    plt.ylabel("Cumulate Regret (Time Delay)")
    plt.legend()
    plt.show()
    
    print("plot finit")

    # # Regret par itération
    # plt.figure(2)
    # plt.title(f"T = {T} l'horizon (nb itération) -> Regret (Time Delay) par itération")
    # # Tracé des croix pour Epsilon-Greedy
    # plt.scatter(range(len(eps_regrets)), eps_regrets, label="Epsilon-Greedy", marker='x')
    # # Tracé des croix pour UCB
    # plt.scatter(range(len(ucb_regrets)), ucb_regrets, label="UCB", marker='x')
    # plt.xlabel("Time")
    # plt.ylabel("Regret (Time Delay)")
    # plt.legend()
    # # Ajout du texte en bas du graphique
    # plt.figtext(0.5, 0.05, f"V2V_UCB: {env.V2V_UCB} V2I_UCB: {env.V2I_UCB} \n V2V_Epsilon: {env.V2V_Epsilon} V2I_Epsilon: {env.V2I_Epsilon}", wrap=True, horizontalalignment='center', fontsize=12)
    # 
    # plt.show()
    # Données
    algorithms = ['Epsilon-Greedy', 'UCB']
    V2V_percentages = [pourcentage_V2V_Epsilon, pourcentage_V2V_UCB]  # Pourcentages pour le bras V2V
    print ("V2V_percentages ok")
    V2I_percentages = [pourcentage_V2I_Epsilon, pourcentage_V2I_UCB]  # Pourcentages pour le bras V2I
    print ("V2I_percentages ok")
    # Position des barres sur l'axe x
    x = np.arange(len(algorithms))

    # Largeur des barres
    width = 0.35
    

    # Tracer les barres
    fig, ax = plt.subplots()
    bars1 = ax.bar(x - width/2, V2V_percentages, width, label='V2V')
    bars2 = ax.bar(x + width/2, V2I_percentages, width, label='V2I')

    # Ajouter des étiquettes, un titre et une légende
    ax.set_xlabel('Algorithmes')
    ax.set_ylabel('Pourcentage de choix (%)')
    ax.set_title('Pourcentage de choix pour chaque bras par algorithme')
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms)
    ax.legend()

    # Afficher les pourcentages au-dessus des barres
    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.annotate('{}'.format(height),
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    add_labels(bars1)
    add_labels(bars2)

    # Afficher le diagramme
    plt.show()



# Define the values of T and k for each environment to be tested
#T_values = [1000, 2000, 10000] # Pour voir l'évolution de la politique de choix de bras de la machine
T_values = [500]
k = 2

# Loop over the different environments and run the bandit algorithm for each
for i in range(len(T_values)):
    print(i)
    # Create a new bandit environment for the current k value
    env = BanditEnvironment(k)
    print("ok")
    # Run the bandit algorithm and plot the results
    run_bandit(env, k, T_values[i])

# for i in range(1):
#     
#     # Create a new bandit environment for the current k value
#     env = BanditEnvironment(k)
#     print("ok")
#     # Run the bandit algorithm and plot the results
#     run_bandit(env, k, 500)