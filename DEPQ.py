import heapq

class DoubleEndedQueue:
    def __init__(self, get_priority):
        self.sorted_list = []
        self.get_priority = get_priority
        self.len = 0

    def insert(self,item):
        self.sorted_list.append(item)
        self.sorted_list.sort(key = self.get_priority)
        len += 1
    
    def get_max(self):
        try:
            return self.sorted_list[len-1]
        except:
            print("something went wrong")

    def get_min(self):
        try:
            return self.sorted_list[0]
        except:
            print("something went wrong")

     def pop_max(self):
        try:
            max = self.sorted_list.pop()
            return max
        except:
            print("something went wrong")

    def get_min(self):
        try:
            min = self.sorted_list.pop(0)
            return min
        except:
            print("something went wrong")