# This function finds all paths connecting two points in the context of your project.

def trouver_chemins_reliant(un, n, chemin_actuel=[]):
    # If we have reached the destination point n, we print the current path
    if un == n:
        print(chemin_actuel + [n])
        return
    
    # Otherwise, we explore two options: going directly to the next step or passing through an intermediate point
    for i in range(un + 1, n + 1):
        # Add the current step to the path
        chemin_actuel.append(un)
        # Explore the path directly to the next step
        trouver_chemins_reliant(i, n, chemin_actuel)
        # Remove the current step to explore other paths
        chemin_actuel.pop()

# Example usage with n = 6 vehicles between V2V communication (Vehicle to Vulnerable person communication)
n = 6
trouver_chemins_reliant(1, n)
