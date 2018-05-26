#!/usr/bin/python3


from CS312Graph import *
import time
import math
from BinaryHeap import BinaryHeap


class NetworkRoutingSolver:
    def __init__( self, display ):
        pass



    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network



    def getShortestPath( self, destIndex ):
        """
        Find the shortest path from the source node to the destination node
        Dijkstra's algorithm has already been run
        We are only finding the specific shortest path and cost for each node

        :param destIndex: The index of the destination node we are interested in finding the shortest path of
        :return: Returns a dictionary with the cost and the path as keys
        """
        self.dest = destIndex

        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL 
        #       NEED TO USE

        path_edges = []
        total_length = 0

        node = self.network.nodes[self.dest]  # Get the destination node
        # Check if the node is the source node
        while node.node_id != self.source:
            # Get parent node
            prev = self.network.nodes[self.results[node.node_id]['prev']]
            # Get the neighbors of prev
            neighbors = prev.neighbors
            for neighbor in neighbors:
                if neighbor.dest.node_id == node.node_id:
                    edge = neighbor
                    break
            path_edges.append( (edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)) )
            total_length += edge.length

            node = prev

        return {'cost': total_length, 'path': path_edges}



    def computeShortestPaths( self, srcIndex, use_heap=False ):
        """
        Compute the shortest path from the source node to every other node in the graph


        :param srcIndex: Specifies the source node used in Djikstra's
        :param use_heap: Determines whether to use heap or array priority queue
        :return: Time it took to compute Dijkstra's
        """
        self.source = srcIndex

        t1 = time.time()
        self.dijkstra(use_heap)
        t2 = time.time()

        return t2-t1

    """
    We will need a function that can perform dijkstra's algorithm
    Function 𝑑𝑖𝑗𝑘𝑠𝑡𝑟𝑎 𝐺, 𝑠
        • 𝐺 = 𝑉, 𝐸 is the weighted directed graph
        • 𝑠 is the starting node
        • Returns the shortest distance from 𝑠 to every
        other vertex
        
        • Foreach 𝑢 ∈ 𝑉:
            • 𝑢. 𝑑𝑖𝑠𝑡 = ∞
            • 𝑢. 𝑝𝑟𝑒𝑣 = 𝑁𝑜𝑛𝑒
        • 𝑠. 𝑑𝑖𝑠𝑡 = 0
        • 𝐻 = 𝑝𝑟𝑖𝑜𝑟𝑖𝑡𝑦𝑞𝑢𝑒𝑢𝑒 𝑉 # distances as keys
        • While 𝐻 is not empty:
            • 𝑢 = 𝐻. 𝑔𝑒𝑡𝑛𝑒𝑥𝑡() # gets the smallest item from the
            priority queue, deleting it from the queue
            • Foreach e = 𝑢, 𝑣 ∈ 𝐸 and 𝑣 ∈ 𝑄 (not visited):
                • If 𝑣. 𝑑𝑖𝑠𝑡 > 𝑢. 𝑑𝑖𝑠𝑡 + 𝑒. 𝑙𝑒𝑛𝑔𝑡ℎ
                • 𝑣. 𝑑𝑖𝑠𝑡 = 𝑢. 𝑑𝑖𝑠𝑡 + 𝑒. 𝑙𝑒𝑛𝑔𝑡ℎ
                • 𝑣. 𝑝𝑟𝑒𝑣 = 𝑢
                • 𝐻. 𝑢𝑝𝑑𝑎𝑡𝑒𝑘𝑒𝑦(𝑣, 𝑣. 𝑑𝑖𝑠𝑡)
"""
    def dijkstra(self, use_heap):
        # Create priority queue with all distances initialized to infinity
        priority_queue = PriorityQueue(self.network, use_heap)
        # Set the source node distance to 0
        priority_queue.update_key(self.source, 0)
        # The source node prev is initialized to -1
        # Loop while nodes remain in the priority queue
        self.results = {}
        # Initialize the results dictionary
        for i in range(len(self.network.nodes)):
            # Add the node to the array
            self.results[self.network.nodes[i].node_id] = {'dist': math.inf, 'prev': -1}
        # Set the results source node distance to 0
        self.results[self.source]['dist'] = 0
        while not priority_queue.is_empty():
            # Get the smallest distance node
            u = priority_queue.get_next()   # u is closest node
            # Get all the neighbors
            neighbors = self.network.nodes[u['id']].neighbors
            # For each neighboring node
            for neighbor in neighbors:
                # Get the neighbor node
                v = self.results[neighbor.dest.node_id]
                # Check the distance to each neighbor
                if v['dist'] > u['dist'] + neighbor.length:
                    v['dist'] = u['dist'] + neighbor.length
                    v['prev'] = u['id']
                    priority_queue.update_key(neighbor.dest.node_id, v['dist'])


class PriorityQueue:
    """
    Implement a priority queue that either uses an array or a heap

    𝑔𝑒𝑡𝑛𝑒𝑥𝑡: Gets the next item with the smallest key
        Runs 𝑉 times
•   𝑢𝑝𝑑𝑎𝑡𝑒𝑘𝑒𝑦 (and 𝑖𝑛𝑠𝑒𝑟𝑡): Updates the key of a desired vertex
•       Runs 𝑉 + 𝐸 times
    """
    def __init__(self, network, use_heap=False):
        self.use_heap = use_heap
        self.node_count = len(network.nodes)
        # Add each node in graph to Priority Queue
        if not use_heap:
            # Create an array for the queue
            self.queue = {}
            # For each node in the network
            for i in range(self.node_count):
                # Add the node to the array
                self.queue[network.nodes[i].node_id] = { 'dist': math.inf}
        else:
            # Create a binary heap
            self.queue = BinaryHeap()
            # Add each element of the network to the queue
            for i in range(self.node_count):
                self.queue.insert(network.nodes[i].node_id, math.inf)

    def get_next(self):
        # Pop the highest priority element off the queue
        if not self.use_heap:
            # Pop the smallest distance item of the array
            smallest_distance = math.inf    # Initialize to infinity
            smallest_key = -1
            # For each element in the queue
            for k,v in self.queue.items():
                if self.queue[k]['dist'] < smallest_distance:
                    smallest_distance = self.queue[k]['dist']
                    smallest_key = k
            smallest_node = {'id': smallest_key, 'dist': smallest_distance}
            if smallest_key == -1:
                popped_item = self.queue.popitem()
                return {'id': popped_item[0], 'dist': popped_item[1]['dist']}
            # Remove the element from queue
            del self.queue[smallest_key]
            # Return the smallest distance node
            return smallest_node
        else:
            # Return the root of
            return self.queue.delete_min()

    def update_key(self, node_id, dist):
        # Update the distance of a specified vertex
        if not self.use_heap:
            self.queue[node_id]['dist'] = dist
        else:
            self.queue.update(node_id, dist)

    def is_empty(self):
        # Return True if the queue is empty
        # Return False if the queue is not empty

        if not self.use_heap:
            if len(self.queue) == 0:
                return True
            else:
                return False
        else:
            if self.queue.length() == 0:
                return True
            else:
                return False
