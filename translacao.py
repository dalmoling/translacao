import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

pos_x = 0.0
pos_y = 0.0
rotation_angle = 0.0  
move_speed = 0.05  
rotation_speed = 5.0  
square_size = 0.2 

def key_callback(window, key, scancode, action, mods):
    global pos_x, pos_y, rotation_angle, move_speed, rotation_speed
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_W:  
            pos_y += move_speed
        elif key == glfw.KEY_S:  
            pos_y -= move_speed
        elif key == glfw.KEY_A: 
            pos_x -= move_speed
        elif key == glfw.KEY_D: 
            pos_x += move_speed
        elif key == glfw.KEY_Q: 
            rotation_angle -= rotation_speed
        elif key == glfw.KEY_E: 
            rotation_angle += rotation_speed

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  
    glEnable(GL_DEPTH_TEST)


    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800 / 600, 0.1, 50.0) 
    glMatrixMode(GL_MODELVIEW)

def draw_square():
    global rotation_angle

    glPushMatrix() 
    glRotatef(rotation_angle, 0.0, 0.0, 1.0)

    glBegin(GL_QUADS)
    glColor3f(0.0, 0.0, 1.0)  
    glVertex3f(-square_size, square_size, 0.0)  # Ponto superior esquerdo
    glVertex3f(square_size, square_size, 0.0)   # Ponto superior direito
    glVertex3f(square_size, -square_size, 0.0)  # Ponto inferior direito
    glVertex3f(-square_size, -square_size, 0.0) # Ponto inferior esquerdo
    glEnd()

    glPopMatrix()

def display(window):
    global pos_x, pos_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(0.0, 0.0, -5) 
    glTranslatef(pos_x, pos_y, 0.0)  # Mover o quadrado de acordo com as teclas

    draw_square()

    # Atualizar a tela
    glfw.swap_buffers(window)

def main():
    global pos_x, pos_y  # Declarando as variáveis globais para que possam ser acessadas e modificadas

    if not glfw.init():
        print("Erro ao inicializar o GLFW")
        return

    # Criar a janela
    window = glfw.create_window(800, 600, "Quadrado Azul Movendo e Rotacionando", None, None)
    
    if not window:
        print("Erro ao criar a janela GLFW")
        glfw.terminate()
        return

    glfw.make_context_current(window)

    glfw.set_key_callback(window, key_callback)

    init()

    while not glfw.window_should_close(window):
        display(window)  
        glfw.poll_events() 

    glfw.terminate()

if __name__ == "__main__":
    main()
