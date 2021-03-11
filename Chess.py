import Model, View, tkinter, copy, itertools, player, time
from tkinter import messagebox

class Controller():
    def __init__(self):
        self.root = tkinter.Tk()
        self.view = View.View(self.root)
        self.possiblePlayerTypes = ['local', 'cpu', 'network']
        self.whitePlayerTypes = itertools.cycle(self.possiblePlayerTypes)
        self.blackPlayerTypes = itertools.cycle(self.possiblePlayerTypes)
        self.view.whitePlayerType = next(self.whitePlayerTypes)
        self.view.blackPlayerType = next(self.blackPlayerTypes)
        self.closed = False
        self.root.bind('<<StartGame>>', self.startGame)
        self.root.bind('<<ChangeWhitePlayer>>', self.changeWhitePlayer)
        self.root.bind('<<ChangeBlackPlayer>>', self.changeBlackPlayer)
        self.root.bind('<<ClickedField>>', self.clickOnField)
        self.root.protocol('WM_DELETE_WINDOW', self.onClose)
        self.selectedField = None
        self.gameActive = False
        self.party = None
        self.players = None
    def run(self):
        while not self.closed:
            if self.gameActive == True:
                if self.party.mate:
                    if messagebox.askquestion('Mate, mate!', 'Want to play again?', icon='warning') == 'yes':
                        self.gameActive = False
                else:
                    self.nextMove()
            self.view.redraw(self.gameActive)
            self.root.update_idletasks()
            self.root.update()
    def startGame(self, event):
        self.party = Model.Party()
        self.view.fields = copy.deepcopy(self.party.board.fields)
        self.gameActive = True
        self.players = {'-1': player.Player.createPlayer(self.view.whitePlayerType, -1), '1': player.Player.createPlayer(self.view.blackPlayerType, 1)}
    def changeWhitePlayer(self, event):
        self.view.whitePlayerType = next(self.whitePlayerTypes)
    def changeBlackPlayer(self, event):
        self.view.blackPlayerType = next(self.blackPlayerTypes)
    def nextMove(self):
        playerType = self.players[str(self.party.activePlayer.color)].type
        movingCoordinates = self.players[str(self.party.activePlayer.color)].move(self.party)
        if movingCoordinates != None:
            if self.party.turn(movingCoordinates[0], movingCoordinates[1]):
                self.view.fields = copy.deepcopy(self.party.board.fields)
                self.activePlayer = self.party.activePlayer.color
                return True
            else:
                return False
    def clickOnField(self, event):
        if self.players[str(self.party.activePlayer.color)].type == 'LocalPlayer' and self.players[str(self.party.activePlayer.color)].moving:
            clickedPosition = Model.Position(event.x, event.y)
            if self.party.board.getPiece(clickedPosition) != None and self.party.board.getPiece(clickedPosition).color == self.party.activePlayer.color:
                self.selectedField = clickedPosition
                self.view.highlighted = clickedPosition
            elif self.selectedField != None:
                self.players[str(self.party.activePlayer.color)].moveCoordinates = [self.selectedField, clickedPosition]
                self.selectedField = None
                self.view.highlighted = None
            else:
                self.selectedField = None
                self.view.highlighted = None
        
    def onClose(self):
        self.closed = True
        self.root.destroy()
if __name__ == "__main__":
    c = Controller()
    c.run()