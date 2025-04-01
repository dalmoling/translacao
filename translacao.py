import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Variáveis para controlar a posição e a rotação do quadrado
pos_x = 0.0
pos_y = 0.0
rotation_angle = 0.0  # Ângulo de rotação do quadrado
move_speed = 0.05  # Velocidade de movimentação do quadrado
rotation_speed = 5.0  # Velocidade de rotação (graus por iteração)
square_size = 0.2  # Tamanho do quadrado

# Função de callback para capturar as teclas pressionadas
def key_callback(window, key, scancode, action, mods):
    global pos_x, pos_y, rotation_angle, move_speed, rotation_speed
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_W:  # Mover para cima
            pos_y += move_speed
        elif key == glfw.KEY_S:  # Mover para baixo
            pos_y -= move_speed
        elif key == glfw.KEY_A:  # Mover para a esquerda
            pos_x -= move_speed
        elif key == glfw.KEY_D:  # Mover para a direita
            pos_x += move_speed
        elif key == glfw.KEY_Q:  # Rotacionar para a esquerda
            rotation_angle -= rotation_speed
        elif key == glfw.KEY_E:  # Rotacionar para a direita
            rotation_angle += rotation_speed

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Cor de fundo preta
    glEnable(GL_DEPTH_TEST)  # Habilitar o teste de profundidade

    # Configuração da projeção
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800 / 600, 0.1, 50.0)  # Perspectiva
    glMatrixMode(GL_MODELVIEW)

def draw_square():
    global rotation_angle

    # Aplicando rotação ao quadrado
    glPushMatrix()  # Salvar o estado atual da transformação
    glRotatef(rotation_angle, 0.0, 0.0, 1.0)  # Rotacionar o quadrado

    # Desenha um quadrado azul
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.0, 1.0)  # Azul
    glVertex3f(-square_size, square_size, 0.0)  # Ponto superior esquerdo
    glVertex3f(square_size, square_size, 0.0)   # Ponto superior direito
    glVertex3f(square_size, -square_size, 0.0)  # Ponto inferior direito
    glVertex3f(-square_size, -square_size, 0.0) # Ponto inferior esquerdo
    glEnd()

    glPopMatrix()  # Restaurar o estado da transformação

def display(window):
    global pos_x, pos_y

    # Limpar tela e buffer de profundidade
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Movendo a câmera para a posição correta
    glTranslatef(0.0, 0.0, -5)  # Afastar a cena para visualizar o quadrado
    glTranslatef(pos_x, pos_y, 0.0)  # Mover o quadrado de acordo com as teclas

    # Desenhar o quadrado
    draw_square()

    # Atualizar a tela
    glfw.swap_buffers(window)

def main():
    global pos_x, pos_y  # Declarando as variáveis globais para que possam ser acessadas e modificadas

    # Inicializar o GLFW
    if not glfw.init():
        print("Erro ao inicializar o GLFW")
        return

    # Criar a janela
    window = glfw.create_window(800, 600, "Quadrado Azul Movendo e Rotacionando", None, None)
    
    # Verificar se a janela foi criada corretamente
    if not window:
        print("Erro ao criar a janela GLFW")
        glfw.terminate()
        return

    # Tornar o contexto OpenGL atual
    glfw.make_context_current(window)

    # Configurar o callback para as teclas pressionadas
    glfw.set_key_callback(window, key_callback)

    # Inicializar o OpenGL
    init()

    # Loop principal
    while not glfw.window_should_close(window):
        # Atualizar e desenhar o quadrado
        display(window)  
        glfw.poll_events()  # Processar eventos como teclas pressionadas

    # Finalizar o GLFW
    glfw.terminate()

if __name__ == "__main__":
    main()
