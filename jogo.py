# ABYSS COCKPIT: DEPTH ZERO
# Base: logica simples de Deep Sea Evade. Graficos procedurais.
import pygame
import random
import sys
import pyttsx3
from datetime import datetime
from Recursos.trabalho import desenhar_indicador


def escrever(texto, x, y, cor, fonte):
    imagem = fonte.render(texto, True, cor)
    tela.blit(imagem, (x, y))


def ler_recorde():
    recordista = 'Sem partidas'
    recorde = -1
    data_recorde = '--/--/----'
    hora_recorde = '--:--:--'
    # Quatro linhas por partida: nome, pontos, data e hora.
    try:
        with open('log.dat', 'r', encoding='utf-8') as arquivo:
            nome_lido = arquivo.readline()
            while nome_lido != '':
                pontos_lidos = arquivo.readline()
                data_lida = arquivo.readline()
                hora_lida = arquivo.readline()
                if pontos_lidos == '' or data_lida == '' or hora_lida == '':
                    break
                try:
                    pontos_lidos = int(pontos_lidos)
                    if pontos_lidos > recorde:
                        recordista = nome_lido.strip()
                        recorde = pontos_lidos
                        data_recorde = data_lida.strip()
                        hora_recorde = hora_lida.strip()
                except ValueError:
                    pass
                nome_lido = arquivo.readline()
    except FileNotFoundError:
        pass
    if recorde < 0:
        recorde = 0
    return recordista, recorde, data_recorde, hora_recorde


def salvar_partida(nome, pontos):
    agora = datetime.now()
    with open('log.dat', 'a', encoding='utf-8') as arquivo:
        arquivo.write(nome + '\n')
        arquivo.write(str(pontos) + '\n')
        arquivo.write(agora.strftime('%d/%m/%Y') + '\n')
        arquivo.write(agora.strftime('%H:%M:%S') + '\n')


nome = input('Informe o nome do competidor: ')
if len(nome) == 0:
    nome = 'Jogador'

pygame.init()
pygame.display.set_caption('ABYSS COCKPIT: DEPTH ZERO')
# Janela normal para manter o X de fechar pedido pelo professor.
tela = pygame.display.set_mode((1000, 700))
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont('consolas', 19)
pequena = pygame.font.SysFont('consolas', 15)
titulo = pygame.font.SysFont('consolas', 43)
media = pygame.font.SysFont('consolas', 27)

branco = (214, 239, 239)
ciano = (64, 219, 226)
verde = (72, 230, 136)
amarelo = (246, 196, 61)
vermelho = (242, 79, 85)
roxo = (175, 98, 211)
metal = (36, 55, 67)
preto = (4, 10, 18)

# A fala ocorre uma vez ao iniciar cada missao, nunca a cada frame.
voz = None
aviso_voz = ''
try:
    voz = pyttsx3.init()
    voz.setProperty('rate', 165)
except (RuntimeError, OSError, ImportError):
    aviso_voz = 'Voz indisponivel: verifique o sintetizador do sistema.'
    print(aviso_voz)

recordista, recorde, data_recorde, hora_recorde = ler_recorde()
estado = 'inicio'
resultado = ''
aviso_log = ''

