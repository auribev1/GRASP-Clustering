import numpy as np
from Functions import gen_sol_alea, costo, is_fact, greedy_construct, local_search

instance = input("Desea ejecutar con la distancia small o la large?: ")
dis = np.loadtxt("distances_" + str(instance) + ".txt")
dem = np.loadtxt("data_" + str(instance) + ".txt")
k = int(input("Cuantos acopios va a utilizar?: "))

def GRASP(dis, dem, k):
    nodos = [i for i in range(len(dem))]

    # SOL = Vector con el numero del nodo que es cluster (3,7,9) en orden
    # cluster: vector con todos los nodos y su respectivo cluster (0,1,2,3...,n)

    # Solución aleatoria
    best_sol, best_cluster = gen_sol_alea(nodos, k)     # Solución aleatoria
    best_cost = costo(best_sol, best_cluster, dis)      # Incumbente

    for i in range(50):     # Para 50 iteraciones (parametro determinado probando varias configuraciones con el dataset small)
        #Greedy constructive
        sol, cluster, cos = greedy_construct(nodos, k, dis) # Generación Greedy
        if is_fact(sol, cluster, nodos, k):                 # Si solución es factible proceder
            #Local Search
            sol, cluster, cos = local_search(sol, cluster, cos, dis, nodos)
            if is_fact(sol, cluster, nodos, k):     # Si solución es factible
                if cos < best_cost:                 # Si es mejor que la incumbente reemplazarla
                    best_sol = sol
                    best_cluster = cluster
                    best_cost = cos

    return best_sol, best_cluster, best_cost


sol, cluster, cost = GRASP(dis, dem, k)
print(sol, cluster, cost)




