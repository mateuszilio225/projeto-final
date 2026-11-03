# DEEP SEA EVADE - Escape Submarino
# Versao simples baseada apenas nos comandos do codigo da atividade.
# Nao precisa de imagens, sons ou da pasta recursos.

import pygame
import random

pygame.init()

nome = input("Informe o nome do competidor: ")
if len(nome) == 0:
    nome = "Jogador"

tamanho = (800, 450)
pygame.display.set_caption("Deep Sea Evade - Escape Submarino")

# FULLSCREEN e SCALED sao apenas opcoes do set_mode que ja existe no exemplo.
tela = pygame.display.set_mode(tamanho, pygame.FULLSCREEN | pygame.SCALED)
relogio = pygame.time.Clock()
fonteMenu = pygame.font.SysFont("comicsans", 23)
fonteTitulo = pygame.font.SysFont("comicsans", 43)

branco = (255, 255, 255)
preto = (0, 0, 0)
azul = (8, 58, 98)
azulClaro = (20, 110, 155)
azulEscuro = (4, 37, 72)
areia = (23, 91, 95)
ruina = (68, 114, 119)
coral = (255, 105, 105)
amarelo = (246, 196, 61)
cinza = (139, 168, 179)
vermelho = (230, 80, 79)
roxo = (186, 119, 211)


def jogar():
    posicaoXPersona = 80
    posicaoYPersona = 200
    movimentoXPersona = 0
    movimentoYPersona = 0
    velocidadeMovPersona = 5

    posicaoXMissel = 850
    posicaoYMissel = 200
    velocidadeMissel = 4
    tipoObstaculo = random.randint(1, 3)
    pontos = 0
    fundoMov1 = 0
    fundoMov2 = 800

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_UP:
                movimentoYPersona = -velocidadeMovPersona
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_DOWN:
                movimentoYPersona = velocidadeMovPersona
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimentoXPersona = -velocidadeMovPersona
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimentoXPersona = velocidadeMovPersona
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_UP:
                movimentoYPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_DOWN:
                movimentoYPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 0

        posicaoXPersona = posicaoXPersona + movimentoXPersona
        posicaoYPersona = posicaoYPersona + movimentoYPersona

        if posicaoXPersona < 20:
            posicaoXPersona = 20
        elif posicaoXPersona > 685:
            posicaoXPersona = 685
        if posicaoYPersona < 65:
            posicaoYPersona = 65
        elif posicaoYPersona > 370:
            posicaoYPersona = 370

        posicaoXMissel = posicaoXMissel - velocidadeMissel
        if posicaoXMissel < -125:
            posicaoXMissel = 800
            posicaoYMissel = random.randint(95, 330)
            tipoObstaculo = random.randint(1, 3)
            pontos = pontos + 25
            if velocidadeMissel < 11:
                velocidadeMissel = velocidadeMissel + 1

        fundoMov1 = fundoMov1 - 1
        fundoMov2 = fundoMov2 - 1
        if fundoMov1 <= -800:
            fundoMov1 = 800
        if fundoMov2 <= -800:
            fundoMov2 = 800

        # Oceano desenhado com os mesmos retangulos usados nos botoes originais.
        tela.fill(azulEscuro)
        pygame.draw.rect(tela, azulClaro, (0, 0, 800, 95))
        pygame.draw.rect(tela, azul, (0, 95, 800, 265))
        pygame.draw.rect(tela, areia, (0, 395, 800, 55))

        # Fundo em movimento: ruinas e corais repetidos.
        pygame.draw.rect(tela, ruina, (fundoMov1 + 100, 260, 32, 135))
        pygame.draw.rect(tela, ruina, (fundoMov1 + 190, 260, 32, 135))
        pygame.draw.rect(tela, ruina, (fundoMov1 + 87, 252, 148, 18))
        pygame.draw.rect(tela, coral, (fundoMov1 + 480, 355, 14, 50))
        pygame.draw.rect(tela, coral, (fundoMov1 + 465, 367, 18, 12))
        pygame.draw.rect(tela, coral, (fundoMov1 + 493, 374, 16, 12))

        pygame.draw.rect(tela, ruina, (fundoMov2 + 100, 260, 32, 135))
        pygame.draw.rect(tela, ruina, (fundoMov2 + 190, 260, 32, 135))
        pygame.draw.rect(tela, ruina, (fundoMov2 + 87, 252, 148, 18))
        pygame.draw.rect(tela, coral, (fundoMov2 + 480, 355, 14, 50))
        pygame.draw.rect(tela, coral, (fundoMov2 + 465, 367, 18, 12))
        pygame.draw.rect(tela, coral, (fundoMov2 + 493, 374, 16, 12))

        # Submarino amarelo: corpo, vidro, cauda e periscopio.
        pygame.draw.rect(tela, amarelo, (posicaoXPersona, posicaoYPersona, 100, 41), border_radius=18)
        pygame.draw.rect(tela, azulClaro, (posicaoXPersona + 59, posicaoYPersona + 9, 25, 23), border_radius=10)
        pygame.draw.rect(tela, amarelo, (posicaoXPersona - 12, posicaoYPersona + 12, 18, 17))
        pygame.draw.rect(tela, amarelo, (posicaoXPersona + 28, posicaoYPersona - 10, 10, 15))
        pygame.draw.rect(tela, amarelo, (posicaoXPersona + 28, posicaoYPersona - 10, 23, 7))

        # Sorteia tubarao, torpedo ou agua-viva a cada obstaculo.
        if tipoObstaculo == 1:
            pygame.draw.rect(tela, cinza, (posicaoXMissel, posicaoYMissel, 100, 39), border_radius=16)
            pygame.draw.rect(tela, cinza, (posicaoXMissel + 50, posicaoYMissel - 14, 18, 17))
            pygame.draw.rect(tela, cinza, (posicaoXMissel + 95, posicaoYMissel + 10, 22, 23))
            pygame.draw.rect(tela, preto, (posicaoXMissel + 12, posicaoYMissel + 10, 6, 6))
        elif tipoObstaculo == 2:
            pygame.draw.rect(tela, cinza, (posicaoXMissel, posicaoYMissel + 8, 100, 26), border_radius=12)
            pygame.draw.rect(tela, vermelho, (posicaoXMissel, posicaoYMissel + 13, 14, 16))
            pygame.draw.rect(tela, vermelho, (posicaoXMissel + 78, posicaoYMissel, 15, 42))
        else:
            pygame.draw.rect(tela, roxo, (posicaoXMissel + 20, posicaoYMissel, 65, 32), border_radius=16)
            pygame.draw.rect(tela, roxo, (posicaoXMissel + 30, posicaoYMissel + 30, 8, 30))
            pygame.draw.rect(tela, roxo, (posicaoXMissel + 50, posicaoYMissel + 30, 8, 30))
            pygame.draw.rect(tela, roxo, (posicaoXMissel + 70, posicaoYMissel + 30, 8, 30))

        texto = fonteMenu.render("Profundidade: " + str(pontos) + " m", True, branco)
        tela.blit(texto, (565, 17))
        textoNome = fonteMenu.render(nome, True, branco)
        tela.blit(textoNome, (20, 17))

        # Colisao, usando apenas comparacoes como no codigo original.
        if posicaoXPersona + 95 > posicaoXMissel + 15 and posicaoXPersona < posicaoXMissel + 95:
            if posicaoYPersona + 36 > posicaoYMissel and posicaoYPersona < posicaoYMissel + 55:
                dead(pontos)

        pygame.display.update()
        relogio.tick(60)


