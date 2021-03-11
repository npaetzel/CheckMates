import tkinter, tkinter.font, Lang

class View(tkinter.Canvas):
    def __init__(self, root):
        self.root = root

        self.refreshValues()     
        self.loadFiles()
        self.inGame = False

        self.fields = None
        self.highlighted = None

        self.root.resizable(False, False)
        self.root.title('CheckMates')
        super().__init__(self.root, height=self.height, width=self.width)
        super().focus_set()
        self.bind('<Button-1>', self.onClick)

        self.pack()
    def refreshValues(self):
        self.zoom = 0.6
        screenHeight = self.root.winfo_screenheight()
        self.fieldsize = int((screenHeight-100)/8)
        self.boardsize = self.fieldsize*8

        self.height = self.root.winfo_screenheight()
        self.width = self.height
        if self.zoom <= 1 and self.zoom > 0:
            self.boardsize = int(self.boardsize*self.zoom)
            self.fieldsize = int(self.fieldsize*self.zoom)
            self.height = int(self.height*self.zoom)
            self.width = int(self.width*self.zoom)
        
        self.menuFont = tkinter.font.Font(size=12)
        self.buttonColor = '#ff0000'

        self.wp = RectArea(self.width*0.2, self.height*0.2, self.width*0.4, self.height*0.3)
        self.bp = RectArea(self.width*0.6, self.height*0.2, self.width*0.8, self.height*0.3)
        self.wt = RectArea(self.width*0.2, self.height*0.45, self.width*0.4, self.height*0.5)
        self.bt = RectArea(self.width*0.6, self.height*0.45, self.width*0.8, self.height*0.5)
        self.sg = RectArea(self.width*0.35, self.height*0.7, self.width*0.65, self.height*0.8)
    def loadFiles(self):
        imgDir = './img/'
        self.whitePawn = tkinter.PhotoImage(file=imgDir + 'pawnW.png')
        self.whiteRook = tkinter.PhotoImage(file=imgDir + 'rookW.png')
        self.whiteKnight = tkinter.PhotoImage(file=imgDir + 'knightW.png')
        self.whiteBishop = tkinter.PhotoImage(file=imgDir + 'bishopW.png')
        self.whiteQueen = tkinter.PhotoImage(file=imgDir + 'queenW.png')
        self.whiteKing = tkinter.PhotoImage(file=imgDir + 'kingW.png')

        self.blackPawn = tkinter.PhotoImage(file=imgDir + 'pawnB.png')
        self.blackRook = tkinter.PhotoImage(file=imgDir + 'rookB.png')
        self.blackKnight = tkinter.PhotoImage(file=imgDir + 'knightB.png')
        self.blackBishop = tkinter.PhotoImage(file=imgDir + 'bishopB.png')
        self.blackQueen = tkinter.PhotoImage(file=imgDir + 'queenB.png')
        self.blackKing = tkinter.PhotoImage(file=imgDir + 'kingB.png')

        self.icons = {
            'white': {
                'Pawn': self.whitePawn,
                'Rook': self.whiteRook,
                'Knight': self.whiteKnight,
                'Bishop': self.whiteBishop,
                'Queen': self.whiteQueen,
                'King': self.whiteKing
            },
            'black': {
                'Pawn': self.blackPawn,
                'Rook': self.blackRook,
                'Knight': self.blackKnight,
                'Bishop': self.blackBishop,
                'Queen': self.blackQueen,
                'King': self.blackKing
            }
        }
    def onClick(self, event):
        self.root.event_generate('<<sub>>')
        if self.inGame:
            if event.x < self.boardsize and event.y < self.boardsize:
                    x = event.x//self.fieldsize
                    y = event.y//self.fieldsize
                    self.root.event_generate('<<ClickedField>>', x=x, y=y)
        else:
            if self.wt.onButton(event.x, event.y):
                #change type of white player
                self.root.event_generate('<<ChangeWhitePlayer>>')
                pass
            elif self.bt.onButton(event.x, event.y):
                #change type of black player
                self.root.event_generate('<<ChangeBlackPlayer>>')
                pass
            elif self.sg.onButton(event.x, event.y):
                self.root.event_generate('<<StartGame>>')
    def redraw(self, gameActive=False):
        self.inGame = gameActive
        self.delete(tkinter.ALL)
        if gameActive:
            self.drawFields()
            self.drawPieces()
            self.hightlightField()
        else:
            self.drawMenu()
    def drawFields(self):
        for i in range(9):
            super().create_line(0, i*self.fieldsize, self.boardsize, i*self.fieldsize)
            super().create_line(i*self.fieldsize, 0, i*self.fieldsize, self.boardsize)
    def drawPieces(self):
        for col in self.fields:
            for field in col:
                if field != None:
                    player = 'white'
                    if field.color == 1:
                        player = 'black'
                    image = self.icons[player][type(field).__name__]
                    super().create_image((0.5+field.position.x)*self.fieldsize, (0.5+field.position.y)*self.fieldsize, image=image)
    def hightlightField(self):
        if self.highlighted != None:
            marginO = 0.05*self.fieldsize
            marginI = 0.1*self.fieldsize
            color = '#2E64FE'
            left = self.highlighted.x*self.fieldsize
            top = self.highlighted.y*self.fieldsize
            right = (1+self.highlighted.x)*self.fieldsize
            bottom = (1+self.highlighted.y)*self.fieldsize
            super().create_rectangle(left+marginO, top+marginO, left+marginI, bottom-marginO, fill=color, outline=color)
            super().create_rectangle(right-marginI, top+marginO, right-marginO, bottom-marginO, fill=color, outline=color)
            super().create_rectangle(left+marginO, top+marginO, right-marginO, top+marginI, fill=color, outline=color)
            super().create_rectangle(left+marginO, bottom-marginI, right-marginO, bottom-marginO, fill=color, outline=color)
    def drawMenu(self):
        super().create_rectangle(self.wp.x1, self.wp.y1, self.wp.x2, self.wp.y2, fill=self.buttonColor)
        super().create_rectangle(self.bp.x1, self.bp.y1, self.bp.x2, self.bp.y2, fill=self.buttonColor)
        super().create_text(self.wp.x1+(self.wp.x2-self.wp.x1)/2 , self.wp.y1+(self.wp.y2-self.wp.y1)/2, text="White Player", font=self.menuFont)
        super().create_text(self.bp.x1+(self.bp.x2-self.bp.x1)/2 , self.bp.y1+(self.bp.y2-self.bp.y1)/2, text="Black Player", font=self.menuFont)

        super().create_rectangle(self.width*0.2, self.height*0.45, self.width*0.4, self.height*0.5, fill=self.buttonColor)
        super().create_rectangle(self.width*0.6, self.height*0.45, self.width*0.8, self.height*0.5, fill=self.buttonColor)
        super().create_text(self.width*0.3, self.height*0.475, text=Lang.languages['Deutsch'].getWord(self.whitePlayerType), font=self.menuFont)
        super().create_text(self.width*0.7, self.height*0.475, text=Lang.languages['Deutsch'].getWord(self.blackPlayerType), font=self.menuFont)

        super().create_rectangle(self.width*0.35, self.height*0.7, self.width*0.65, self.height*0.8, fill=self.buttonColor)
        super().create_text(self.width*0.5, self.height*0.75, text='START GAME', font=self.menuFont)

class RectArea():
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    def onButton(self, x, y):
        if x > self.x1 and x < self.x2 and y > self.y1 and y < self.y2:
            return True
        return False