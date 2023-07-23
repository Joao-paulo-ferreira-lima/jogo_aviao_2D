import pygame
import random
import sys


class Jogo:
    def __init__(self):
        pygame.init()

        # Defina as dimensões da tela
        self.largura_tela = 800
        self.altura_tela = 600

        # Defina as cores (formato RGB)
        self.branco = (255, 255, 255)
        self.preto = (0, 0, 0)

        # Defina a velocidade do avião e do fundo

        self.velocidade_aviao = 3
        self.velocidade_horizontal_aviao = 3
        self.velocidade_horizontal_fundo = 2
        self.velocidade_inimigo = 3
        self.velocidade_tiro = 5
        self.tiros = []
        # Crie a tela do jogo
        self.tela = pygame.display.set_mode((self.largura_tela, self.altura_tela))
        pygame.display.set_caption("Jogo de Avião 2D")

        # Lista de caminhos das imagens de obstáculos
        self.obstaculo_imagens = [
            r"C:\Users\WIN10\PycharmProjects\jogo_python\images/disco_voador_tras.png",
            r"C:\Users\WIN10\PycharmProjects\jogo_python\images\disco1_tras.png",
            r"C:\Users\WIN10\PycharmProjects\jogo_python\images\disco2_tras.png"
        ]

        # Defina o intervalo mínimo entre tiros em milissegundos (1000ms = 1 segundo)
        self.intervalo_tiro = 500  # Por exemplo, aqui o intervalo é de 0.5 segundos
        self.ultimo_disparo_tempo = 0

        # Carregue as imagens do avião e do obstáculo
        self.aviao_imagem = pygame.image.load(r"images\aviao_tras.png").convert_alpha()
        self.obstaculo_imagem = pygame.image.load(r"images\disco_voador_tras.png").convert_alpha()
        self.fundo_imagem = pygame.image.load(r"images\fundo.jpg").convert_alpha()
        #self.inimigo = pygame.image.load(r'C:\Users\WIN10\PycharmProjects\jogo_python\images\aviao_inimigo_tras.png').convert_alpha()

        # Carregue a imagem do tiro
        self.tiro_imagem = pygame.image.load(r"images\bala.jpg")
        # Crie uma lista para armazenar os tiros


        # Mascara para as imagens de fundo trasparente
        self.aviao_mask = pygame.mask.from_surface(self.aviao_imagem)
        self.obstaculo_mask = pygame.mask.from_surface(self.obstaculo_imagem)
        self.tiro_mask = pygame.mask.from_surface(self.tiro_imagem)
        #self.inimigo_mask = pygame.mask.from_surface(self.inimigo)

    def tela_inicial(self):
        fundo_x = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if botao.collidepoint(event.pos):
                        return

            # Preencha a tela com a cor branca
            self.tela.blit(self.fundo_imagem, (fundo_x, 0))
            self.tela.blit(self.fundo_imagem, (fundo_x + self.largura_tela, 0))

            # Desenhe o botão
            fonte = pygame.font.Font(None, 46)
            botao = pygame.draw.rect(self.tela, self.preto, (300, 250, 200, 100))
            texto_botao = fonte.render("JOGAR ", True, self.branco)
            self.tela.blit(texto_botao, (340, 280))

            # Atualize a tela
            pygame.display.update()

    def disparar_tiro(self, aviao_x, aviao_y):

        # Verifique se já passou o intervalo mínimo desde o último disparo
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.ultimo_disparo_tempo > self.intervalo_tiro:
            tiro_x = aviao_x + self.aviao_imagem.get_width()  # Posição inicial do tiro
            tiro_y = aviao_y + self.aviao_imagem.get_height() // 2 - self.tiro_imagem.get_height() // 2
            self.tiros.append((tiro_x, tiro_y))  # Adiciona o tiro à lista de tiros
            self.ultimo_disparo_tempo = tempo_atual  # Atualiza o tempo do último disparo

    def exibir_pontuacao(self, pontuacao, abatidos, vidas):
        fonte = pygame.font.Font(None, 36)
        texto = fonte.render("Passaram: " + str(pontuacao), True, self.preto)
        texto1 = fonte.render("Abatidos: " + str(abatidos), True, self.preto)
        vidas = fonte.render('Vidas: ' + str(vidas), True, self.preto)
        self.tela.blit(vidas, (656, 10))
        self.tela.blit(texto, (10, 10))
        self.tela.blit(texto1, (180, 10))

    def gerar_inimigo(self):
        global obstaculo_imagem  # Declare a variável como global
        obstaculo_x = self.largura_tela
        obstaculo_y = random.randint(0, self.altura_tela - self.obstaculo_imagem.get_height())
        obstaculo_imagem_path = random.choice(self.obstaculo_imagens)
        # Escolhe aleatoriamente um caminho de imagem de inimigo
        obstaculo_imagem = pygame.image.load(obstaculo_imagem_path).convert_alpha()
        return obstaculo_x, obstaculo_y, obstaculo_imagem

    def jogo(self, aviao_x, aviao_y, obstaculo_x, obstaculo_y):
        global obstaculo_imagem
        # Posição inicial do fundo
        fundo_x = 0
        # Variavel do loop
        lop = True
        # Variável para armazenar a pontuação
        pontuacao = 0
        abatidos = 0
        vidas = 10
        while lop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    lop = False
                if vidas <= 0:
                    self.tela_inicial()
                    vidas = 10
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    print("x = {}, y = {}".format(pos[0], pos[1]))
            # Obtenha as teclas pressionadas
            teclas = pygame.key.get_pressed()

            # Mova o avião para cima ou para baixo com base nas teclas pressionadas
            if teclas[pygame.K_UP] and aviao_y > 0:
                aviao_y -= self.velocidade_aviao
            if teclas[pygame.K_DOWN] and aviao_y < self.altura_tela - self.aviao_imagem.get_height():
                aviao_y += self.velocidade_aviao

            # Mova o avião para a esquerda ou para a direita com base nas teclas pressionadas
            if teclas[pygame.K_LEFT] and aviao_x > 0:
                aviao_x -= self.velocidade_horizontal_aviao
            if teclas[pygame.K_RIGHT] and aviao_x < self.largura_tela - self.aviao_imagem.get_width():
                aviao_x += self.velocidade_horizontal_aviao

            # Mova o fundo para a esquerda
            fundo_x -= self.velocidade_horizontal_fundo

            # Se o fundo sair completamente da tela, reinicie a posição do fundo
            if fundo_x <= -self.largura_tela:
                fundo_x = 0

            # Mova o inimigo para a esquerda
            obstaculo_x -= self.velocidade_inimigo

            # Verifique se o jogador pressionou a tecla de disparo (barra de espaço)
            if teclas[pygame.K_SPACE]:
                self.disparar_tiro(aviao_x, aviao_y)

            # Atualize a posição dos tiros apenas na direção horizontal
            for i in range(len(self.tiros)):
                tiro_x, tiro_y = self.tiros[i]
                tiro_x += self.velocidade_tiro
                self.tiros[i] = (tiro_x, tiro_y)
                if tiro_x > self.largura_tela:  # Se o tiro sair da tela, remova-o da lista de tiros
                    self.tiros.pop(i)
                    break

            # Se o inimigo sair completamente da tela, gere um novo inimigo
            if obstaculo_x < -obstaculo_imagem.get_width():
                pontuacao += 1
                obstaculo_x, obstaculo_y, obstaculo_imagem = self.gerar_inimigo()

            # Verifique colisão entre avião e obstáculo
            aviao_rect = pygame.Rect(aviao_x, aviao_y, self.aviao_imagem.get_width(), self.aviao_imagem.get_height())
            colisao_aviao = self.aviao_mask.overlap(self.obstaculo_mask, (aviao_rect.x - obstaculo_x, aviao_rect.y - obstaculo_y))
            if colisao_aviao:
                # Colisão detectada, reinicie o jogo
                aviao_x = self.largura_tela // 20
                aviao_y = self.altura_tela // 2
                obstaculo_x, obstaculo_y, obstaculo_imagem = self.gerar_inimigo()
                vidas -= 1

            # Verifique colisões entre tiros e obstáculos
            for tiro in self.tiros:
                tiro_x, tiro_y = tiro
                if obstaculo_x < tiro_x < obstaculo_x + obstaculo_imagem.get_width() and \
                        obstaculo_y < tiro_y < obstaculo_y + obstaculo_imagem.get_height():
                    # Acertou o obstáculo, remova o obstáculo e o tiro da tela e da lista de tiros
                    self.tiros.remove(tiro)
                    obstaculo_x, obstaculo_y, obstaculo_imagem = self.gerar_inimigo()
                    abatidos += 1
                    break
            # Limpe a tela
            self.tela.fill(self.branco)

            # Desenhe o fundo em duas posições para criar o efeito de movimento contínuo
            self.tela.blit(self.fundo_imagem, (fundo_x, 0))
            self.tela.blit(self.fundo_imagem, (fundo_x + self.largura_tela, 0))

            # Desenhe o avião, inimigo e obstáculo na tela
            self.tela.blit(self.aviao_imagem, (aviao_x, aviao_y))
            self.tela.blit(obstaculo_imagem, (obstaculo_x, obstaculo_y))

            # Desenhe os tiros na tela
            for tiro in self.tiros:
                tiro_x, tiro_y = tiro
                self.tela.blit(self.tiro_imagem, (tiro_x, tiro_y))

            # Exiba a pontuação na tela
            self.exibir_pontuacao(pontuacao, abatidos, vidas)

            # Atualize a tela

            pygame.display.update()
        pygame.quit()
