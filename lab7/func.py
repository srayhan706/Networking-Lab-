from collections import defaultdict
import heapq as heap
import math
import socket
import os
import threading
import time
import random
import utils
from concurrent.futures import ThreadPoolExecutor


ipport = utils.getIpPorts()
neighbour = []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
G = {}


curr = ""
def set_curr(value):
    global curr
    curr = value

def init_graph():
    with open("init.txt") as f:
        for line in f:
            src, dest, cost = line.split()
            if src == curr:
                neighbour.append(dest)
                if src not in G:
                    G[src] = {}
                G[src][dest] = int(cost)
                if dest not in G:
                    G[dest] = {}
                G[dest][src] = int(cost)

    nodeCost, parentsMap = dijkstra(G, curr)
    print_cost(nodeCost, parentsMap)


def dijkstra(G, start):
    visited = set()
    parentsMap = {}
    pq = []
    nodeCost = {node: math.inf for node in G}
    nodeCost[start] = 0
    heap.heappush(pq, (0, start))
    while pq:
        currCost, currNode = heap.heappop(pq)
        if currNode in visited:
            continue
        visited.add(currNode)
        for neighbour, cost in G[currNode].items():
            if neighbour in visited:
                continue
            if currCost + cost < nodeCost[neighbour]:
                nodeCost[neighbour] = currCost + cost
                parentsMap[neighbour] = currNode
                heap.heappush(pq, (nodeCost[neighbour], neighbour))

    return nodeCost, parentsMap

def print_shortest_path(parentsMap, start):
    print("Shortest Path from", start)
    for destNode in parentsMap:
        path = []
        node = destNode
        while node != start:
            if node not in parentsMap:
                print("No path from", start, "to", destNode)
                break

            path.append(node)
            node = parentsMap[node]
        path.append(start)
        print(f"{start} to {destNode}: {' -> '.join(reversed(path))}")


def print_cost(nodeCost, parentsMap):
    print("Cost of each node")
    for node in nodeCost:
        print(f"Cost to reach {node}: {nodeCost[node]}")
    print_shortest_path(parentsMap, curr)


def msg_to_neighbour(msg):
    for n in neighbour:
        neighbourIP = ''
        neighbourPort = ipport[n]
        cl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            cl.connect((neighbourIP, neighbourPort))
            cl.send(msg.encode())
        except:
            print("Error in sending message to", n)
        finally:
            cl.close()

        
def msg_send():
    id = curr + " 60\n"
    s = ""
    for adj, weight in G[curr].items():
        s += curr + " " + adj + " " + str(weight) + "@"

    msg = id + s
    msg_to_neighbour(msg)

def msg_parse(msg):
    temp = msg
    msg = msg.split('\n')
    id, ttl = msg[0].split()
    if id == curr:
        return
    else:
        msg_to_neighbour(temp)
        msg = msg[1].split('@')
        for i in msg:
            try:
                src, dest, cost = i.split()
            except:
                break
            if src not in G:
                G[src] = {}
            G[src][dest] = int(cost)
            if dest not in G:
                G[dest] = {}
            G[dest][src] = int(cost)
        print("Graph updated")
        nodeCost, parentsMap = dijkstra(G, curr)
        print_cost(nodeCost, parentsMap)

def update_graph():
    while True:
        time.sleep(30)
        id = curr + " 60\n"
        s = ""
        node = random.choice(list(G.keys()))
        cost = random.randint(30, 50)
        if node == curr:
            continue
        G[curr][node] = cost
        G[node][curr] = cost
        print(f"Updated cost from {curr} to {node} is {cost}")
        s += curr + " " + node + " " + str(cost) + "@"
        msg = id + s
        msg_to_neighbour(msg)
        nodeCost, parentsMap = dijkstra(G, curr)
        print_cost(nodeCost, parentsMap)


def handle_client(conn, addr):
    data = conn.recv(1024).decode()
    msg_parse(data)

def main():
    a = input("press ENTER to start")
    init_graph()
    print("[STARTING] Server is starting...")
    server.bind(('', ipport[curr]))
    server.listen()
    IP = socket.gethostbyname(socket.gethostname())
    print(f"[LISTENING] Server is listening on {IP}")
    
    # Create a thread pool for handling client connections
    with ThreadPoolExecutor(max_workers=10) as executor:
        initial_msg_thread = executor.submit(msg_send)
        update_thread = executor.submit(update_graph)
        
        while True:
            conn, addr = server.accept()
            executor.submit(handle_client, conn, addr)

