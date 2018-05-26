

class BinaryHeap:
    def __init__(self):
        self.heap = [-1] # Initialize an array that is our heap

    def insert(self, node_id, dist):
        x = {'id': node_id, 'dist': dist}
        self.heap.append(x)     # Append the new element on the end of the array

        # Percolate up
        # Percolating up is log(V) operation because at worst case it needs to percolate up the whole tree.
        self.percolate_up(x, len(self.heap) - 1)

    def delete_min(self):
        first = self.heap[1]    # Get the smallest element in the heap
        x = self.heap[len(self.heap) - 1]   # Get the last element added to the heap
        self.heap[1] = x     # Add the last element to the top of the tree
        self.heap.pop()     # Pop the last item on the index

        # Percolate down
        # Percolating down is log(V) operation because at worst case it needs to percolate down the whole tree.
        self.percolate_down(x, 1)

        return first

    # Updating a value needs to be O(V) at the worst case to avoid missing the target node
    # The tree is only partially sorted
    def update(self, node_id, dist):
        for i in range(1, len(self.heap)):
            if self.heap[i]['id'] == node_id:
                self.heap[i]['dist'] = dist
                self.percolate_up(self.heap[i], i)
                # self.percolate_down(self.heap[i], i)
                break

    # Log(V) operation because we divide the position by 2 every step
    def percolate_up(self, x, pos):
        # Percolate up

        # Check if the parent is bigger
        while pos != 1 and self.heap[int(pos / 2)]['dist'] > x['dist']:
            # Get the element's parent
            parent = self.heap[int(pos / 2)]
            # Swap the parent and the child
            self.heap[int(pos / 2)] = x
            self.heap[pos] = parent
            # Update the position of the new element
            pos = int(pos / 2)

    # Log(V) operation because we multiply the position by 2 every step
    def percolate_down(self, x, pos):
        # Percolate down
        # Check if we are at the bottom of the tree
        # or if the children are not less than x
        while True:
            children = []
            positions = []
            # Check left child
            if (2 * pos) <= (len(self.heap) - 1) and self.heap[pos * 2]['dist'] < x['dist']:
                # Get the child
                children.append(self.heap[pos * 2])
                positions.append(pos * 2)
            # Otherwise check if there is another child
            if (2 * pos + 1) <= (len(self.heap) - 1) and self.heap[pos * 2 + 1]['dist'] < x['dist']:
                children.append(self.heap[pos * 2 + 1])
                positions.append(pos * 2 + 1)
            if len(children) == 0:
                break
            # Swap the parent and the child
            if len(children) == 1:
                child = children[0]
                child_pos = positions[0]
            elif children[0]['dist'] < children[1]['dist']:
                child = children[0]
                child_pos = positions[0]
            else:
                child = children[1]
                child_pos = positions[1]

            self.heap[child_pos] = self.heap[pos]
            self.heap[pos] = child
            pos = child_pos

    def length(self):
        return len(self.heap) - 1
