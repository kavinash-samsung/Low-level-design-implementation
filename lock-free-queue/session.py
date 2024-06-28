import threading

# a node data structure
# individual element in the queue
class Node:
    def __init__(self, item) -> None:
        self.item = item
        self.next = None
        

class LockFreeQueue:
    def __init__(self) -> None:
        self.head = None
        self.tail = None
        # creating lock for synchronization
        self.lock = threading.Lock()
        # creating it for connection between two threads
        # this is also associated with the lock
        self.empty_condition = threading.Condition(self.lock)
        
    def enqueue(self, item):
        # create a node
        newNode = Node(item)
        with self.lock:
            if self.tail:
                self.tail.next = newNode
            else:
                self.head = newNode
            self.tail = newNode
            # notify other waiting thread that queue is no longer empty
            self.empty_condition.notify()
    
    # this method remove item from queue
    def dequeue(self):
        with self.lock:
            # TODO: yet to handle dequeue if queue is empty
            # if queue is empty wait till notified by other thread
            while not self.head:
                self.empty_condition.wait()
            first_item = self.head.item
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            return first_item
    
    # checks if queue is empty or not 
    def is_empty(self):
        with self.lock:
            return self.head is None;
        
        
# def simulate_concurrency()