while True:
    if estado == 'preparar':
        profundidade = 10000
        integridade = 100
        agua = 0
        bateria = 100
        pontos = 0
        quadros = 0
        posicao = 0
        esquerda = False
        direita = False
        pausado = False
        farol = False
        manchas = False
        limpador = 0
        efeito_limpador = 0
        efeito_bomba = 0
        impacto = 0
        distancia = 400
        ameaca_x = random.randint(-280, 280)
        tipo = random.randint(1, 3)
        direcao = 1
        bolha_x = random.randint(65, 925)
        bolha_y = random.randint(80, 405)
        raio = 10
        pulso = 1
        aviso_log = ''
        estado = 'jogo'
        if voz != None:
            try:
                voz.say('Sistemas ativados. Iniciando subida.')
                voz.runAndWait()
            except (RuntimeError, OSError):
                aviso_voz = 'Nao foi possivel reproduzir a voz.'
                print(aviso_voz)

    # Os botoes sao retangulos como na base do professor.
    # Sao redesenhados depois de processar os eventos.
    botao_inicio = pygame.draw.rect(tela, ciano, (310, 555, 380, 60))
    botao_reinicio = pygame.draw.rect(tela, ciano, (310, 555, 380, 60))
    botao_farol = pygame.draw.rect(tela, metal, (315, 505, 125, 58))
    botao_limpador = pygame.draw.rect(tela, metal, (450, 505, 125, 58))
    botao_bomba = pygame.draw.rect(tela, metal, (585, 505, 125, 58))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif estado == 'jogo':
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausado = not pausado
                    esquerda = False
                    direita = False
                elif not pausado:
                    if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                        esquerda = True
                    elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                        direita = True
            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    esquerda = False
                elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    direita = False
            elif evento.type == pygame.MOUSEBUTTONUP and not pausado:
                if botao_farol.collidepoint(evento.pos):
                    if bateria > 0:
                        farol = not farol
                elif botao_limpador.collidepoint(evento.pos) and limpador == 0:
                    manchas = False
                    limpador = 180
                    efeito_limpador = 30
                elif botao_bomba.collidepoint(evento.pos) and bateria >= 8:
                    agua = agua - 18
                    if agua < 0:
                        agua = 0
                    bateria = bateria - 8
                    efeito_bomba = 40
        elif evento.type == pygame.MOUSEBUTTONUP:
            if estado == 'inicio' and botao_inicio.collidepoint(evento.pos):
                estado = 'preparar'
            elif estado == 'fim' and botao_reinicio.collidepoint(evento.pos):
                estado = 'preparar'

    tela.fill(preto)

    if estado == 'inicio':
        pygame.draw.rect(tela, metal, (30, 30, 940, 640), 4)
        pygame.draw.rect(tela, (9, 35, 53), (55, 55, 890, 150))
        escrever('ABYSS COCKPIT', 90, 70, ciano, titulo)
        escrever('D E P T H   Z E R O', 95, 133, amarelo, media)
        escrever('Bem-vindo, ' + nome, 90, 235, branco, media)
        escrever('Seu batiscafo esta danificado a 10.000 metros.', 90, 290, branco, fonte)
        escrever('Sobreviva por cerca de 3 minutos e alcance a superficie.', 90, 320, branco, fonte)
        escrever('A/D ou setas: desviar somente na horizontal.', 90, 365, ciano, fonte)
        escrever('Mouse: FAROL, LIMPADOR e BOMBA. Espaco: pausa.', 90, 395, ciano, fonte)
        escrever('ESC ou X da janela: fechar.', 90, 425, ciano, fonte)
        escrever('Recordista: ' + recordista + ' | ' + str(recorde) + ' pontos', 90, 475, verde, fonte)
        escrever(data_recorde + '  ' + hora_recorde, 90, 505, branco, fonte)
        pygame.draw.rect(tela, ciano, (310, 555, 380, 60), border_radius=10)
        escrever('INICIAR MISSAO', 393, 574, preto, media)
        escrever(aviso_voz, 65, 637, amarelo, pequena)

    elif estado == 'jogo':
        if not pausado:
            quadros = quadros + 1
            if esquerda:
                posicao = posicao - 5
            if direita:
                posicao = posicao + 5
            if posicao < -300:
                posicao = -300
            elif posicao > 300:
                posicao = 300

            # 10.800 quadros / 60 FPS = aproximadamente 3 minutos ativos.
            profundidade = 10000 - quadros * 10000 / 10800
            if profundidade < 0:
                profundidade = 0
            if quadros % 60 == 0:
                pontos = pontos + 5
            if farol:
                bateria = bateria - 0.025
                if bateria <= 0:
                    bateria = 0
                    farol = False
            elif bateria < 100:
                bateria = bateria + 0.012
                if bateria > 100:
                    bateria = 100

            if limpador > 0:
                limpador = limpador - 1
            if efeito_limpador > 0:
                efeito_limpador = efeito_limpador - 1
            if efeito_bomba > 0:
                efeito_bomba = efeito_bomba - 1
            if impacto > 0:
                impacto = impacto - 1
            if agua > 0:
                agua = agua + 0.007

            distancia = distancia - 1.6
            if tipo == 1:
                distancia = distancia - 0.6
            elif tipo == 3:
                ameaca_x = ameaca_x + direcao * 1.5
                if ameaca_x > 280:
                    direcao = -1
                elif ameaca_x < -280:
                    direcao = 1
            if distancia <= 0:
                diferenca = ameaca_x - posicao
                if diferenca > -100 and diferenca < 100:
                    impacto = 35
                    if tipo == 2:
                        manchas = True
                        integridade = integridade - 10
                        agua = agua + 8
                    else:
                        integridade = integridade - 20
                        agua = agua + 18
                else:
                    pontos = pontos + 50
                distancia = 400
                ameaca_x = random.randint(-280, 280)
                tipo = random.randint(1, 3)
                direcao = 1
            if integridade < 0:
                integridade = 0
            if agua > 100:
                agua = 100

            bolha_y = bolha_y - 1
            if quadros % 12 == 0:
                bolha_x = bolha_x + random.randint(-8, 8)
            if bolha_y < 65 or bolha_x < 60 or bolha_x > 935:
                bolha_y = 410
                bolha_x = random.randint(65, 925)
            if quadros % 4 == 0:
                raio = raio + pulso
                if raio >= 18:
                    pulso = -1
                elif raio <= 9:
                    pulso = 1

        # Escotilha e oceano: somente retangulos, sem imagens ou 3D real.
        tom = int((10000 - profundidade) / 400)
        pygame.draw.rect(tela, (7, 26 + tom, 48 + tom), (35, 40, 930, 400))
        pygame.draw.rect(tela, (9, 35 + tom, 58 + tom), (95, 90, 810, 280))
        pygame.draw.rect(tela, (12, 45 + tom, 70 + tom), (195, 145, 610, 160))
        if farol:
            pygame.draw.rect(tela, (20, 74 + tom, 96 + tom), (220, 115, 560, 240))
            pygame.draw.rect(tela, (29, 91 + tom, 113 + tom), (340, 155, 320, 160))
        pygame.draw.rect(tela, (77, 150, 164), (bolha_x, bolha_y, 7, 11))
        pygame.draw.rect(tela, (50, 103, 127), (bolha_x + 22, bolha_y + 17, 4, 6))
        escrever('SONAR ATIVO / CONTATO ANTECIPADO', 62, 62, ciano, pequena)

        # Primeiro aparece no radar; a escotilha revela depois (distancia < 310).
        if distancia < 310:
            tamanho = int(20 + (310 - distancia) * 0.6)
            centro_x = int(500 + (ameaca_x - posicao) * (0.3 + tamanho / 220))
            x = centro_x - tamanho // 2
            if x < 52:
                x = 52
            elif x > 930 - tamanho:
                x = 930 - tamanho
            y = 240 - tamanho // 3
            if tipo == 1:
                pygame.draw.rect(tela, (145, 164, 175), (x, y, tamanho, tamanho // 3))
                pygame.draw.rect(tela, vermelho, (x, y, tamanho // 5, tamanho // 3))
                pygame.draw.rect(tela, vermelho, (x + tamanho * 3 // 4, y - tamanho // 8, tamanho // 9, tamanho // 2))
            elif tipo == 2:
                pygame.draw.rect(tela, roxo, (x + tamanho // 4, y, tamanho // 2, tamanho // 2), border_radius=12)
                pygame.draw.rect(tela, roxo, (x + tamanho // 4, y + tamanho // 3, tamanho // 10, tamanho // 2))
                pygame.draw.rect(tela, roxo, (x + tamanho // 2, y + tamanho // 3, tamanho // 10, tamanho // 2))
                pygame.draw.rect(tela, roxo, (x + tamanho * 7 // 10, y + tamanho // 3, tamanho // 10, tamanho // 2))
                pygame.draw.rect(tela, amarelo, (x + tamanho // 3, y + tamanho // 6, 5, 5))
            else:
                pygame.draw.rect(tela, (116, 151, 165), (x, y, tamanho, tamanho // 3), border_radius=12)
                pygame.draw.rect(tela, (116, 151, 165), (x + tamanho // 2, y - tamanho // 5, tamanho // 7, tamanho // 3))
                pygame.draw.rect(tela, (116, 151, 165), (x + tamanho - 5, y - 5, tamanho // 6, tamanho // 2))
                pygame.draw.rect(tela, vermelho, (x + tamanho // 7, y + tamanho // 10, 5, 5))

        if manchas:
            pygame.draw.rect(tela, preto, (220, 130, 210, 170), border_radius=30)
            pygame.draw.rect(tela, preto, (520, 170, 260, 145), border_radius=35)
            pygame.draw.rect(tela, preto, (390, 240, 170, 100), border_radius=20)
        if integridade < 80:
            pygame.draw.rect(tela, ciano, (155, 95, 3, 115))
            pygame.draw.rect(tela, ciano, (155, 208, 55, 3))
            pygame.draw.rect(tela, ciano, (207, 210, 3, 65))
        if integridade < 40:
            pygame.draw.rect(tela, ciano, (802, 115, 3, 145))
            pygame.draw.rect(tela, ciano, (755, 257, 50, 3))
        if efeito_limpador > 0:
            pygame.draw.rect(tela, branco, (50 + efeito_limpador * 29, 70, 8, 340))
        pygame.draw.rect(tela, metal, (30, 35, 940, 410), 18)
        pygame.draw.rect(tela, ciano, (39, 44, 922, 392), 2)
        if impacto > 0:
            pygame.draw.rect(tela, vermelho, (40, 45, 920, 390), 7)
        pygame.draw.circle(tela, amarelo, (935, 22), raio)
        escrever('ABYSS / DEPTH ZERO', 50, 7, ciano, fonte)

        # Painel inferior e radar de varredura retangular.
        pygame.draw.rect(tela, metal, (20, 455, 960, 230))
        pygame.draw.rect(tela, (3, 23, 19), (40, 490, 245, 165))
        escrever('SONAR', 45, 463, verde, fonte)
        for grade in range(1, 5):
            pygame.draw.rect(tela, (15, 65, 45), (40 + grade * 49, 490, 1, 165))
            pygame.draw.rect(tela, (15, 65, 45), (40, 490 + grade * 33, 245, 1))
        pygame.draw.rect(tela, verde, (40 + quadros % 245, 490, 2, 165))
        radar_x = int(160 + (ameaca_x - posicao) / 6)
        radar_y = int(640 - distancia / 3)
        if distancia > 110 or quadros % 30 < 15:
            pygame.draw.rect(tela, vermelho, (radar_x, radar_y, 8, 8))
        pygame.draw.rect(tela, ciano, (157, 638, 10, 10))

        escrever('SISTEMAS DE EMERGENCIA', 315, 470, branco, fonte)
        pygame.draw.rect(tela, ciano if farol else (75, 94, 104), (315, 505, 125, 58), border_radius=8)
        pygame.draw.rect(tela, (75, 94, 104) if limpador > 0 else ciano, (450, 505, 125, 58), border_radius=8)
        pygame.draw.rect(tela, ciano if bateria >= 8 else (75, 94, 104), (585, 505, 125, 58), border_radius=8)
        escrever('FAROL', 345, 525, preto, fonte)
        escrever('LIMPADOR', 465, 525, preto, fonte)
        escrever('BOMBA', 615, 525, preto, fonte)
        escrever('ON' if farol else 'OFF', 355, 575, amarelo, pequena)
        escrever('AGUARDE' if limpador > 0 else 'PRONTO', 474, 575, amarelo, pequena)
        escrever('ATIVA' if efeito_bomba > 0 else '-18% AGUA', 595, 575, amarelo, pequena)
        escrever('DESVIO: ' + str(posicao), 315, 609, ciano, fonte)
        escrever('PONTOS: ' + str(pontos), 520, 609, verde, fonte)
        escrever('Press Space to Pause Game.', 315, 650, branco, pequena)
        escrever('PROFUNDIDADE ' + str(int(profundidade)) + ' m', 735, 465, ciano, fonte)
        desenhar_indicador(tela, pequena, 'CASCO', integridade, 735, 500, verde if integridade > 30 else vermelho)
        desenhar_indicador(tela, pequena, 'AGUA', agua, 735, 552, ciano if agua < 75 else vermelho)
        desenhar_indicador(tela, pequena, 'BATERIA', bateria, 735, 604, amarelo)

        if pausado:
            pygame.draw.rect(tela, preto, (350, 180, 300, 110))
            pygame.draw.rect(tela, amarelo, (350, 180, 300, 110), 3)
            escrever('PAUSE', 435, 195, amarelo, titulo)
            escrever('Espaco para continuar', 379, 253, branco, fonte)
        elif integridade <= 0 or agua >= 100 or profundidade <= 0:
            if integridade <= 0 or agua >= 100:
                resultado = 'MISSAO FRACASSADA'
            else:
                resultado = 'MISSAO CONCLUIDA'
                pontos = pontos + 1000
            # Executado uma unica vez por partida encerrada.
            try:
                salvar_partida(nome, pontos)
                recordista, recorde, data_recorde, hora_recorde = ler_recorde()
            except OSError:
                aviso_log = 'Falha ao salvar log.dat. Verifique a permissao da pasta.'
                print(aviso_log)
            esquerda = False
            direita = False
            estado = 'fim'

    elif estado == 'fim':
        pygame.draw.rect(tela, metal, (40, 40, 920, 620), 4)
        escrever(resultado, 120, 110, verde if resultado == 'MISSAO CONCLUIDA' else vermelho, titulo)
        escrever(nome, 120, 200, branco, media)
        if resultado == 'MISSAO CONCLUIDA':
            escrever('Superficie alcancada!', 120, 250, ciano, media)
        else:
            escrever('Profundidade final: ' + str(int(profundidade)) + ' m', 120, 250, ciano, media)
        escrever('Subida realizada: ' + str(int(10000 - profundidade)) + ' m', 120, 295, branco, fonte)
        escrever('Pontuacao final: ' + str(pontos), 120, 340, amarelo, media)
        escrever('Recordista: ' + recordista, 120, 410, verde, fonte)
        escrever(str(recorde) + ' pontos | ' + data_recorde + ' ' + hora_recorde, 120, 445, branco, fonte)
        pygame.draw.rect(tela, ciano, (310, 555, 380, 60), border_radius=10)
        escrever('JOGAR NOVAMENTE' if resultado == 'MISSAO CONCLUIDA' else 'REINICIAR', 375, 574, preto, media)
        escrever(aviso_log, 65, 630, amarelo, pequena)

    pygame.display.update()
    relogio.tick(60)
