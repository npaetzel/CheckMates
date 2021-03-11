class Language():
    def __init__(self, name):
        self.name = name
        self.vocabulary = {}
    def addWord(self, indexWord, translation):
        self.vocabulary[indexWord] = translation
    def getWord(self, indexWord):
        return self.vocabulary[indexWord]



languages = {}
en = Language('English')
en.addWord('pawn', 'Pawn')
en.addWord('rook', 'Rook')
en.addWord('knight', 'Knight')
en.addWord('bishop', 'Bishop')
en.addWord('queen', 'Queen')
en.addWord('king', 'King')
en.addWord('en passant', 'en passant')
en.addWord('castling', 'castling')
en.addWord('check', 'Check')
en.addWord('checkmate', 'Check Mate')
en.addWord('local', 'Local Player')
en.addWord('cpu', 'CPU Player')
en.addWord('network', 'Network Player')


de = Language('Deutsch')
de.addWord('pawn', 'Bauer')
de.addWord('rook', 'Turm')
de.addWord('knight', 'Springer')
de.addWord('bishop', 'Läufer')
de.addWord('queen', 'Königin')
de.addWord('king', 'König')
de.addWord('en passant', 'en passant')
de.addWord('castling', 'Rochade')
de.addWord('check', 'Schach')
de.addWord('checkmate', 'Schach Matt')
de.addWord('local', 'Lokaler Spieler')
de.addWord('cpu', 'KI-Spieler')
de.addWord('network', 'Netzwerkspieler')

languages[en.name] = en
languages[de.name] = de
