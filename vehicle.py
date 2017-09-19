class Vehicle:
    """Vehicle Class.
    
    This class store information about problem vehicles
    
    Attribuetes:
        time               (int): The actual time.
        position           (int): The vehicles actual position.
        capacity           (int): The vehicles actual capacity.
        limit              (int): The vehicles limit capacity.
        distance          (list): The distance travel.
    """
    def __init__(self, depost = None, limit = 0, request = []):
        """init method for PDPT class
        
        This method construct an PDPT instance
        
        Parameters:
            deposts  (list): The vehicle initial position
            limit   (tuple): The vehicle limit capacity
            request      (list): The request assign to this vehicle
        """
        self.time = 0
        self.position = depost
        self.requests = request
        self.limit = limit
        self.distance = 0

    def move(self, nx, cost):
        self.position = nx
        self.distance += cost
        delivery()

    def capacity(self):
        return sum([i[0] for i in self.requests])
    
    def endpoints(self):
        return [i[1] for i in self.requests]
            
    def pickup(self, value, destination):
        if value + self.capacity() < self.limit:
            self.requests.append((value, destination))
        else:
            value/0 # the ugliest way to generate an error
    
    def delivery(self):
        # https://stackoverflow.com/a/2522013/7929168 
        # why this instance try/except(ValueError)
        end = endpoints()
        while self.position in end: # if i can deliver
            pos = end.index(self.position)
            print("delivering {}".format(self.requests[pos]))
            del self.requests[pos]
                        
    def Transfer(self, other, request):
        index = self.requests.index(request)
        del self.requests[index]
        other.requests.append(request)
        
    def __rshift__(self, other):
        # Full transfer
        if self.capacity() + other.capacity() < other.limit:
            other.requests.extend(self.requests)
            self.requests = []
        else:
            self.requests.sort(key=lambda x: x[0], reverse=True)
            oc = other.capacity()
            while self.requests and self.requests[-1][0] + oc < other.limit:
                oc += self.requests[-1][0]
                other.requests.append(self.requests.pop())

    def __str__(self):
        return """
           o__________________
           |              |   \\
           |     cap {c}    |____\\_____
           | _____        |    |_o__ |
           [/ ___ \       |   / ___ \|
          []_/.-.\_\______|__/_/.-.\_[]
             |(O)|             |(O)|
              '-'   Pos {n}       '-'
        ---   ---   ---   ---   ---   --- 
        request : {req}
        """.format(c = self.limit,
                   n = self.position,
                   req = self.requests)