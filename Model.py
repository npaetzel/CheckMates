import math, copy, time

class Party():
    def __init__(self):
        self.startGame()
    def startGame(self):
        self.board = Board()
        self.activePlayer = self.whitePlayer = Player(-1)
        whitePieces = [Rook(0, 7, -1), Knight(1, 7, -1), Bishop(2, 7, -1), Queen(3, 7, -1), King(4, 7, -1), Bishop(5, 7, -1), Knight(6, 7, -1), Rook(7, 7, -1)] + [Pawn(i, 6, -1) for i in range(8)]
        self.waitingPlayer = self.blackPlayer = Player(+1)
        blackPieces = [Rook(0, 0, 1), Knight(1, 0, 1), Bishop(2, 0, 1), Queen(3, 0, 1), King(4, 0, 1), Bishop(5, 0, 1), Knight(6, 0, 1), Rook(7, 0, 1)] + [Pawn(i, 1, 1) for i in range(8)]
        for piece in whitePieces+blackPieces:
            self.board.addPiece(piece)
        self.check = False
        self.mate = False
    def changePlayer(self):
        cachedPlayer = self.activePlayer
        self.activePlayer = self.waitingPlayer
        self.waitingPlayer = cachedPlayer
    def turn(self, oldPosition, newPosition):
        self.possibleMoves()
        piece = self.board.getPiece(oldPosition)
        if piece.color == self.activePlayer.color:
            if self.board.hasField(newPosition):
                moves = piece.move(newPosition, self.board)
                if self.makeMove(moves):
                    self.changePlayer()
                    self.checkStatus()
                    return True
            return False
    def makeMove(self, moves):
        if len(moves) != 0:
            captured = None
            if moves[0].capturePosition != None:
                captured = self.board.getPiece(moves[0].capturePosition)
                self.board.removePieceAt(moves[0].capturePosition)
            hasMoved = []
            for forwardIndex in range(len(moves)):
                hasMoved.append(self.board.getPiece(moves[forwardIndex].oldPosition).hasMoved)
                self.board.move(moves[forwardIndex].oldPosition, moves[forwardIndex].newPosition)
                if self.board.inCheck(self.activePlayer.color):   
                    if captured != None:
                        self.board.addPiece(captured)
                    for backwardIndex in range(forwardIndex, -1, -1):
                        self.board.move(moves[backwardIndex].newPosition, moves[backwardIndex].oldPosition)  
                        self.board.getPiece(moves[backwardIndex].oldPosition).hasMoved = hasMoved[backwardIndex]
                    return False
            return True
    def checkStatus(self):
        if self.board.inCheck(self.activePlayer.color):
            self.check = True
            if self.inMate():
                self.mate = True
        else:
            self.check = False
    def inMate(self):
        moves = self.possibleMoves()
        for move in moves:
            shadowParty = copy.deepcopy(self)
            shadowParty.makeMove(move)
            if not shadowParty.board.inCheck(self.activePlayer.color):
                return False
        return True
    def possibleMoves(self):
        moves = []
        for col in self.board.fields:
            for field in col:
                if field != None and field.color == self.activePlayer.color:
                    fieldsMoves = field.possibleMoves(self.board)

                    if len(fieldsMoves) > 0:
                        for move in fieldsMoves:
                            if len(move) > 0:
                                moves.append(move)
        return moves

