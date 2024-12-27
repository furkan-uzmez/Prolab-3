from pqueue import PriorityQueue
from myqueue import Queue

def dijkstra(graph, start):
    #kuyruk = Queue() # 3.ister için

    INF = 10 ** 9
    distances = {}
    for node in graph:
        distances[node] = INF
    distances[start] = 0

    previous_nodes = {}

    for node in graph:
        previous_nodes[node] = None


    unvisited = PriorityQueue()
    unvisited.push(start, 0)

    while not unvisited.is_empty():
        current_node = unvisited.pop()

        for neighbor, weight in graph[current_node].items():
            distance = distances[current_node] + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                unvisited.push(neighbor, distance)
    return distances, previous_nodes


def shortest_path(graph, start, end): # 1.ister
    distances, previous_nodes = dijkstra(graph, start)

    path = []
    current_node = end
    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]

    path.reverse()
    #print(path)
    #print(distances[end])
    return path, distances[end]

