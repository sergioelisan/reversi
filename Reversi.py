# -------------------------------------- #
# Joguinho de Reversi Orientado a Objeto #
# Autor: Serginho                        #
# Dia:   21/12/2010                      #
# -------------------------------------- #

# Modulos do sistema
import pygame
import random
import time
from pygame.locals import *
from sys import exit

# Modulos do jogo
from Board import *
from Multimedia import *
from Player import *
from Ranking import *
from Sprites import *
from Resources import *


class Reversi:
    ''' Classe que abstrai um jogo de Reversi!
        Essa classe tem como atributos dois jogadores (que podem ser 2 Player's, ou 1 Player e 1 Computer
        ou 2 Computer's), um tabuleiro (representado pela classe Board) e metodos que representam as regras
        e operacoes do jogo. '''
    
    def __init__(self):
        ''' Construtor que inicializa as variaveis e os metodos de construcao do jogo
            RECEBE uma tupla que sera a representacao das dimensoes do tabuleiro '''
        # Inicia o Pygame, o Mixer e o relogio principal
        pygame.init()
        self.clock = pygame.time.Clock()
        
        # Define a dimensao da janela, do tabuleiro e inicia o relogio
        self.RES = (800, 600)
                
        # Inicializa as funcoes multimedia do jogo
        self.sound = Sounds()
        self.draw = Draw()

        # Opcoes do jogo
        self.loadOptions()
        
        # Inicia o jogo
        self.initGUI()
        self.abertura()


    def loadOptions(self):
        ''' Carregas as opcoes salvas do jogo '''
        #ReversiIO("res/options.dat").read()
        opcoes = {} 
        
        if opcoes.keys() in ['fullscreen', 'dificuldade']:
            self.fullscreen  = opcoes['fullscreen']
            self.dificuldade = opcoes['dificuldade']
        else:            
            self.fullscreen  = 0
            self.dificuldade = "EASY"

    def initGUI(self):
        ''' Cria a superficie principal '''        
        if self.fullscreen:
            mode = FULLSCREEN
        else:
            mode = 0
            
        self.surface = pygame.display.set_mode(self.RES, mode, 32)
        pygame.display.set_caption("United tm - Reversi against Humanity")


    def opcoes(self):
        ''' Tela de opcoes '''
        def changeSelectionColor():
            if self.dificuldade == 'EASY':
                dif_fac.cor  = selectedColor
                dif_nor.cor  = unselectedColor
                dif_hell.cor = unselectedColor
                
            elif self.dificuldade == 'NORMAL':
                dif_fac.cor  = unselectedColor
                dif_nor.cor  = selectedColor
                dif_hell.cor = unselectedColor
                
            elif self.dificuldade == 'FROM_HELL':
                dif_fac.cor  = unselectedColor
                dif_nor.cor  = unselectedColor
                dif_hell.cor = selectedColor

            if self.fullscreen:
                full_yes.cor = selectedColor
                full_no.cor = unselectedColor
            else:
                full_yes.cor = unselectedColor
                full_no.cor = selectedColor

            if self.sound.getMusicName() == self.sound.tracks[0]['title']:
                mus_prod.cor = selectedColor
                mus_under.cor = unselectedColor
            else:
                mus_prod.cor = unselectedColor
                mus_under.cor = selectedColor

        # Variaveis pra facilitar a nossa vida
        draw   = self.draw
        sfc    = self.surface
        difc   = self.dificuldade
        fulls  = self.fullscreen
        actMus = self.sound.tracks[0]['title']
        
        selectedColor   = CORBLU
        unselectedColor = BLACK

        opt = Text(15, 15, 30, GRAY, "Opcoes do Reversi")
        
        dif         = Text(15, 110, 20, GRAY, "Dificuldade")	
        dif_fac     = Text(200, 110, 20, selectedColor if difc == "EASY" else unselectedColor, "Facinho!")
        dif_nor     = Text(300, 110, 20, selectedColor if difc == "NORMAL" else unselectedColor, "Normal")
        dif_hell    = Text(400, 110, 20, selectedColor if difc == "FROM_HELL" else unselectedColor, "From Hell")
        
        full        = Text(15, 165, 20, GRAY, "Modo")	
        full_yes    = Text(200, 165, 20, selectedColor if fulls else unselectedColor, "Fullscreen")	
        full_no     = Text(325, 165, 20, selectedColor if not fulls else unselectedColor, "Janela")	

        mus         = Text(15,  220, 20, GRAY, "Tracks")
        mus_prod    = Text(200, 220, 20, selectedColor if actMus == self.sound.getMusicName() else unselectedColor, "Prodigy")
        mus_under   = Text(200, 260, 20, selectedColor if actMus != self.sound.getMusicName() else unselectedColor, "Under Her Control")
        
        rank 	    = Text(15, 310, 20, GRAY, "Salvar opcoes?")
        rank_yes    = Text(200, 310, 20, BLACK, "Sim")

        sprite_group = pygame.sprite.Group(opt, dif, dif_fac, dif_nor, dif_hell,
                                           mus, mus_prod, mus_under,
                                           full, full_yes, full_no,
                                           rank, rank_yes)

        quit = False
        musicPlaying = True
                
        while not quit:
            self.clock.tick(10) # Segura o jogo em 10 quadros por segundo            
            changeSelectionColor()            

            for event in pygame.event.get():    
                # Se o usuario clicar no botao de 'sair'
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    quit = True
                elif event.type == KEYDOWN:                                
                    # Para ou recomeca a Musica de fundo 
                    if event.key == ord('p'):
                        if musicPlaying:
                            self.sound.stop()
                            musicPlaying = False
                        else:
                            self.sound.changeMusic()
                            musicPlaying = True                                      
                            # Muda a musica de fundo sendo tocada        
                    elif event.key == ord('t'):
                        self.sound.changeMusic()

                # Usa o motion do mouse
                elif event.type == MOUSEMOTION:
                    posx, posy = event.pos
                    overColor = GRAY
                    
                    if (posx >= 200 and posx <= 276) and (posy <= 137 and posy >= 108):
                        dif_fac.updateColor(overColor)
                    else:
                        dif_fac.updateColor(0)
                    
                    if (posx >= 300 and posx <= 375) and (posy <= 137 and posy >= 108):
                        dif_nor.updateColor(overColor)
                    else:
                        dif_nor.updateColor(0)
                                        
                    if (posx >= 400 and posx <= 495) and (posy <= 137 and posy >= 108):
                        dif_hell.updateColor(overColor)
                    else:
                        dif_hell.updateColor(0)

                    if (posx >= 200 and posx <= 300) and (posy <= 190 and posy >= 160):
                        full_yes.updateColor(overColor)
                    else:
                        full_yes.updateColor(0)

                    if (posx >= 320 and posx <= 400) and (posy <= 190 and posy >= 160):
                        full_no.updateColor(overColor)
                    else:
                        full_no.updateColor(0)

                    if (posx >= 200 and posx <= 276) and (posy <= 250 and posy >= 215):
                        mus_prod.updateColor(overColor)
                    else:
                        mus_prod.updateColor(0)

                    if (posx >= 200 and posx <= 385) and (posy <= 285 and posy >= 255):
                        mus_under.updateColor(overColor)
                    else:
                        mus_under.updateColor(0)

                    if (posx >= 200 and posx <= 240) and (posy <= 335 and posy >= 305):
                        rank_yes.updateColor(overColor)
                    else:
                        rank_yes.updateColor(0)
                    
                # Se o usuario clicar em algum lugar, captura a posicao (x, y)
                elif event.type == MOUSEBUTTONDOWN:
                    posx, posy = event.pos
                    
                    if (posx >= 200 and posx <= 276) and (posy <= 137 and posy >= 108):
                        self.dificuldade = 'EASY'
                    
                    if (posx >= 300 and posx <= 375) and (posy <= 137 and posy >= 108):
                        self.dificuldade = 'NORMAL'
                                        
                    if (posx >= 400 and posx <= 495) and (posy <= 137 and posy >= 108):
                        self.dificuldade = 'FROM_HELL'

                    if (posx >= 200 and posx <= 300) and (posy <= 190 and posy >= 160):
                        self.fullscreen = True
                        self.initGUI()

                    if (posx >= 320 and posx <= 400) and (posy <= 190 and posy >= 160):
                        self.fullscreen = False
                        self.initGUI()

                    if (posx >= 200 and posx <= 276) and (posy <= 250 and posy >= 215):
                        self.sound.loadBackgroundSound(self.sound.tracks[0]['path'])
                        self.sound.turn = 1

                    if (posx >= 200 and posx <= 385) and (posy <= 285 and posy >= 255):
                        self.sound.loadBackgroundSound(self.sound.tracks[1]['path'])
                        self.sound.turn = 0

                    if (posx >= 200 and posx <= 240) and (posy <= 335 and posy >= 305):
                        io = ReversiIO('res/options.dat')
                        io.save({'fullscreen': self.fullscreen, 'dificuldade': self.dificuldade})
                        quit = True
                    
            
            sfc.fill(WHITE)
            pygame.draw.aaline(sfc, BLACK, (15, 60), (300, 60))
            pygame.draw.aaline(sfc, BLACK, (15, 145), (500, 145))
            pygame.draw.aaline(sfc, BLACK, (15, 200), (500, 200))
            pygame.draw.aaline(sfc, BLACK, (15, 295), (500, 295))
            
            draw.update(sfc, sprite_group)
            pygame.display.update()


    def abertura(self):
        ''' Abertura do Jogo  '''
        background = pygame.image.load("img/main").convert()
        draw = self.draw
        
        self.surface.blit(background, (0, 0))
        pressEnter = Text(265, 445, 20, GRAY, "Pressione ENTER para jogar")        
        
        selected = False
        blinked = True
        self.sound.changeMusic()
        
        while not selected:
            self.clock.tick(5) # Segura o jogo em 5 quadros por segundo

            if blinked:
                cor = GRAY
                blinked = False
            else:
                cor = WHITE
                blinked = True
            
            for event in pygame.event.get():    
                # Se o usuario clicar no botao de 'sair'
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self.shutdown()

                # Se o usuario clicar em algum lugar, captura a posicao (x, y)
                if event.type == KEYDOWN and event.key == K_RETURN:
                    selected = True
            
            self.surface.blit(background, (0, 0))
            pressEnter.update("Pressione ENTER para jogar", cor)            
            draw.update(self.surface, pygame.sprite.Group(pressEnter))            
        

    def help(self):
        # Instrucoes
        ajuda   = Text(15, 15, 30, mensagem = "Ajuda", cor = BLACK)
        pausa   = Text(25, 75, 14, mensagem = "P - Pausa / Retorna a musica", cor = CORBLU)
        troca   = Text(25, 100, 14, mensagem = "T - Troca a musica", cor = CORBLU)
        reinit  = Text(25, 125, 14, mensagem = "R - Reinicia o Jogo", cor = CORBLU)
        esc     = Text(25, 150, 14, mensagem = "ESC - Sai da rodada / Sai da ajuda", cor = CORBLU)

        images  = pygame.sprite.Group(ajuda, pausa, troca, reinit, esc)
        quit = False
        while not quit:
            self.clock.tick(5) # Segura o jogo em 10 quadros por segundo

            for event in pygame.event.get():    
                # Se o usuario clicar no botao de 'sair'
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    quit = True
                elif event.type == KEYDOWN:                                
                    # Para ou recomeca a Musica de fundo 
                    if event.key == ord('p'):
                        if musicPlaying:
                            self.sound.stop()
                            musicPlaying = False
                        else:
                            self.sound.changeMusic()
                            musicPlaying = True                                      
                            # Muda a musica de fundo sendo tocada        
                    elif event.key == ord('t'):
                        self.sound.changeMusic()

            self.surface.fill(WHITE)
            self.draw.update(self.surface, images)           

    def menu(self):
        ''' Metodo que cria o menu inicial '''

        # Atalhos para facilitar a vida de quem digita :P
        sfc  = self.surface
        draw = self.draw
        min  = draw.mini_text
         
        #-- Desenha o texto e os sprites --#
        self.surface.fill(WHITE)
        
        # Ranking
        ranking = Text(630, 13, 28, GRAY, "Ranking")
        
        # Nome do Jogo e os creditos no canto inferior direito    
        nome = Text(12, 13, 28, GRAY, "Reversi. The AI against Humanity") 
        cred = Text(560, 570, 14, GRAY, "Kod Games. Challenge is Everything") 

        # Musica do momento
        playList = Text(12, 570, 14, BLACK, "Now Playing: " + self.sound.getMusicName())

        # Opcoes
        play_cpu    = Text(320, 175, 20, GRAY, "Player vs CPU")
        play_play   = Text(320, 220, 20, GRAY, "Player vs Player")
        options     = Text(320, 280, 20, GRAY, "Opcoes")
        ajuda       = Text(320, 315, 20, GRAY, "Ajuda")
        escape      = Text(320, 375, 20, GRAY, "Sair do jogo")
        
        # Grupo de textos
        texts = pygame.sprite.Group(ranking, nome, cred, playList, play_cpu, play_play, options, ajuda, escape)     

        # Variaveis usadas para armazenar a posicao do mouse, que sera usada para saber exatamente
        # onde o usuario esta clicando
        posx, posy = 0, 0
        musicPlaying = True
        selected = False

        while not selected:
            self.clock.tick(16)
            for event in pygame.event.get():

                # Se o usuario clicar no botao de 'sair'
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self.shutdown()

                elif event.type == KEYDOWN:                                
                    # Para ou recomeca a Musica de fundo 
                    if event.key == ord('p'):
                        if musicPlaying:
                            self.sound.stop()
                            musicPlaying = False
                        else:
                            self.sound.changeMusic()
                            musicPlaying = True                                        
                        # Muda a musica de fundo sendo tocada        
                    elif event.key == ord('t'):
                        self.sound.changeMusic()
                        playList.update("Now Playing: " +self.sound.getMusicName(), BLACK)

                # Captura o movimento do mouse
                elif event.type == MOUSEMOTION:
                    posx, posy = event.pos

                    overColor = CORBLU

                    if (posx >= 320 and posx <= 510) and (posy <= 215 and posy >= 175):
                        play_cpu.update("Player vs CPU", overColor)
                    else:
                        play_cpu.update("Player vs CPU", GRAY)

                    if (posx >= 320 and posx <= 510) and (posy <= 260 and posy >= 220):
                        play_play.update("Player vs Player", overColor)
                    else:
                        play_play.update("Player vs Player", GRAY)                    

                    if (posx >= 320 and posx <= 510) and (posy <= 320 and posy >= 280):
                        options.update("Opcoes", overColor)
                    else:
                        options.update("Opcoes", GRAY)

                    if (posx >= 320 and posx <= 510) and (posy <= 355 and posy >= 315):
                        ajuda.update("Ajuda", overColor)
                    else:
                        ajuda.update("Ajuda", GRAY)

                    if (posx >= 320 and posx <= 510) and (posy <= 415 and posy >= 375):
                        escape.update("Sair do jogo", overColor)
                    else:
                        escape.update("Sair do jogo", GRAY)
                    
                # Se o usuario clicar em algum lugar, captura a posicao (x, y)
                elif event.type == MOUSEBUTTONDOWN:
                    posx, posy = event.pos

                    if (posx >= 320 and posx <= 510) and (posy <= 215 and posy >= 175):
                        self.p1 = Player("Jogador         ", draw.gray_orb)
                        self.p2 = Computer(draw.black_orb, self.dificuldade)
                        self.turn = self.p1
                        selected = True

                    elif (posx >= 320 and posx <= 510) and (posy <= 260 and posy >= 220):
                        self.p1 = Player("Jogador Preto   ", draw.black_orb)
                        self.p2 = Player("Jogador Cinza   ", draw.gray_orb)
                        self.turn = self.p2
                        selected = True

                    elif (posx >= 320 and posx <= 510) and (posy <= 320 and posy >= 280):
                        self.opcoes()

                    elif (posx >= 320 and posx <= 510) and (posy <= 355 and posy >= 315):
                        self.help()

                    elif (posx >= 320 and posx <= 510) and (posy <= 415 and posy >= 375):
                        self.shutdown()

            # Atualiza a tela
            sfc.fill(WHITE)
            
            #for i, player in enumerate(Ranking().toString()[:-1]):
            #    draw.draw(sfc, draw.text(min, player, GRAY), 632, 40 + ((i + 1) * 20))
           
            draw.update(sfc, texts)
            pygame.display.update()

    def switch(self):
        ''' Troca a vez do jogador '''        
        if self.turn == self.p1:
            self.turn = self.p2
        else:
            self.turn = self.p1

        # Atualiza os pontos e avisa o novo jogador
        self.updateScores(self.board.getPontos())
        self.alert(self.turn.nome, BLACK)


    def getCasa(self, x, y, t):
        ''' Pega a casa que foi clicada
            x => posicao x do Mouse
            y => posicao y do Mouse
            t => tamanho da casa        '''
        return ((x - (x % t)) / t, (y - (y % t)) / t)   


    def loop(self):
        ''' Inicia o jogo e seu loop principal '''
        
        # Inicia as estruturas de dados da interface
        self.menu()
        self.board = Board((8, 8), self.p1, self.p2)
        self.surface.fill(WHITE)

        # Inicia o relogio
        clock = self.clock
        cronometro = 15000
        
        # Variaveis-atalho pra melhorar a vida do programador
        draw = self.draw
        min = draw.mini_text
        player = self.p1
        player2 = self.p2
        board = self.board
        t = self.draw.tamanho_casa        
        change = self.sound.change
        stun = self.sound.stun
                
        # Inicia os Sprites
        cron = Cronometer(600, 350)
        self.cron_group = pygame.sprite.Group(cron)
        self.clock.tick() # Reinicia o contador de quadros
        
        self.p1_score = Text(500, 100,  30, BLACK, "")
        self.p2_score = Text(500, 150, 30, BLACK, "")
        self.alert_text = Text(100, 500, 48, BLACK, "")
        pontuacao = Text(502, 75, 14, GRAY, "Pontuacao")
        tempo = Text(504, 358, 14, GRAY, "Seu Tempo")
        
        self.text_group = pygame.sprite.Group(self.p1_score, self.p2_score, self.alert_text, pontuacao, tempo)

        self.tab = Tabuleiro(draw.espacamento, t, board.dim, 5, 5)
        self.tab_group = pygame.sprite.Group(self.tab)
        
        # Imprime os sprites e textos pela primeira vez na rodada
        self.tab.update(board, player, player2)
        self.alert(self.turn.nome, BLACK)    
        self.updateScores(self.board.getPontos())        
        
        musicPlaying = True
        Reset = False
        escape = False

