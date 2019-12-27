# Autor: Serginho
# Dia:   21/12/2010

class Board:
    ''' Classe que abstrai um tabuleiro. Aqui nao ha representacao grafica, apenas uma estrutura de dados e metodos
        de manipulacao dessa estrutura. Cabe a classe Reversi implementar a GUI usando essa estrutura

        O Tabuleiro aqui eh representado por um dicionario, em que cada CHAVE eh uma tupla que corresponde a uma
        coordenada de casa, e armazena o jogador de cada casa.

        Tambem tem os metodos para verificacao de disponibilidade ou movimento valido das pecas nas casas
        '''
    
    def __init__(self, dimensoes, p1, p2):
        self.dim = dimensoes
        self.novoTabuleiro(p1, p2)
        self.p1 = p1
        self.p2 = p2


    def getPontos(self):
        ''' Pega a estrutura de dados que representa o tabuleiro e conta quantos pontos
            cada jogador tem nela '''
        p1_score = 0
        p2_score = 0        
        board = self.casas
        
        for x in range(self.dim[0]):
            for y in range(self.dim[1]):
                if board[(x, y)] == self.p1: p1_score += 1
                if board[(x, y)] == self.p2: p2_score += 1
                
        return {self.p1.nome : p1_score, self.p2.nome : p2_score}


    def melhorJogada(self, player, possibleMoves):
        ''' Usada pela inteligencia artificial e pelo joguinho quando esta no modo EASY '''

        bestMove = False
        bestScore = -1
        for x, y in possibleMoves:
            dupeBoard = self.getCopiaTabuleiro()
            player.fazMovimento(dupeBoard, x, y)
            score = dupeBoard.getPontos()[player.nome]
            
            if score > bestScore:
                bestMove = (x, y)
                bestScore = score

        return bestMove
    

    def getCopiaTabuleiro(self):
        ''' Faz uma copia do tabuleiro '''
        copia = Board(self.dim, self.p1, self.p2)
        copia.casas = {}
        
        for x in range(self.dim[0]):
            for y in range(self.dim[1]):
                copia.casas[(x, y)] = self.casas[(x, y)]

        return copia


    def novoTabuleiro(self, p1, p2):
        ''' Inicializa a estrutura dicionario que armazenara as informacoes das casas do tabuleiro '''
        self.casas = {}
        for x in range(self.dim[0]):
            for y in range(self.dim[1]):
                self.casas[(x, y)] = None

        # Inicia o tabuleiro com 4 pecas iniciais localizadas no centro deste
        self.casas[self.dim[0] / 2, self.dim[1] / 2    ] = p1
        self.casas[self.dim[0] / 2 - 1, self.dim[1] / 2    ] = p2
        self.casas[self.dim[0] / 2 - 1, self.dim[1] / 2 - 1] = p1
        self.casas[self.dim[0] / 2, self.dim[1] / 2 - 1] = p2
        

    def isOnBoard(self, x, y):
        ''' Verifica se as coordenadas estao dentro do tabuleiro '''
        return (x >= 0 and x < self.dim[0]) and (y >= 0 and y < self.dim[1])

    
    def getMovimentosValidos(self, tile):
        ''' Retorna uma lista com possiveis jogadas validas'''
        validos = []

        for x in range(self.dim[0]):
            for y in range(self.dim[1]):
                if self.isMovimentoValido(tile, x, y) != False:
                    validos.append([x, y])
        return validos


    def isMovimentoValido(self, tile, x0, y0):
        ''' Metodo para averiguar se a jogada eh valida'''
        
        board = self.casas

        if board[(x0, y0)] not in [None, 'DICA'] or not self.isOnBoard(x0, y0):
            return False

        board[(x0, y0)] = tile # Coloca temporariamente a jogada na casa

        if tile == self.p1:
            otherTile = self.p2
        else:
            otherTile = self.p1

        tilesToFlip = []
        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            
            x, y = x0, y0
            x += xdirection # Primento passo na direcao
            y += ydirection # Primento passo na direcao
            
            if self.isOnBoard(x, y) and board[(x, y)] == otherTile:
                x += xdirection
                y += ydirection

                if not self.isOnBoard(x, y):
                    continue

                while board[(x, y)] == otherTile:
                    x += xdirection
                    y += ydirection
                    if not self.isOnBoard(x, y):
                        break
                    
                if not self.isOnBoard(x, y):
                    continue
                
                if board[(x, y)] == tile:
                    while True:
                        x -= xdirection
                        y -= ydirection
                        if x == x0 and y == y0:
                            break
                        tilesToFlip.append([x, y])

        board[(x0, y0)] = None
        
        if len(tilesToFlip) == 0:
            return False
        
        return tilesToFlip
