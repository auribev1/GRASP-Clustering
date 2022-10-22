def costo(sol, cluster, dis):  #Determina el costo distancia a recorrer de los nodos a su respectivo centro
    cost = 0
    for pos, i in enumerate(cluster):
        cost += dis[pos, sol[i]]
    return cost


def gen_sol_alea(nodos, k): # Solución completamente aleatoria
    import numpy as np
    sol = np.random.choice(nodos, k, replace=False)
    cluster = np.random.randint(0, k, len(nodos))
    if is_fact(sol, cluster, nodos, k):
        return sol, cluster


def is_fact(sol, cluster, nodos, k): #Esta solucion determina si la sol es factible en terminos del tamaño de la solución y los rangos entre los que estén
    sol_pos = [i for i in range(k)]
    if (len(sol) == k) and (len(cluster) == len(nodos)):
        for i in sol:
            if i not in nodos:
                print("Not a valid node")
                return False
        for i in cluster:
            if i not in sol_pos:
                print("Node is not a center")
                return False
        return True
    else:
        print("Solution incomplete")
        return False


def assign_cluster(sol, cluster, nodos, dis): #Esta funcion asigna cada nodo a la menor distancia de centro en la solución
    import numpy as np
    for i in nodos:
        short_dis = []
        for j in sol:
            short_dis.append(dis[i, j])
        cluster[i] = np.argmin(short_dis)
    return cluster


def greedy_construct(nodos, k, dis):
    import numpy as np
    sol = np.array([np.random.randint(0, len(nodos))])  # Creo solución con centro random
    cluster = np.zeros(len(nodos), dtype=int)
    for i in range(1, k):
        cluster = assign_cluster(sol, cluster, nodos, dis)  # Asigna los clusters con menor distancia a cada centro
        cos = costo(sol, cluster, dis)                      # Calcula el costo asociado
        costos = []
        for n in nodos:
            if n not in sol:
                sol_copy = np.copy(sol)
                cluster_copy = np.copy(cluster)
                sol_copy = np.append(sol_copy, n)                                   # Añado un centro n a la copia de la solución
                cluster_copy = assign_cluster(sol_copy, cluster_copy, nodos, dis)   # Asigno con la nueva solución los nodos a la menor distancia
                cos_aux = costo(sol_copy, cluster_copy, dis)                        # Calculo el costo auxiliar
                costos.append(cos_aux)                                              # Concateno en la lista de costos cual fue el costo actual
            else:
                costos.append(cos)
        RCL = np.sort(costos)[:k]                                   # Creo una lista con los k mejores costos (menores)
        nodo = np.where(np.random.choice(RCL) == costos)[0][0]      # Selecciono un nodo aleatorio en la lista RCL
        sol = np.append(sol, nodo)                                  # Lo añado a la solución real
    cluster = assign_cluster(sol, cluster, nodos, dis)              # Calculo la distancia menor para la solución final y calculo el costo
    cos = costo(sol, cluster, dis)
    return sol, cluster, cos

def local_search(sol, cluster, cos, dis, nodos):
    import numpy as np
    import random
    condition = True
    while condition:        # Mientras la condicion de parada no se cumpla (que no haya mejora en la iteracion)
        node_list = [i for i in nodos if i not in sol]
        random.shuffle(node_list)       # Crea una lista random y la aleatoriza
        nodo = np.random.choice(sol)    # Seleciona un centro random de la solución para intercambiar
        indicator = 0
        for i in node_list:
            sol_copy = np.copy(sol)
            cluster_copy = np.copy(cluster)
            sol_copy[np.where(sol_copy == nodo)[0][0]] = i                  # Cambia el centro seleccionado anteriormente por cada nodo
            cluster_copy = assign_cluster(sol, cluster_copy, nodos, dis)    # Asigna los centros y calcula los costos
            cos_aux = costo(sol_copy, cluster_copy, dis)
            if cos_aux < cos:       # Si el costo es mejor, reemplaza el actual
                sol = sol_copy
                cluster = cluster_copy
                cos = cos_aux
                indicator = 1
                break
        if indicator == 0:      # Si la condicion se cumple se sale del ciclo infinito
            condition = False
    return sol, cluster, cos









