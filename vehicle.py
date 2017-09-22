class Vehicle:
    """Vehicle Class.

    This class store information about problem vehicles
    Attribuetes:
        time               (int): The actual time.
        position           (int): The vehicles actual position.
        distance          (list): The distance travel.
    """
    def __init__(self, depost=None, request=[]):
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
        self.distance = 0

    def move(self, nx, cost):
        self.position = nx
        self.distance += cost

    def endpoints(self):
        return [i for i in self.requests]

    def pickup(self, destination):
        self.requests.append(destination)

    def delivery(self):
        # https://stackoverflow.com/a/2522013/7929168
        # why this instance try/except(ValueError)
        end = self.endpoints()
        while self.position in end:  # if i can deliver
            pos = end.index(self.position)
            print("delivering {}".format(self.requests.pop(pos)))

    def Transfer(self, other, request):
        index = self.requests.index(request)
        other.requests.append(self.requests.pop(index))

    def __rshift__(self, other):
        # Full transfer
        other.requests.extend(self.requests)
        self.requests = []

    def __str__(self):
        return """
           o__________________
           |              |   \\
           |              |____\\_____
           | _____        |    |_o__ |
           [/ ___ \       |   / ___ \|
          []_/.-.\_\______|__/_/.-.\_[]
             |(O)|             |(O)|
              '-'   Pos {n}       '-'
        ---   ---   ---   ---   ---   ---
        request : {req}
        """.format(n=self.position,
                   req=self.requests)