##        try:
        while not Reset:
            clock.tick(10)
            
            for event in pygame.event.get():
                if event.type == QUIT:   self.shutdown()
                elif event.type == KEYDOWN and event.key == ord('r'): Reset = True

            # Loop principal do jogo
            while not self.endGame() and not escape:
                ### Jogada da CPU ###
                if self.turn.type == CPU:
                    x, y = self.turn.AI(board) # CPU calcula a melhor jogada
                    clock.tick(1)            # Cria um delay de 1s para a jogada da CPU pra nao ficar sem graca                     
                    self.turn.fazMovimento(board, x, y)
                    self.switch()

                ### Jogada do Jogador Humano ###
                if self.turn.type == HUMAN:
                    # Decrementa o cronometro
                    cronometro -= clock.tick(10)

                    if self.dificuldade == 'EASY':
                        melhorMovimento = board.melhorJogada(self.turn, board.getMovimentosValidos(self.turn) )
                        if melhorMovimento != False:
                            board.casas[melhorMovimento] = 'DICA'

                    # Conta o tempo... Se passar de 15 segundos a vez passa para a o proximo jogador
                    if cronometro <= 0:
                        cronometro = 15000
                        self.switch()                            
                                            
                    for event in pygame.event.get():
                        # Se o jogador clicar no X da janela, encerra o jogo
                        if event.type == QUIT:
                            self.shutdown()
                        
                        elif event.type == KEYDOWN:                                
                            # Para ou recomeca a Musica de fundo 
                            if event.key == ord('p'):
                                if musicPlaying:
                                    self.sound.stop()
                                    musicPlaying = False
                                else:
                                    self.sound.changeMusic()
                                    musicPlaying = True                                        
                            # Muda a musica de fundo sendo tocada        
                            elif event.key == ord('t'):
                                self.sound.changeMusic()
                                self.alert(self.sound.getMusicName(), GRAY)

                            # Se o jogador digitar ESC sai do jogo atual e reseta
                            elif event.key == K_ESCAPE:
                                escape = True
                                Reset = True

                        # Registra a jogada do jogador a partir do evento gerado pelo Mouse
                        elif event.type == MOUSEBUTTONDOWN:
                            posx, posy = event.pos
                            x, y = self.getCasa(posx, posy, t)

                            # So registra movimentos de cliques que foram dados dentro das
                            # dimensoes do tabuleiro
                            if (x >= 0 and x < board.dim[0]) and (y >= 0 and y < board.dim[1]):
                                if self.turn.fazMovimento(board, x, y) == False:
                                    # Se a jogada for errada da uma mensagem de erro e um som: 'STOMP!'
                                    self.alert("Jogada invalida", GRAY)
                                    stun.play()
                                else:
                                    # Se a jogada for um sucesso, toca o som da moedinha do Mario e troca o jogador
                                    change.play()
                                    self.switch()
                                    cronometro = 0

                # Atualiza os graficos
                cron.update(str(int(cronometro / 1000)))
                self.tab.update(self.board, self.p1, self.p2)
                self.surface.fill(WHITE)
                draw.update (self.surface, self.text_group, self.tab_group, self.cron_group)

            if not escape:
                # Repinta o fundo de branco
                self.surface.fill(WHITE)
                
                # Estando o jogo terminado, exibe uma mensagem com o nome do vencedor em vermelho, ou empate
                resultado = "Vencedor: " + self.getVencedor().nome if self.getVencedor() != None else "Empate!"
                self.alert(resultado, RED)                
                draw.update (self.surface, self.text_group, self.tab_group, self.cron_group)

        # Reset the Game
        #self.registerInRanking()
        self.loop()
            
