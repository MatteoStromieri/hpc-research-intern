import json

"""
This class is a DOubleEndedQueue for items (Objects) that implement a getPriority method
"""

class DoubleEndedQueue:
    def __init__(self):
        self.sorted_list = []
    
    def toString(self):
        s = ""
        for p in self.sorted_list:
            s = s + " | " + p.toString()
        return s
    
    def duplicate(self):
        dup = DoubleEndedQueue()
        dup.sorted_list = list(self.sorted_list)

    def insert(self,item,G, K, h, ed):
        self.sorted_list.append(item)
        self.sorted_list.sort(key = lambda obj : obj.getExecTime(G, K, h, ed))
    
    def readMax(self):
        try:
            return self.sorted_list[len(self.sorted_list) - 1]
        except:
            print(f"something went wrong. sorted_list = {self.sorted_list} | len(self.sorted_list) = {len(self.sorted_list)}")

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
        if len(self.sorted_list) == 0:
            return True
        else:
            return False
    
    def remove(self, item):
        self.sorted_list.remove(item)

    def reset(self, G, K, h, ed):
        self.sorted_list.sort(key = lambda obj : obj.getExecTime(G, K, h, ed))