class Board():
    def __init__(self):
        self.fields = [[None for col in range(0,8)] for row in range(0,8)]
    def addPiece(self, piece):
        self.fields[piece.position.y][piece.position.x] = piece
    def removePieceAt(self, position):
        self.fields[position.y][position.x] = None
    def getPiece(self, position):
        return self.fields[position.y][position.x]
    def hasField(self, position):
        if position.x < 0 or position.x > 7 or position.y < 0 or position.y > 7:
            return False
        return True
    def isFree(self, position):
        if self.fields[position.y][position.x] == None:
            return True
        return False
    def move(self, oldPosition, newPosition):
        piece = self.fields[oldPosition.y][oldPosition.x]
        self.fields[oldPosition.y][oldPosition.x] = None
        self.fields[newPosition.y][newPosition.x] = piece
        piece.position = newPosition
        piece.hasMoved = True
    def canBeAttackedBy(self, positions, activeColor, types, dependent=True):
        for position in positions:
            if position != None and self.hasField(position):
                piece = self.getPiece(position)
                if piece != None:
                    if piece.color != activeColor and types.count(piece.type):
                        return True
                    elif dependent:
                        break
        return False
    def inCheck(self, activeColor):
        for col in self.fields:
            for field in col:
                if field != None and field.type == 'King' and field.color == activeColor:
                    king = field
        if (self.canBeAttackedBy([Position(x, king.position.y) for x in range(king.position.x+1, 8)], activeColor, ['Queen', 'Rook']) or
            self.canBeAttackedBy([Position(x, king.position.y) for x in range(king.position.x-1, -1, -1)], activeColor, ['Queen', 'Rook']) or
            self.canBeAttackedBy([Position(king.position.x, y) for y in range(king.position.y+1, 8)], activeColor, ['Queen', 'Rook']) or
            self.canBeAttackedBy([Position(king.position.x, y) for y in range(king.position.y-1, -1, -1)], activeColor, ['Queen', 'Rook']) or
            self.canBeAttackedBy([Position(king.position.x+step, king.position.y+step) for step in range(1, 8)], activeColor, ['Queen', 'Bishop']) or
            self.canBeAttackedBy([Position(king.position.x-step, king.position.y-step) for step in range(1, 8)], activeColor, ['Queen', 'Bishop']) or
            self.canBeAttackedBy([Position(king.position.x+step, king.position.y-step) for step in range(1, 8)], activeColor, ['Queen', 'Bishop']) or
            self.canBeAttackedBy([Position(king.position.x-step, king.position.y+step) for step in range(1, 8)], activeColor, ['Queen', 'Bishop']) or
            self.canBeAttackedBy([Position(king.position.x-2, king.position.y-1), Position(king.position.x-2, king.position.y+1), 
                Position(king.position.x-1, king.position.y-2), Position(king.position.x-1, king.position.y+2),
                Position(king.position.x+1, king.position.y-2), Position(king.position.x+1, king.position.y+2),
                Position(king.position.x+2, king.position.y-1), Position(king.position.x+2, king.position.y+1)], activeColor, ['Knight'], False) or
            self.canBeAttackedBy([Position(king.position.x-1, king.position.y+activeColor), Position(king.position.x+1, king.position.y+activeColor)], activeColor, ['Pawn'], False) or
            self.canBeAttackedBy([Position(king.position.x+stepX, king.position.y+stepY) for stepX in range(-1, 2) for stepY in range(-1, 2)], activeColor, ['King'], False)):
            return True

                        


class Piece():
    def __init__(self, x, y, color=-1):
        self.hasMoved = False
        self.position = Position(x, y)
        self.color = color
        self.type = type(self).__name__
    def move(self, newPosition, board):
        pass
    def possibleMoves(self, board):
        pass
class King(Piece):
    def move(self, newPosition, board):
        if board.hasField(newPosition):
            relativePosition = newPosition-self.position
            if (abs(relativePosition.x) == 1 or abs(relativePosition.y) == 1) and abs(relativePosition.x) < 2 and abs(relativePosition.y) <2:
                if board.isFree(newPosition):
                    return [Move(self.position, newPosition)]
                elif board.getPiece(newPosition).color != self.color:
                    return [Move(self.position, newPosition, newPosition)]
            elif abs(relativePosition.x) == 2 and relativePosition.y == 0 and not board.inCheck(self.color) and self.hasMoved == False:
                if relativePosition.x == -2:
                    #queenside castling
                    rook = board.getPiece(Position(0, self.position.y))
                    if rook != None and rook.type == 'Rook' and rook.color == self.color:
                        return [Move(self.position, Position(3, self.position.y)), Move(Position(3, self.position.y), newPosition), Move(rook.position, Position(3, self.position.y))]
                elif relativePosition.x == 2:
                    #kingside castling
                    rook = board.getPiece(Position(7, self.position.y))
                    if rook != None and rook.type == 'Rook' and rook.color == self.color:
                        return [Move(self.position, Position(5, self.position.y)), Move(Position(5, self.position.y), newPosition), Move(rook.position, Position(5, self.position.y))]
        return []
    def possibleMoves(self, board):
        moves = []
        for x in range(-1, 1):
            for y in range(-1, 1):
                if x != 0 and y != 0:
                    newPosition = self.position + Position(x, y)
                    moves.append(self.move(newPosition, board))
        return moves

