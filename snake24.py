
# SNAKE 24 - JUEGO DE SERPIENTE CLÁSICO EN PYTHON
# JESÚS DELGADO SÁNCHEZ / MIGUEL SANCHEZ-LA FUENTE BOSCH
# 1º DAM - IES MAJUELO

import pygame
import random

# Inicialización de Pygame y configuración del juego
pygame.init()
ANCHO, ALTO = 1280, 960  # Tamaño de la ventana
ventana = pygame.display.set_mode((ANCHO, ALTO))  # Establecer la ventana
pygame.display.set_caption("SNAKE 24")  # Título de la ventana
BLANCO, NEGRO, VERDE, ROJO, AMARILLO = (255, 255, 255), (0, 0, 0), (0, 255, 0), (255, 0, 0), (255, 255, 0)  # Colores
fuente, fuente_grande = pygame.font.Font("chakrapetch.ttf", 24), pygame.font.Font("chakrapetch.ttf", 100)  # Fuentes
reloj = pygame.time.Clock()  # Controlar los FPS
SIZE_CELDA = 20  # Tamaño de la celda

# Texto centrado (menú y game over)
def texto(text, font, color, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(ANCHO // 2, y))
    ventana.blit(text_surface, text_rect)

# Texto a la derecha (puntuación)
def texto_der(text, font, color, y, extra_text="", extra_color=None):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(ANCHO // 1.1, y))
    ventana.blit(text_surface, text_rect)

    if extra_text and extra_color: # Color para los puntos
        extra_surface = font.render(extra_text, True, extra_color)
        extra_rect = extra_surface.get_rect(
            midleft=(text_rect.right + 5, text_rect.centery))
        ventana.blit(extra_surface, extra_rect)

# Menú del juego
def menu_principal():
    while True:
        ventana.fill(NEGRO)
        texto("SNAKE 24", fuente_grande, AMARILLO, ALTO // 4)
        texto("Presiona ENTER para Jugar", fuente, BLANCO, ALTO // 2)
        texto("Presiona ESC para Salir", fuente, BLANCO, ALTO // 2 + 100)
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: # Salir del juego si se cierra la ventana
                return "salir"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN: # Jugar una partida
                    return "jugar"
                elif evento.key == pygame.K_ESCAPE: # Salir del juego
                    return "salir"

# Clase para la serpiente
class Serpiente:
    def __init__(self):
        # Usamos coordenadas (x, y) en lugar de Rect
        self.body = [(5, 5), (4, 5), (3, 5)]
        self.direction = pygame.Vector2(1, 0)  # Dirección inicial
        self.grow = False

    def movimiento(self):
        # Nueva cabeza calculada con las coordenadas actuales
        nueva_cabeza = (self.body[0][0] + int(self.direction.x),
                        self.body[0][1] + int(self.direction.y))

        # Detectar colisión con bordes
        if not (0 <= nueva_cabeza[0] < ANCHO // SIZE_CELDA and 0 <= nueva_cabeza[1] < ALTO // SIZE_CELDA):
            return False  # Colisión con bordes

        # Detectar colisión con el cuerpo
        if nueva_cabeza in self.body[2:]:
            return False  # Colisión con el cuerpo

        # Actualizar la posición de la serpiente
        self.body.insert(0, nueva_cabeza)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

        return True

    def crecer_serpiente(self):
        self.grow = True

    def dibujar_serpiente(self):
        for x, y in self.body:
            pygame.draw.rect(ventana, VERDE, pygame.Rect(x * SIZE_CELDA, y * SIZE_CELDA, SIZE_CELDA, SIZE_CELDA))

# Clase para la comida
class Comida:
    def __init__(self):
        self.position = self.nueva_posicion()

    @staticmethod
    def nueva_posicion():
        # Generar una posición aleatoria en celdas
        return random.randint(0, (ANCHO // SIZE_CELDA) - 1), random.randint(0, (ALTO // SIZE_CELDA) - 1)

    def dibujar_comida(self):
        x, y = self.position
        pygame.draw.rect(ventana, AMARILLO, pygame.Rect(x * SIZE_CELDA, y * SIZE_CELDA, SIZE_CELDA, SIZE_CELDA))

# Función para iniciar el juego
def iniciar_juego():
    serpiente = Serpiente() # Iniciar la serpiente
    comida = Comida() # Iniciar la comida
    puntos = 0 # Puntuación inicial

    while True:
        ventana.fill(NEGRO)
        texto_der("PUNTOS", fuente, BLANCO, 30, extra_text=str(puntos), extra_color=AMARILLO) # Puntuación en la partida
        eventos(serpiente) # Iniciar eventos de teclado

        if not eventos(serpiente):  # Manejar eventos
            return puntos  # Fin del juego si el jugador cierra la ventana

        if not serpiente.movimiento():  # Detectar colisiones en el movimiento
            return puntos  # Terminar juego si colisiona

        # Comprobar si la serpiente come la comida
        if serpiente.body[0] == comida.position:
            puntos += 10
            serpiente.crecer_serpiente()
            comida.position = comida.nueva_posicion()

        # Dibujar elementos del juego
        serpiente.dibujar_serpiente()
        comida.dibujar_comida()
        pygame.display.update()

        # Ajustar velocidad del juego basada en los puntos (10/50 fps)
        if puntos >= 1000:
            velocidad = 50
        elif puntos >= 600:
            velocidad = 40
        elif puntos >= 300:
            velocidad = 30
        elif puntos >= 150:
            velocidad = 20
        elif puntos >= 50:
            velocidad = 15
        else:
            velocidad = 10
            
        reloj.tick(velocidad)

# Manejar eventos del teclado
def eventos(serpiente):
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            quit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP and serpiente.direction.y == 0:
                serpiente.direction = pygame.Vector2(0, -1)
            elif evento.key == pygame.K_DOWN and serpiente.direction.y == 0:
                serpiente.direction = pygame.Vector2(0, 1)
            elif evento.key == pygame.K_LEFT and serpiente.direction.x == 0:
                serpiente.direction = pygame.Vector2(-1, 0)
            elif evento.key == pygame.K_RIGHT and serpiente.direction.x == 0:
                serpiente.direction = pygame.Vector2(1, 0)
    return True

# Función para manejar la finalización del juego
def game_over(puntos):
    ventana.fill(NEGRO)
    texto(f"¡Game Over! Puntos: {puntos}", fuente, BLANCO, ALTO // 3) # Mostrar la puntuación final
    texto("Presiona ENTER para volver al menú", fuente, BLANCO, ALTO - 50) # Informa al jugador que puede volver al menú principal
    pygame.display.update()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit() # Salir si se cierra la ventana
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN: # Volver al menú principal
                    return

# Función principal del juego
def main():
    while True:
        action = menu_principal()
        if action == "salir": # Salir del juego
            pygame.quit()
            quit()
        elif action == "jugar": # Jugar una partida
            puntos = iniciar_juego()
            game_over(puntos)

if __name__ == "__main__":
    main()
