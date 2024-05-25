import numpy as np
import matplotlib.pyplot as plt

# Import des simulations
from V2V import V2V

# Define k-stochastic bandit environment
class BanditEnvironment:
    def __init__(self, k):
        # k: number of bandits
        self.k = k
        self.bandits = []

        # On enregistre les choix bras de la machine
        # UCB
        self.V2V_UCB = 0
        self.V2I_UCB = 0

        # Epsilon-Greedy
        self.V2V_Epsilon = 0
        self.V2I_Epsilon = 0

        # On génère les rewards pour chaque bras de la machine
        # V2V 
        a = np.random.uniform(0, 1)              # A FAIRE LA SIMU
        b = np.random.uniform(0, 1)              # A FAIRE LA SIMU
        self.bandits.append((a, b))

        # V2I
        a = np.random.uniform(0, 1)              # A FAIRE LA SIMU
        b = np.random.uniform(0, 1)              # A FAIRE LA SIMU
        self.bandits.append((a, b))
    
    # Given an arm, return a random reward drawn from the corresponding bandit's distribution
    def get_reward(self, arm):
        # arm: index of the bandit to pull
        # Returns a reward drawn from a uniform distribution with lower bound a and upper bound b
        a, b = self.bandits[arm]
        return np.random.uniform(a, b)
    
def epsilon_greedy(env, k, T):
    n = [0] * k # Number of times each arm has been pulled
    rewards = [0] * k # Cumulative rewards for each arm
    est_means = [0] * k # Estimated mean reward for each arm
    regrets = []
    for t in range(T):
        # Calculate exploration rate epsilon for the current time step using the given theorem
        with np.errstate(divide='ignore'):
            epsilon = np.power(t, -1/3) * np.power(k * np.log(t), 1/3)

        if np.random.rand() < epsilon:
            # Choose a random arm with equal probability if the exploration strategy is selected
            arm = np.random.randint(k)
        else:
            # Choose the arm with the highest estimated mean reward if the exploitation strategy is selected
            arm = np.argmax(est_means)
        reward = env.get_reward(arm) # Observe the reward for the chosen arm
        n[arm] += 1 # Increment the count of times the chosen arm has been pulled
        rewards[arm] += reward # Add the observed reward to the cumulative rewards for the chosen arm
        est_means[arm] = rewards[arm] / n[arm] # Update the estimated mean reward for the chosen arm
        optimal_reward = np.max([env.get_reward(i) for i in range(k)]) # Find the optimal reward among all arms
        regret = optimal_reward - reward #Calculate regret for the chosen arm
        regrets.append(regret) #Add the regret to the list of regrets
        
        # on enregistre les choix bras de la machine
        if arm == 0:
            env.V2V_Epsilon += 1
        else:
            env.V2I_Epsilon += 1

    # on retourne le cumul des regrets
    return np.cumsum(regrets)


def ucb(env, k, T):
    n = [0] * k # Number of times each arm has been pulled
    rewards = [0] * k # Cumulative rewards for each arm
    est_means = [0] * k # Estimated mean reward for each arm
    regrets = []
    for t in range(T):
        if t < k:
            # Play each arm k times to initialize the estimates and UCB values
            reward = env.get_reward(t)
            n[t] += 1
            rewards[t] += reward
            est_means[t] = rewards[t] / n[t]
            regrets.append(0)
        else:
            # Choose the arm with the highest UCB value
            ucb_values = [est_means[i] + np.sqrt(2*np.log(t) / n[i]) for i in range(k)] # Calculate UCB values for each arm
            arm = np.argmax(ucb_values) # Select the arm with the highest UCB value
            reward = env.get_reward(arm) # Observe the reward for the chosen arm
            n[arm] += 1 # Increment the count of times the chosen arm has been pulled
            rewards[arm] += reward # Add the observed reward to the cumulative rewards for the chosen arm
            est_means[arm] = rewards[arm] / n[arm] # Update the estimated mean reward for the chosen arm
            optimal_reward = np.max([env.get_reward(i) for i in range(k)]) # Find the optimal reward among all arms
            regret = optimal_reward - reward #Calculate regret for the chosen arm
            regrets.append(regret) #Add the regret to the list of regrets

            # on enregistre les choix bras de la machine
            if arm == 0:
                env.V2V_UCB += 1
            else:
                env.V2I_UCB += 1

    # on retourne le cumul des regrets
    return np.cumsum(regrets)

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
    plt.title(f"T = {T} l'horizon (nb itération), k = 2 BRAS")
    plt.plot(eps_regrets, label="Epsilon-Greedy")
    plt.plot(ucb_regrets, label="UCB")
    plt.xlabel("Time")
    plt.ylabel("Cumulative Regret")
    plt.legend()
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


