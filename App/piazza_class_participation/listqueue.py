class ListQueue:
    """Implementation of a queue using list as underlying storage"""
    # a default capacity which can be increased using resize
    default_capacity = 100

    def __init__(self):
        """initialize a queue"""
        self._data = [None] * ListQueue.default_capacity
        self._size = 0
        self._front = 0

    def __len__(self):
        # returns the number of element in the queue
        return self._size

    def print(self):
        print(self._data)

    def is_empty(self):
        # returns true if queue is empty, false otherwise
        return self._size == 0

    # if full, resize
    def _resize(self, new_capacity):
        """create a new list of the given capacity"""
        # front will be realigned to zero
        # rest of the elements will be copied maintaining the order of the elements
        copy = self._data  # copy the existing list
        self._data = [None] * new_capacity
        temp = self._front

        for index in range():
            self._data[index] = copy[temp]  # copying each element one by one
            temp = (temp + 1) % len(copy)  # ensuring the circularity
        # resetting the front to 0 i.e. beginning of the new list
        self._front = 0

    def first(self):
        # raise an IndexError with a message "The Queue is empty" if the queue is empty
        # else return the element at the front without removing it
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._data[self._front]

    def enqueue(self, e):
        """add an element to the back of the queue"""
        # add an element if there is enough space, else resize by 3*current size
        # Make use of the resize defined above
        # In other words, first compute the location where you can put the new element
        # the formula for computing location should be sound enough to take care of both of the
        # cases i.e. (1) if the queue was full and resize occurred, (ii) if the resize did not occur
        if self._size == len(self._data):
            self._resize(3 * len(self._data))  # double the queue size
        available_index = (self._front + self._size) % len(self._data)
        self._data[available_index] = e
        self._size += 1

    def dequeue(self):
        """removes and returns an element from the front of the queue"""

        if self.is_empty():
            raise IndexError("Queue is empty")
        answer = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % len(self._data)
        self._size = self._size - 1
        return answer