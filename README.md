# ABYSS COCKPIT: DEPTH ZERO

Jogo academico desenvolvido a partir da logica de Deep Sea Evade: variaveis,
condicoes, eventos, funcoes simples e retangulos. O exemplo original permanece
em main.py apenas como referencia. O jogo novo inicia por jogo.py.

## Desenvolvedores

- Nome completo: PREENCHER — RA: PREENCHER
- Nome completo: PREENCHER — RA: PREENCHER

## Historia

Dentro de um batiscafo danificado a 10.000 metros, o piloto precisa chegar a
superficie. O sonar antecipa torpedos, lulas e tubaroes; desvios e equipamentos
preservam o casco. Uma missao dura 10.800 atualizacoes, aproximadamente tres
minutos ativos a 60 FPS. Computadores lentos podem levar mais tempo.

## Tecnologias e excecoes ao exemplo

Nao sao usados classes proprias, sprites, vetores, imagens, motores 3D ou NumPy.
Os graficos sao desenhados por codigo. Recursos externos futuros devem ficar
em bases/. As fontes sao fornecidas pelo sistema via SysFont, como na base.

| Acrescimo | Motivo |
| --- | --- |
| pygame.draw.circle | Circulo amarelo pulsante, item 16 |
| pygame.K_SPACE, K_a e K_d | Pausa e controles horizontais |
| pyttsx3 e seus metodos | Voz na abertura de cada missao, item 19 |
| datetime.now e strftime | Data e hora HH:MM:SS, item 15 |
| open, with, read/write/readline/strip | Persistencia de partidas e recorde |
| try/except e excecoes de arquivo/voz | Ausencia de log, registros invalidos e falhas do sintetizador |
| from Recursos.trabalho import ... | Funcao externa, item 7 |
| return e desempacotamento de tupla | Devolver os quatro campos do recorde |
| range, resto %, divisao inteira //, booleanos | Grade do radar, temporizadores, pausa e dimensoes inteiras |
| pygame.quit | Liberar a janela antes de sys.exit() |
| sys.exit | Fechar tambem no executavel, onde quit() pode nao existir |
| cx_Freeze, setup e Executable | Gerar executavel, item 4; listas/dicionarios usados apenas no setup.py |

## Estrutura

```text
ABYSS-COCKPIT/
    jogo.py
    Recursos/
        __init__.py
        trabalho.py
    bases/
        LEIA-ME.txt
    requirements.txt
    setup.py
    README.md
    log.dat          # gerado ao terminar a primeira partida
    build/           # gerado pelo build
```

## Executar no VS Code

Use Python 3.12. Abra a pasta do projeto e use o terminal integrado, pois o nome
sera solicitado com input(). Nao use execucao em painel sem entrada de teclado.

Windows:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe jogo.py
```

Linux:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python jogo.py
```

Para jogar, e necessario um desktop com display e saida de audio. No Windows,
pyttsx3 usa as vozes do sistema (SAPI5). No Linux, instale o sintetizador de fala
do sistema; no Debian/Ubuntu: `sudo apt install espeak-ng libespeak1 alsa-utils`.
Se a voz falhar, o jogo apresenta um aviso; isso NAO equivale a validar o item de
voz. Verifique a fala no computador da apresentacao.

Execute a partir de uma pasta gravavel. log.dat fica no diretorio de trabalho.
Nao coloque o projeto em pastas protegidas do sistema.

## Controles e mecanicas

- A/D ou setas esquerda/direita: deslocamento somente no eixo X.
- Espaco: pausa/retoma. Durante a pausa, a simulacao e os botoes ficam congelados.
- ESC ou X da janela: fecha; sair no meio da missao nao registra uma partida.
- FAROL: alterna iluminacao, consumindo bateria; desligado recarrega lentamente.
- LIMPADOR: remove tinta; intervalo de 180 quadros ativos (cerca de 3 segundos).
- BOMBA: remove ate 18 pontos percentuais de agua, gastando 8 de bateria.

Um contato por vez aparece primeiro no sonar. Torpedos e tubaroes tiram 20 de
casco e adicionam 18 de agua; lulas tiram 10 de casco, adicionam 8 de agua e tinta.
Casco zero ou agua 100 encerram a missao. Profundidade zero concede vitoria.
Pontos: 5 por segundo ativo, 50 por contato evitado e 1.000 pela vitoria.
O desempate de recordes preserva a primeira partida com a pontuacao maxima.
Cada registro ocupa quatro linhas em log.dat: nome, pontos, data e hora.

## Gerar executavel

Ative o ambiente virtual para que as ferramentas do build estejam no PATH:

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python setup.py build
```

Se a politica local impedir a ativacao, use o Prompt de Comando e execute
`.venv\Scripts\activate.bat`, depois `python setup.py build`.

Linux:

```bash
. .venv/bin/activate
python setup.py build
```

Distribua a pasta completa criada em build/, nao somente o arquivo executavel.
O console permanece aberto porque o nome e solicitado com input(). O build deve
ser feito no sistema de destino: para Windows, gere no Windows. O build Linux
nao e um .exe de Windows. O sintetizador de fala do sistema continua necessario.

## Verificacao e checklist da atividade

- [x] Python e Pygame; tema proprio e graficos procedurais.
- [x] bases/ preparada para recursos externos.
- [x] Funcao util em Recursos/trabalho.py importada por from ... import.
- [x] Tela 1000 x 700, boas-vindas, nome, instrucoes, recorde com data/hora e um unico botao.
- [x] Pausa por Espaco, PAUSE central e frase exata solicitada.
- [x] Controle exclusivamente no eixo X.
- [x] Decoracao com deslocamento aleatorio sem colisao.
- [x] log.dat com nome, pontos, data e hora; recordista tambem no fim de jogo.
- [x] Circulo amarelo pulsante e fechamento por ESC.
- [x] Chamada de pyttsx3 implementada uma vez por inicio de missao.
- [x] setup.py; build Linux gerado durante a validacao.
- [ ] Ouvir a fala no computador de entrega (sintetizador ausente nesta nuvem).
- [ ] Gerar e verificar o executavel no Windows, se esse for o sistema da entrega.
- [ ] Preencher nomes e RAs.
- [x] Cinco novos commits descritivos; build Linux incluido no commit final.
- [ ] Compartilhar com professor/colega; commit do colaborador feito pelo proprio colega.

Validacao automatica sem display: menu, movimento X, pausa sem atualizar estado,
farol, bomba, limpador, dano de lula, derrota, log, recorde, reinicio completo,
vitoria apos 10.800 quadros e Escape. O executavel Linux tambem iniciou e fechou sem erro em um teste sem display. Isso nao substitui testar audio e janela
no computador da apresentacao.

## Commits de entrega

1. Prepara estrutura e dependencias do ABYSS COCKPIT
2. Adiciona funcao externa para indicadores do cockpit
3. Implementa cockpit, ameacas, controles e registros de partidas
4. Documenta controles, instalacao e requisitos da atividade
5. Adiciona configuracao de build e executavel Linux validado

Esses commits organizam os arquivos da entrega; consulte o historico Git para verificar as alteracoes. O PDF cita IronManV2 como base; confirme com o professor
que o exemplo Deep Sea Evade fornecido e aceito como referencia da turma.