##        except Exception, t:
##            print t
##            self.shutdown()

    def updateScores(self, scores):
        ''' Atualiza os dados de Scores '''
        n1 = self.p1.nome
        n2 = self.p2.nome
        self.p1_score.update(n1 + "  " + str(scores[n1]), BLACK)
        self.p2_score.update(n2 + "  " + str(scores[n2]), BLACK)

                  
    def alert(self, msg, cor):
        ''' Metodo que fornece uma interface pratica de aviso para o usuario '''
        self.alert_text.update(msg, cor)
        

    def registerInRanking(self):
        ''' Registra o Jogador Vencedor no Ranking '''
        rank = Ranking()
        if self.getVencedor() != None:
            vencedor = self.getVencedor()
            pontos = self.board.getPontos()[vencedor.nome]
            rank.register(vencedor.nome, pontos)
        
        
    def getVencedor(self):
        ''' Analisa os pontos para saber quem eh o vencedor '''
        player = self.p1
        cpu = self.p2
        
        pontos = self.board.getPontos()
        if pontos[player.nome] > pontos[cpu.nome]:     return player
        elif pontos[cpu.nome] > pontos[player.nome]:  return cpu
        elif pontos[cpu.nome] == pontos[player.nome]: return None


    def endGame(self):
        ''' Verifica o tabuleiro e finaliza o jogo '''
        casas = self.board.casas.values()

        # Se nao houverem mais casas vazias, ou se nao houverem mais pecas de um determinado jogador
        # ou se nao ha mais movimentos validos de um jogador, encerra a partida
        if (None not in casas) or (self.p1 not in casas) or (self.p2 not in casas) or \
           (self.board.getMovimentosValidos(self.turn) == []):
            return True
        else:
            return False
        

    def shutdown(self):
        ''' Desliga o pygame e fecha a janela '''
        pygame.quit()
        exit()
