import pygame
from pygame.locals import *

# Cores do Jogo
AQUA = (0, 255, 255)
CORBLU = (100, 149, 237)
FUCHIA = (255, 0, 255)
LIME = (0, 255, 0)
MARRON = (128, 0, 0)
NAVBLU = (0, 0, 128)
OLIVE = (128, 128, 0)
PURPLE = (128, 0, 128)
SILVER = (192, 192, 192)
TEAL = (0, 128, 128)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0  , 255, 0)
BLUE = (0  , 0  , 255)
GRAY = (128, 128, 128)

class Sounds:
    ''' Classe que abstrai e controla o som do jogo '''
    
    def __init__(self):
        ''' Inicializa a classe com os atributos como o endereco de algumas Tracks '''
        pygame.mixer.init()
        self.turn = 0
        self.tracks = [ {'path' : "sons/initial.mp3", 'title': "Prodigy"},
                        {'path' : "sons/back.mp3",    'title': "Under Her Control" } ]        
                        
        # Sons momentaneos
        self.change = pygame.mixer.Sound("sons/coin.wav")
        self.stun = pygame.mixer.Sound("sons/stun.wav")
                 
    def loadBackgroundSound(self, path):
        ''' Inicia a musica de fundo do jogo '''
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1, 0.0)

    def changeMusic(self):
        ''' Troca a musica de fundo '''        
        self.loadBackgroundSound(self.tracks[self.turn]['path'])
        
        if self.turn == len(self.tracks) - 1:
            self.turn = 0
        else:
            self.turn += 1

    def getMusicName(self):
        ''' Retorna o nome da musica pelo indice '''
        return self.tracks[self.turn - 1]['title']

    def stop(self):
        ''' Para a musica do jogo '''
        pygame.mixer.music.stop()



class Draw:
    ''' Classe que tem as funcoes de desenho de textos e imagens do jogo '''

    def __init__(self):
        ''' Inicia os atributos desta classe '''
        # Fontes
        self.mini_text = pygame.font.Font("fonts/ubuntu.ttf", 12)
        self.medium_text = pygame.font.Font("fonts/ubuntu.ttf", 26)
        self.large_text = pygame.font.Font("fonts/ubuntu.ttf", 42)

        # Imagens dos jogadores
        self.gray_orb = pygame.image.load("img/gray_orb")
        self.black_orb = pygame.image.load("img/black_orb")

        # Variaveis do desenho do tabuleiro
        self.espacamento = 15  # Distancia entre cada casa do tabuleiro
        self.tamanho_casa = 50 # Tamanho de cada casa

        # Usa do no efeito pisca-pisca
        self.blinked = False

    def draw(self, surf, obj, x, y):
        ''' Funcao criada para desenhar um item na tela em uma determinada posicao '''        
        rect = obj.get_rect() # Pega o retangulo desse item
        rect.topleft = (x, y)  # Insere as coordenadas x, y no canto superior-esquerdo
        surf.blit(obj, rect) # Insere o item a ser desenhado sobre o retangulo posicionado
            
    def text(self, font, msg, cor):
        ''' Renderiza um texto, usando uma fonte definida no jogo com uma cor e uma mensagem '''
        return font.render(msg, True, cor) 

    def update(self, surf, *sprites):
        ''' Atualiza a tela '''
        
        # Repinta os Sprites atualizados
        for sprite in sprites:
            sprite.draw(surf)

        pygame.display.update()