class Queen(Piece):
    def move(self, newPosition, board):
        if board.hasField(newPosition):
            relativePosition = newPosition-self.position
            if abs(relativePosition.x) > 0 and relativePosition.y == 0:
                for stepX in range(int(math.copysign(1, relativePosition.x)), relativePosition.x, int(math.copysign(1, relativePosition.x))):
                    if not board.isFree(self.position + Position(stepX, 0)):
                        return []
            elif relativePosition.x == 0 and abs(relativePosition.y) > 0:
                for stepY in range(int(math.copysign(1, relativePosition.y)), relativePosition.y, int(math.copysign(1, relativePosition.y))):
                    if not board.isFree(self.position + Position(0, stepY)):
                        return []
            elif abs(relativePosition.x) == abs(relativePosition.y):
                for step in range(1, abs(relativePosition.x)):
                    if not board.isFree(self.position + Position(int(math.copysign(step, relativePosition.x)), int(math.copysign(step, relativePosition.y)))):
                        return []
            else:
                return []
            if board.getPiece(newPosition) == None:
                return [Move(self.position, newPosition)]
            elif board.getPiece(newPosition).color != self.color:
                return [Move(self.position, newPosition, newPosition)]
        return []
    def possibleMoves(self, board):
        moves = []
        for x in range(0, 8):
            newPosition = Position(x, self.position.y)
            moves.append(self.move(newPosition, board))
        for y in range(8, 0):
            newPosition = Position(self.x, y)
            moves.append(self.move(newPosition, board))
        for xy in range(1, max(self.position.x+1+1, 8-self.position.x, self.position.y+1, 8-self.position.y)):
            newPosition = self.position + Position(xy, xy)
            moves.append(self.move(newPosition, board))
            newPosition = self.position + Position(-xy, xy)
            moves.append(self.move(newPosition, board))
            newPosition = self.position + Position(xy, -xy)
            moves.append(self.move(newPosition, board))
            newPosition = self.position + Position(-xy, -xy)
            moves.append(self.move(newPosition, board))
        return moves
class Bishop(Piece):
    def move(self, newPosition, board):
        if board.hasField(newPosition):
            relativePosition = newPosition-self.position
            if abs(relativePosition.x) == abs(relativePosition.y):
                for step in range(1, abs(relativePosition.x)):
                    if not board.isFree(self.position + Position(int(math.copysign(step, relativePosition.x)), int(math.copysign(step, relativePosition.y)))):
                        return []
                if board.isFree(newPosition):
                    return [Move(self.position, newPosition)]
                elif board.getPiece(newPosition).color != self.color:
                    return [Move(self.position, newPosition, newPosition)]
        return []
    def possibleMoves(self, board):
        moves = []
        for xy in range(1, max(self.position.x+1+1, 8-self.position.x, self.position.y+1, 8-self.position.y)):
            newPosition = self.position + Position(xy, xy)
            moves.append(self.move(newPosition, board))
            newPosition = self.position + Position(-xy, xy)
            moves.append(self.move(newPosition, board))
            newPosition = self.position + Position(xy, -xy)
            moves.append(self.move(newPosition, board))
            newPosition = self.position + Position(-xy, -xy)
            moves.append(self.move(newPosition, board))
        return moves
class Knight(Piece):
    def move(self, newPosition, board):
        if board.hasField(newPosition):
            relativePosition = newPosition-self.position
            if (abs(relativePosition.x) == 1 and abs(relativePosition.y) == 2) or (abs(relativePosition.x) == 2 and abs(relativePosition.y) == 1):
                if board.hasField(newPosition):
                    if board.isFree(newPosition):
                        return [Move(self.position, newPosition)]
                    elif board.getPiece(newPosition).color != self.color:
                        return [Move(self.position, newPosition, newPosition)]
        return []
    def possibleMoves(self, board):
        moves = []
        moves.append(self.move(self.position + Position(2, 1), board))
        moves.append(self.move(self.position + Position(2, -1), board))
        moves.append(self.move(self.position + Position(-2, 1), board))
        moves.append(self.move(self.position + Position(-2, -1), board))
        moves.append(self.move(self.position + Position(1, 2), board))
        moves.append(self.move(self.position + Position(1, -2), board))
        moves.append(self.move(self.position + Position(-1, 2), board))
        moves.append(self.move(self.position + Position(-1, -2), board))
        return moves
