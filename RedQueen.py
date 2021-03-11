import Model, copy
from operator import itemgetter

class Bot():
    def __init__(self, color):
        self.color = color
        self.values = {'Pawn': 1, 'Knight': 3.05, 'Bishop': 3.33, 'Rook': 5.63, 'Queen': 9.5}
    def evaluateBoard(self, party):
        ownStrength = 0
        enemysStrength = 0
        if party.mate:
            if activePlayer.color == self.color:
                ownStrength -= 1000
            else:
                enemysStrengh -= 1000
        for y in range(0, 8):
            for x in range(0, 8):
                position = Model.Position(x, y)
                if not party.board.isFree(position):
                    piece = party.board.getPiece(position)
                    if piece.type != 'King':
                        if piece.color == self.color:
                            ownStrength += self.values[piece.type]
                        else:
                            enemysStrength += self.values[piece.type]
        return ownStrength-enemysStrength
    def lookAhead(self, party, depth, end=True):
        moves = party.possibleMoves()
        ratings = {}
        if depth > 0:
            for index in range(len(moves)):
                shadowParty = copy.deepcopy(party)
                if shadowParty.makeMove(moves[index]):
                    shadowParty.changePlayer()
                    strength = self.lookAhead(shadowParty, depth-1, False)
                    ratings[str(index)] = strength
            if len(ratings) == 0:
                return party.activePlayer.color*self.color*1000
            if party.activePlayer.color == self.color:
                strength = max(ratings, key = lambda k: ratings[k])
            else:
                strength = min(ratings, key = lambda k: ratings[k])
            if end:
                return moves[int(strength)][0].oldPosition, moves[int(strength)][0].newPosition
            else:
                return ratings[strength]
        else:
            strength = self.evaluateBoard(party)
            return (strength)