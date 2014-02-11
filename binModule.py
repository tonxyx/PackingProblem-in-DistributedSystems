class Bin:
    """Spremnik za spremanje elemenata"""
    def __init__(self, binId, capacity, contents=[]):
        self.binId = binId
        self.capacity = capacity
        self.contents = contents
    def add(self, x):
        self.contents.append(x)
    def __repr__(self):
        return str(self.contents)

class Item:
    """Spremnik za spremanje  podataka o elementima"""
    def __init__(self, itemId, value, startTime, binId, exeTime):
        self.itemId = itemId
        self.value = value
        self.startTime = startTime
        self.binId = binId
        self.exeTime = exeTime;
    def __repr__(self):
        return str(self.value)
