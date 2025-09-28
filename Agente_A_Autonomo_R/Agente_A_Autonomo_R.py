# Equipo 2
# Marcela Jimenez Mendez
# Eduardo Velazquez Perez
# José Elías Guzmán Miranda

import pygame
import random
import time

# ============================
# Estadísticas
# ============================
movimientos_agentes = 0
tiempo_inicio = time.time()
limpieza_completa = False
tiempo_total = 0

# ============================
# Configuración de la pantalla
# ============================
ANCHO, ALTO = 400, 400
TAMANIO_CELDA = 40
FILAS = ANCHO // TAMANIO_CELDA
COLUMNAS = ALTO // TAMANIO_CELDA

# ============================
# Colores
# ============================
COLOR_FONDO = (30, 30, 30)
COLOR_SUCIO = (139, 69, 19)
COLOR_LIMPIO = (255, 255, 255)
COLOR_ASPIRADOR = (0, 255, 0)
COLOR_PANEL = (0, 20, 20)
COLOR_BORDE_PANEL = (100, 100, 10)
COLOR_TEXTO = (255, 255, 0)
NUMERO_ASPIRADORAS = 2

# ============================
# Inicializar Pygame
# ============================
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Aspiradoras Autónomas con Estadísticas")
pygame.font.init()
fuente = pygame.font.SysFont("Times New Roman", 20, bold=True)

# ============================
# Generar el entorno
# ============================
entorno = [[random.choice([0, 1]) for _ in range(COLUMNAS)] for _ in range(FILAS)]

# ============================
# Posición inicial de las aspiradoras
# ============================
aspiradoras = []
for _ in range(NUMERO_ASPIRADORAS):
    a_x = random.randint(0, FILAS - 1)
    a_y = random.randint(0, COLUMNAS - 1)
    aspiradoras.append({"x": a_x, "y": a_y})

# ============================
# Función para mover aleatoriamente
# ============================
def mover_aspirador(x, y):
    movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    random.shuffle(movimientos)
    for dx, dy in movimientos:
        nuevo_x, nuevo_y = x + dx, y + dy
        if 0 <= nuevo_x < FILAS and 0 <= nuevo_y < COLUMNAS:
            return nuevo_x, nuevo_y
    return x, y

# ============================
# Buscar celda sucia cercana
# ============================
def buscar_celda_sucia(x, y):
    movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for dx, dy in movimientos:
        sx, sy = x + dx, y + dy
        if 0 <= sx < FILAS and 0 <= sy < COLUMNAS:
            if entorno[sx][sy] == 1:
                return sx, sy
    return None

# ============================
# Mostrar estadísticas en pantalla
# ============================
def mostrar_estadisticas(pantalla, movimientos, sucias, tiempo, finalizado):
    panel_w, panel_h = 180, 100
    panel_x, panel_y = 10, 10

    panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 150))
    pantalla.blit(panel, (panel_x, panel_y))

    texto1 = fuente.render(f"Movimientos: {movimientos}", True, COLOR_TEXTO)
    texto2 = fuente.render(f"Sucias restantes: {sucias}", True, COLOR_TEXTO)
    texto3 = fuente.render(f"Tiempo: {tiempo:.2f}s", True, COLOR_TEXTO)

    pantalla.blit(texto1, (panel_x + 10, panel_y + 10))
    pantalla.blit(texto2, (panel_x + 10, panel_y + 35))
    pantalla.blit(texto3, (panel_x + 10, panel_y + 60))

    if finalizado:
        mensaje = fuente.render("¡Limpieza completa!", True, (0, 255, 255))
        pantalla.blit(mensaje, (panel_x + 10, panel_y + 80))

# ============================
# Bucle principal
# ============================
ejecutando = True
while ejecutando:
    pygame.time.delay(500)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    if not limpieza_completa:
        for aspirador in aspiradoras:
            x, y = aspirador["x"], aspirador["y"]
            if entorno[x][y] == 1:
                entorno[x][y] = 0
            else:
                objetivo = buscar_celda_sucia(x, y)
                if objetivo:
                    aspirador["x"], aspirador["y"] = objetivo
                else:
                    nuevo_x, nuevo_y = mover_aspirador(x, y)
                    aspirador["x"], aspirador["y"] = nuevo_x, nuevo_y
                    movimientos_agentes += 1

    casillas_sucias = sum(fila.count(1) for fila in entorno)

    if casillas_sucias == 0 and not limpieza_completa:
        tiempo_total = time.time() - tiempo_inicio
        limpieza_completa = True
        print("¡Entorno completamente limpio!")
        print(f"Movimientos totales: {movimientos_agentes}")
        print(f"Tiempo total de limpieza: {tiempo_total:.2f} segundos")

    tiempo_actual = tiempo_total if limpieza_completa else time.time() - tiempo_inicio

    pantalla.fill(COLOR_FONDO)
    for i in range(FILAS):
        for j in range(COLUMNAS):
            color = COLOR_SUCIO if entorno[i][j] == 1 else COLOR_LIMPIO
            pygame.draw.rect(pantalla, color, (j * TAMANIO_CELDA, i * TAMANIO_CELDA, TAMANIO_CELDA, TAMANIO_CELDA))

    for aspirador in aspiradoras:
        pygame.draw.rect(
            pantalla,
            COLOR_ASPIRADOR,
            (aspirador["y"] * TAMANIO_CELDA, aspirador["x"] * TAMANIO_CELDA, TAMANIO_CELDA, TAMANIO_CELDA),
        )

    mostrar_estadisticas(pantalla, movimientos_agentes, casillas_sucias, tiempo_actual, limpieza_completa)
    pygame.display.update()

pygame.quit()
