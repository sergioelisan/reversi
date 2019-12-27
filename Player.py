# Autor: Serginho
# Dia:   21/12/2010

import random

# Tipos de jogadores
HUMAN = 0
CPU = 1

class Player:
    ''' Classe que abstrai um jogador '''
    
    def __init__(self, nome, cor):
        ''' Construtor do Objeto Player (jogador) que inicializa os atributos deste '''
        self.nome = nome
        self.cor = cor
        self.type = HUMAN
        

    def fazMovimento(self, board, x0, y0):
        ''' Realiza o movimento. Retorna TRUE se conseguir, e FALSE se nao'''
        tilesToFlip = board.isMovimentoValido(self, x0, y0)

        # Se nao tiver pecas para inverter, retorna falso
        if tilesToFlip == False:
            return False

        # Se houverem pecas para inverter, coloca como pecas do jogador a
        # casa onde ele jogou e as casas que ficam ao redor
        board.casas[(x0, y0)] = self        
        for x, y in tilesToFlip:
            board.casas[(x, y)] = self




class Computer(Player):
    ''' Classe que abstrai um jogador computacional '''
    
    def __init__(self, cor, dificuldade):        
        Player.__init__(self, "Computador ", cor)
        self.type = CPU
        self.dificuldade = dificuldade


    def isEsquina(self, x, y, board):
        ''' Verifica se as coordenadas dadas estao na esquina do tabuleiro. Tambem usada
            na estrategia da AI '''
        return  (x == 0 and y == 0) or \
                (x == board.dim[0] - 1 and y == 0) or \
                (x == 0 and y == board.dim[1] - 1) or \
                (x == board.dim[0] - 1  and y == board.dim[1] - 1)


    def AI(self, board):
        ''' Core da AI do computador '''
        possibleMoves = board.getMovimentosValidos(self)
        random.shuffle(possibleMoves)

        # Se tiver jogadas possiveis nas bordas, entao joga lah
        if self.dificuldade not in ['EASY', 'NORMAL']:
            for x, y in possibleMoves:
                if self.isEsquina(x, y, board):
                    return (x, y)

        # Vai atraves de todos os possiveis movimentos em busca do que da mais pontos        
        return board.melhorJogada(self, possibleMoves)
