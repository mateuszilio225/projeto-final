import pygame


def desenhar_indicador(tela, fonte, titulo, valor, x, y, cor):
    # Funcao externa exigida na atividade; usa somente texto e retangulos.
    texto = fonte.render(titulo + ': ' + str(int(valor)) + '%', True, (213, 235, 235))
    tela.blit(texto, (x, y))
    pygame.draw.rect(tela, (7, 18, 28), (x, y + 25, 225, 12))
    pygame.draw.rect(tela, cor, (x, y + 25, int(valor * 2.25), 12))
