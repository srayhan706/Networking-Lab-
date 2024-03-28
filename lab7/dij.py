import heapq

def dijkstra(graph, start):
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances

def main():
    num_vertices, num_edges = map(int, input("Enter the number of vertices and edges: ").split())
    graph = {str(i): {} for i in range(num_vertices)}

    for _ in range(num_edges):
        v1, v2, weight = map(int, input("Enter edge and weight (format: v1 v2 weight): ").split())
        v1, v2 = str(v1), str(v2)
        graph[v1][v2] = weight
        graph[v2][v1] = weight  # Assuming undirected graph
    
    start_vertex = input("Enter the start vertex: ")
    shortest_distances = dijkstra(graph, start_vertex)
    print("Shortest distances from vertex", start_vertex, ":", shortest_distances)

if __name__ == "__main__":
    main()

