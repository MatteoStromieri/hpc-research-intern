import heapq

"""
This class is a DOubleEndedQueue for items (Objects) that implement a getPriority method
"""

class DoubleEndedQueue:
    def __init__(self):
        self.sorted_list = []
        self.len = 0

    def insert(self,item):
        self.sorted_list.append(item)
        self.sorted_list.sort(key = item.getPriority())
        len += 1
    
    def readMax(self):
        try:
            return self.sorted_list[len-1]
        except:
            print("something went wrong")

    def readMin(self):
        try:
            return self.sorted_list[0]
        except:
            print("something went wrong")

    def popMax(self):
        try:
            max = self.sorted_list.pop()
            return max
        except:
            print("something went wrong")

    def getMin(self):
        try:
            min = self.sorted_list.pop(0)
            return min
        except:
            print("something went wrong")

    def isEmpty(self):
        if self.len == 0:
            return True
        else:
            return False
    
    def remove(self, item):
        self.sorted_list.remove(item)

    def reset(self):
        self.sorted_list.sort()