class Rook(Piece):
    def move(self, newPosition, board):
        if board.hasField(newPosition):
            relativePosition = newPosition-self.position
            if abs(relativePosition.x) > 0 and relativePosition.y == 0:
                for stepX in range(int(math.copysign(1, relativePosition.x)), relativePosition.x, int(math.copysign(1, relativePosition.x))):
                    if not board.isFree(self.position+Position(stepX, 0)):
                        return []
            elif relativePosition.x == 0 and abs(relativePosition.y) > 0:
                for stepY in range(int(math.copysign(1, relativePosition.y)), relativePosition.y, int(math.copysign(1, relativePosition.y))):
                    if not board.isFree(self.position+Position(0, stepY)):
                        return []
            else:
                return []
            if board.getPiece(newPosition) == None:
                return [Move(self.position, newPosition)]
            elif board.getPiece(newPosition).color != self.color:
                return [Move(self.position, newPosition, newPosition)]
        return []
    def possibleMoves(self, board):
        moves = []
        for x in range(0, 8):
            newPosition = Position(x, self.position.y)
            moves.append(self.move(newPosition, board))
        for y in range(8, 0):
            newPosition = Position(self.position.x, y)
            moves.append(self.move(newPosition, board))
        return moves        
class Pawn(Piece):
    def __init__(self, x, y, color=-1):
        super().__init__(x, y, color)
        self.passable = False        
    def move(self, newPosition, board):
        if board.hasField(newPosition):
            relativePosition = newPosition-self.position
            if relativePosition.x == 0:
                if relativePosition.y*self.color == 1:
                    if board.isFree(newPosition):
                        return [Move(self.position, newPosition, passable=False)]
                elif relativePosition.y*self.color == 2 and ((self.position.y == 6 and self.color == -1) or (self.position.y == 1 and self.color == 1)):
                    if board.isFree(self.position + Position(0, self.color)) and board.isFree(newPosition):
                        return [Move(self.position, newPosition, passable=True)]
            elif abs(relativePosition.x) == 1 and relativePosition.y*self.color == 1:
                if not board.isFree(newPosition):
                    if board.getPiece(newPosition).color != self.color:
                        return [Move(self.position, newPosition, newPosition, passable=False)]
                elif not board.isFree(self.position + Position(relativePosition.x, 0)) and board.getPiece(self.position + Position(relativePosition.x, 0)).color != self.color:
                    passablePawn = board.getPiece(self.position + Position(relativePosition.x, 0))
                    if passablePawn != None and passablePawn.type == 'Pawn' and passablePawn.passable == True:
                        return [Move(self.position, newPosition, self.position + Position(relativePosition.x, 0), passable=False)]
        return []
    def possibleMoves(self, board):
        moves = []
        moves.append(self.move(self.position + Position(0, self.color), board))
        moves.append(self.move(self.position + Position(0, self.color*2), board))
        moves.append(self.move(self.position + Position(-1, self.color), board))
        moves.append(self.move(self.position + Position(1, self.color), board))    
        return moves

class Player():
    def __init__(self, color=-1):
        self.color = color

class Position():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def relativePosition(self, position):
        return Position(position.x-self.x, position.y-self.y)
    def __add__(self, summand):
        return Position(self.x+summand.x, self.y+summand.y)
    def __sub__(self, subtrahend):
        return Position(self.x-subtrahend.x, self.y-subtrahend.y)
    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

class Move():
    def __init__(self, oldPosition, newPosition, capturePosition=None, passable=None):
        self.oldPosition = oldPosition
        self.newPosition = newPosition
        self.capturePosition = capturePosition
        self.passable = passable
    def __str__(self):
        return str(self.oldPosition) + ' to ' + str(self.newPosition) + ' capturing ' + str(self.capturePosition)