def dead(pontos):
    startButton = pygame.draw.rect(tela, amarelo, (225, 260, 150, 50), border_radius=15)
    quitButton = pygame.draw.rect(tela, branco, (425, 260, 150, 50), border_radius=15)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                quit()
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    jogar()
                elif quitButton.collidepoint(evento.pos):
                    quit()

        tela.fill(azulEscuro)
        texto = fonteTitulo.render("FIM DE JOGO!", True, branco)
        tela.blit(texto, (270, 90))
        texto = fonteMenu.render("Voce explorou " + str(pontos) + " metros", True, branco)
        tela.blit(texto, (275, 155))

        startButton = pygame.draw.rect(tela, amarelo, (225, 260, 150, 50), border_radius=15)
        texto = fonteMenu.render("Jogar de novo", True, preto)
        tela.blit(texto, (231, 269))
        quitButton = pygame.draw.rect(tela, branco, (425, 260, 150, 50), border_radius=15)
        texto = fonteMenu.render("Sair", True, preto)
        tela.blit(texto, (476, 269))

        pygame.display.update()
        relogio.tick(60)


def start():
    startButton = pygame.draw.rect(tela, amarelo, (225, 320, 150, 50), border_radius=15)
    quitButton = pygame.draw.rect(tela, branco, (425, 320, 150, 50), border_radius=15)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                quit()
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    jogar()
                elif quitButton.collidepoint(evento.pos):
                    quit()

        tela.fill(azulEscuro)
        pygame.draw.rect(tela, azul, (0, 250, 800, 200))
        pygame.draw.rect(tela, amarelo, (335, 195, 130, 46), border_radius=20)
        pygame.draw.rect(tela, azulClaro, (413, 207, 26, 22), border_radius=10)
        pygame.draw.rect(tela, amarelo, (325, 210, 20, 17))

        texto = fonteTitulo.render("DEEP SEA EVADE", True, branco)
        tela.blit(texto, (195, 80))
        texto = fonteMenu.render("Escape dos tubaroes, torpedos e aguas-vivas!", True, branco)
        tela.blit(texto, (158, 143))

        startButton = pygame.draw.rect(tela, amarelo, (225, 320, 150, 50), border_radius=15)
        texto = fonteMenu.render("Jogar", True, preto)
        tela.blit(texto, (272, 329))
        quitButton = pygame.draw.rect(tela, branco, (425, 320, 150, 50), border_radius=15)
        texto = fonteMenu.render("Sair", True, preto)
        tela.blit(texto, (476, 329))
        pygame.display.update()
        relogio.tick(60)


start()
