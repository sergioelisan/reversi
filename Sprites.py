# Autor: Serginho
# Dia:   21/12/2010

import pygame
from pygame.locals import *
from Multimedia import GRAY, WHITE, BLACK, RED

class Tabuleiro(pygame.sprite.Sprite):
    ''' Sprite que eh a representacao grafica do tabuleiro '''

    def __init__(self, espacamento, tamanho_casa, dim, x, y):
        pygame.sprite.Sprite.__init__(self)
        area = (dim[0] * tamanho_casa, dim[1] * tamanho_casa)        
        self.espacamento = espacamento
        self.tamanho_casa = tamanho_casa        
        self.null = pygame.image.load("img/null")
        self.advice = pygame.image.load("img/advice")
        self.image = pygame.Surface(area)
        self.image.fill     (WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, board, p1, p2):
        ''' Atualiza o Tabuleiro '''
        self.board = board        
        self.p1 = p1
        self.p2 = p2
        self.renderizaBoard()

    def pintaCasa(self, cor, x, y):
        ''' Pinta cada casinha de acordo com a cor do jogador '''
        t = self.tamanho_casa
        e = self.espacamento
        self.image.blit(self.null, (x * t + e / 3, y * t + e / 3))
        self.image.blit(cor, (x * t + e / 3, y * t + e / 3))
    
    def renderizaBoard(self):
        ''' Desenha na GUI o objeto Board e seus atributos '''
        
        # Atributos da Representacao Grafica do Tabuleiro
        e = self.espacamento
        casa = self.board.casas
        t = self.tamanho_casa
        corLinhas = GRAY              # Cor das linhas
        dim = self.board.dim          # Dimensoes do Board
        p1 = self.p1
        p2 = self.p2        
        self.raio = t / 2             # Tamanho do Raio de cada peca        

        for x in range(dim[0]):
            # Pinta as linhas verticais
            if x != 0: pygame.draw.line(self.image, corLinhas, (x * t, e), (x * t, dim[1] * t))
            
            for y in range(dim[1]):              
                if   casa[(x, y)] == p1:     self.pintaCasa(p1.cor, x, y)                  
                elif casa[(x, y)] == p2:     self.pintaCasa(p2.cor, x, y)
                elif casa[(x, y)] == 'DICA': self.pintaCasa(self.advice, x, y)
                else:                        self.pintaCasa(self.null , x, y)

                # Pinta as linhas horizontais
                if y != 0: pygame.draw.line(self.image, corLinhas, (e, y * t), (dim[0] * t, y * t))



class Image(pygame.sprite.Sprite):
    ''' Sprite de uma imagem'''
    
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.update(x, y, img)        

    def update(self, x, y, img):
        ''' Atualiza os dados de alerta '''
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)




class Text(pygame.sprite.Sprite):
    ''' Sprite que eh a representacao grafica de um texto '''
    
    def __init__(self, x, y, font_size, cor, mensagem):
        pygame.sprite.Sprite.__init__(self)
        self.cor = cor
        self.msg = mensagem
        self.font = pygame.font.Font("fonts/ubuntu.ttf", font_size)
        self.image = self.font.render(mensagem, True, self.cor)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, msg, cor = GRAY):
        ''' Atualiza os dados de alerta '''
        self.image = self.font.render(msg, True, cor)

    def updateColor(self, cor):        
        ''' Atualiza apenas as cores do texto '''
        if cor == 0:
            cor = self.cor
        self.image = self.font.render(self.msg, True, cor)

    def getRect(self):
        return self.rect
   
   
        

class Cronometer(Text):
    ''' Sprite que eh a representacao grafica de um cronometro '''
    
    def __init__(self, x, y):
        Text.__init__(self, x, y, 30, GRAY, "")

    def update(self, tempo):
        ''' Atualiza os relogio '''
        if int(tempo) <= 5:
            cor = RED
        else:
            cor = GRAY
            
        self.image = self.font.render(tempo, True, cor)
