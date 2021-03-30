from heapq import heappush, heappop
from itertools import count

import networkx as nx
from networkx.algorithms.shortest_paths.weighted import _weight_function

def greedy_path(G, source, target, heuristic=None, weight='weight'):
    
    if source not in G or target not in G:
        msg = f"Il nodo di partenza {source} o il nodo di arrivo {target} non appartengono al grafo G"
        raise nx.NodeNotFound(msg)
        
    if heuristic is None:
        def heuristic(u, v):
            return 0
    
    push = heappush
    pop = heappop
    weight = _weight_function(G, weight)
    
    c = count()
    queue = [(0, next(c), source, 0, None)]
    
    enqueued = {}
    explored = {}
    
    while queue:
        _, __, curnode, dist, parent = pop(queue)

        if curnode == target:
            path = [curnode]
            node = parent
            while node is not None:
                path.append(node)
                node = explored[node]
            path.reverse()
            return path

        if curnode in explored:
            if explored[curnode] is None:
                continue

            qcost, h = enqueued[curnode]
            if qcost < dist:
                continue

        explored[curnode] = parent

        for neighbor, w in G[curnode].items():
            ncost = weight(curnode, neighbor, w)
            if neighbor in enqueued:
                qcost, h = enqueued[neighbor]
                if qcost <= ncost:
                    continue
            else:
                h = heuristic(neighbor, target)
            enqueued[neighbor] = ncost, h
            push(queue, (ncost + h, next(c), neighbor, ncost, curnode))

    raise nx.NetworkXNoPath(f"Il nodo {target} non è raggiungibile da {source}")

    
#In questo modo esegue la graph search, infatti passandogli il grafo che rappresenta le città della Romania cicla all'infinito, ma basta
#definire un'euristica e porre ncost = costo_nodo(neighbor) alla riga 50 per ottenere la greedy search che utilizza l'euristica:
def greedy_path_con_euristica(G, source, target, heuristic=None, weight='weight'):
    
    if source not in G or target not in G:
        msg = f"Il nodo di partenza {source} o il nodo di arrivo {target} non appartengono al grafo G"
        raise nx.NodeNotFound(msg)
        
    if heuristic is None:
        def heuristic(u, v):
            return costo_nodo(u)
    
    push = heappush
    pop = heappop
    weight = _weight_function(G, weight)
    
    c = count()
    queue = [(0, next(c), source, 0, None)]
    
    enqueued = {}
    explored = {}
    
    while queue:
        _, __, curnode, dist, parent = pop(queue)

        if curnode == target:
            path = [curnode]
            node = parent
            while node is not None:
                path.append(node)
                node = explored[node]
            path.reverse()
            return path

        if curnode in explored:
            if explored[curnode] is None:
                continue

            qcost, h = enqueued[curnode]
            if qcost < dist:
                continue

        explored[curnode] = parent

        for neighbor, w in G[curnode].items():
            ncost = costo_nodo(neighbor)
            if neighbor in enqueued:
                qcost, h = enqueued[neighbor]
                if qcost <= ncost:
                    continue
            else:
                h = heuristic(neighbor, target)
            enqueued[neighbor] = ncost, h
            push(queue, (ncost + h, next(c), neighbor, ncost, curnode))

    raise nx.NetworkXNoPath(f"Il nodo {target} non è raggiungibile da {source}")
    
#L'euristica definita per la prova:
def costo_nodo(u):
    if(u == 'Arad'):
        return 366
    if(u == 'Bucharest'):
        return 0
    if(u == 'Craiova'):
        return 160
    if(u == 'Dobreta'):
        return 242
    if(u == 'Fagaras'):
        return 178
    if(u == 'Lugoj'):
        return 244
    if(u == 'Mehadia'):
        return 247
    if(u == 'Oradea'):
        return 380
    if(u == 'Pitesti'):
        return 98
    if(u == 'Rimnicu'):
        return 193
    if(u == 'Sibiu'):
        return 253
    if(u == 'Timisoara'):
        return 329
    if(u == 'Zerind'):
        return 374
    
#Il grafo definito per la prova:
g = nx.Graph()

g.add_edge('Arad', 'Zerind', weight=75)
g.add_edge('Arad', 'Sibiu', weight=140)
g.add_edge('Arad', 'Timisoara', weight=118)
g.add_edge('Zerind', 'Oradea', weight=71)
g.add_edge('Sibiu', 'Oradea', weight=151)
g.add_edge('Sibiu', 'Fagaras', weight=99)
g.add_edge('Sibiu', 'Rimnicu', weight=80)
g.add_edge('Timisoara', 'Lugoj', weight=111)
g.add_edge('Fagaras', 'Bucharest', weight=211)
g.add_edge('Rimnicu', 'Pitesti', weight=97)
g.add_edge('Rimnicu', 'Craiova', weight=146)
g.add_edge('Lugoj', 'Mehadia', weight=70)
g.add_edge('Bucharest', 'Pitesti', weight=101)
g.add_edge('Pitesti', 'Craiova', weight=138)
g.add_edge('Craiova', 'Dobreta', weight=120)
g.add_edge('Mehadia', 'Dobreta', weight=75)
