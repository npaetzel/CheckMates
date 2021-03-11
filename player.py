import RedQueen
from threading import Thread

class Player():
    def __init__(self, color):
        self.color = color
        self.type = type(self).__name__
        self.moving = False
        self.moveCoordinates = None
    def move(self, party):
        pass
    @staticmethod
    def createPlayer(type, color):
        if type == 'local':
            return LocalPlayer(color)
        elif type == 'cpu':
            return CPUPlayer(color)
        elif type == 'network':
            return NetworkPlayer(color)
        else:
            return None
class LocalPlayer(Player):
    def __init__(self, color):
        super().__init__(color)        
    def move(self, party):
        if self.moving:
            if self.moveCoordinates == None:
                return None
            else:
                self.moving = False
                return self.moveCoordinates
        else:
            self.moveCoordinates = None
            self.moving = True
            return None
class CPUPlayer(Player):
    def __init__(self, color):
        super().__init__(color)
        self.bot = RedQueen.Bot(color)
    def move(self, party):
        if self.moving:
            if self.moveCoordinates == None:
                return None
            else:
                self.moving = False
                return self.moveCoordinates
        else:
            self.moveCoordinates = None
            self.moving = True
            thread = Thread(target=self.startBot, args=(party, 3))
            thread.start()
            return None
    def startBot(self, party, depth):
        self.moveCoordinates = self.bot.lookAhead(party, depth)
class NetworkPlayer(Player):
    def __init__(self, color):
        super().__init__(color)