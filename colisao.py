import glfw
from OpenGL.GL import *
import math
import random

x, y = 0.0, 0.0
angulo = 0.0
velocidade = 0.0
aceleracao = 0.0015
velocidade_max = 0.005
misseis = []

RAIO_NAVE = 0.045  # Ajustado para o novo tamanho
RAIO_ASTEROIDE = 0.06

# Estrelas
num_estrelas = random.randint(100, 150)
estrelas = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(num_estrelas)]

# Asteroides
num_asteroides = random.randint(3, 5)
asteroides = []
asteroide_angulos = []
asteroide_formas = []
asteroide_velocidades = []

for _ in range(num_asteroides):
    ax = random.uniform(-1, 1)
    ay = random.uniform(-1, 1)
    asteroides.append([ax, ay])
    asteroide_angulos.append(random.uniform(0, 360))

    forma = []
    for i in range(60):
        angle = i * 2 * math.pi / 60
        offset = 0.05 + random.uniform(-0.015, 0.015)
        forma.append((math.cos(angle) * offset, math.sin(angle) * offset))
    asteroide_formas.append(forma)

    vx = random.uniform(-0.002, 0.002)
    vy = random.uniform(-0.002, 0.002)
    asteroide_velocidades.append((vx, vy))


def inicio():
    glClearColor(0, 0, 0, 1)

def desenha_estrelas():
    glColor3f(1, 1, 1)
    glPointSize(3)
    glBegin(GL_POINTS)
    for estrela in estrelas:
        glVertex2f(*estrela)
    glEnd()

def desenha_asteroides():
    glColor3f(0.4, 0.4, 0.4)
    for i, (ax, ay) in enumerate(asteroides):
        glPushMatrix()
        glTranslatef(ax, ay, 0)
        glRotatef(asteroide_angulos[i], 0, 0, 1)
        glBegin(GL_POLYGON)
        for vx, vy in asteroide_formas[i]:
            glVertex2f(vx, vy)
        glEnd()
        glPopMatrix()

def desenha_misseis():
    glColor3f(0.2, 0.6, 1.0)
    for m in misseis:
        glPushMatrix()
        glTranslatef(m["x"], m["y"], 0)
        glRotatef(m["angulo"], 0, 0, 1)
        glBegin(GL_TRIANGLES)
        glVertex2f(0.0, 0.05)
        glVertex2f(-0.01, -0.02)
        glVertex2f(0.01, -0.02)
        glEnd()
        glPopMatrix()

def desenha_nave():
    glPushMatrix()
    glTranslatef(x, y, 0)
    glRotatef(angulo, 0, 0, 1)

    escala = 0.6  # Fator de redução da nave

    glColor3f(1, 1, 1)
    glBegin(GL_TRIANGLES)
    glVertex2f(0.0 * escala, 0.2 * escala)
    glVertex2f(-0.06 * escala, -0.05 * escala)
    glVertex2f(0.06 * escala, -0.05 * escala)
    glEnd()

    glColor3f(0.8, 0.8, 0.8)
    glBegin(GL_TRIANGLES)
    glVertex2f(-0.06 * escala, -0.05 * escala)
    glVertex2f(-0.12 * escala, -0.15 * escala)
    glVertex2f(0.0 * escala, -0.07 * escala)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(0.06 * escala, -0.05 * escala)
    glVertex2f(0.12 * escala, -0.15 * escala)
    glVertex2f(0.0 * escala, -0.07 * escala)
    glEnd()

    glColor3f(0.9, 0.9, 0.9)
    glBegin(GL_TRIANGLES)
    glVertex2f(-0.04 * escala, -0.1 * escala)
    glVertex2f(0.04 * escala, -0.1 * escala)
    glVertex2f(0.0 * escala, -0.18 * escala)
    glEnd()

    glPopMatrix()

def desenha():
    glClear(GL_COLOR_BUFFER_BIT)
    desenha_estrelas()
    desenha_asteroides()
    desenha_misseis()
    desenha_nave()
    glFlush()

def atualizar_movimento():
    global x, y
    rad = math.radians(angulo + 90)
    x += math.cos(rad) * velocidade
    y += math.sin(rad) * velocidade

    if x > 1: x = -1
    if x < -1: x = 1
    if y > 1: y = -1
    if y < -1: y = 1

def atualizar_misseis():
    for m in misseis:
        rad = math.radians(m["angulo"] + 90)
        m["x"] += math.cos(rad) * m["vel"]
        m["y"] += math.sin(rad) * m["vel"]
    misseis[:] = [m for m in misseis if -1.0 < m["x"] < 1.0 and -1.0 < m["y"] < 1.0]

def atualizar_asteroide_rotacao():
    for i in range(len(asteroide_angulos)):
        asteroide_angulos[i] = (asteroide_angulos[i] + 1.0) % 360

def atualizar_asteroide_movimento():
    for i in range(len(asteroides)):
        asteroides[i][0] += asteroide_velocidades[i][0]
        asteroides[i][1] += asteroide_velocidades[i][1]

        if asteroides[i][0] > 1.0:
            asteroides[i][0] = -1.0
        elif asteroides[i][0] < -1.0:
            asteroides[i][0] = 1.0

        if asteroides[i][1] > 1.0:
            asteroides[i][1] = -1.0
        elif asteroides[i][1] < -1.0:
            asteroides[i][1] = 1.0

def verificar_colisoes():
    global x, y, velocidade
    for ax, ay in asteroides:
        distancia = math.sqrt((x - ax) ** 2 + (y - ay) ** 2)
        if distancia < (RAIO_NAVE + RAIO_ASTEROIDE):
            print("💥 COLISÃO DETECTADA!")
            x, y = 0.0, 0.0
            velocidade = 0.0
            break

def tecla_callback(window, key, scancode, action, mods):
    global angulo, velocidade, misseis, x, y

    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_LEFT:
            angulo += 10
        elif key == glfw.KEY_RIGHT:
            angulo -= 10
        elif key == glfw.KEY_UP:
            if velocidade < velocidade_max:
                velocidade += aceleracao
        elif key == glfw.KEY_DOWN:
            if velocidade > -velocidade_max:
                velocidade -= aceleracao
    if action == glfw.PRESS:
        if key == glfw.KEY_SPACE:
            rad = math.radians(angulo + 90)
            mx = x + math.cos(rad) * 0.15
            my = y + math.sin(rad) * 0.15
            misseis.append({
                "x": mx,
                "y": my,
                "angulo": angulo,
                "vel": velocidade + 0.003
            })

def main():
    if not glfw.init():
        return

    window = glfw.create_window(900, 1000, "Nave DALMO", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, tecla_callback)
    inicio()

    while not glfw.window_should_close(window):
        atualizar_movimento()
        atualizar_misseis()
        atualizar_asteroide_movimento()
        atualizar_asteroide_rotacao()
        verificar_colisoes()
        desenha()
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
