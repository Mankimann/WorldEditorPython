import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from Entity import Player
from Utils.camera import Camera
from Utils.ObjLoader import ObjLoader
from Utils.TextureLoader import load_texture
import Shader.ShaderProgram as ShaderProgram
import ASI


WIDTH, HEIGHT = 1280, 980
lastX, lastY = WIDTH / 2, HEIGHT / 2

cam = Camera()


class Game:

    proj_loc = glGetUniformLocation(ShaderProgram.shader, "projection")
    view_loc = glGetUniformLocation(ShaderProgram.shader, "view")

    def __init__(self):
        self.title = "LaughTale Game"
        self.width = WIDTH
        self.height = HEIGHT
        self.Fullscreen = False
        self.Wireframe = False

    def create_Display(self):

        # initializing glfw library
        if not glfw.init():
            raise Exception("glfw can not be initialized!")

        # creating the window
        window = glfw.create_window(self.width, self.height, self.title, None, None)

        # check if window was created
        if not window:
            glfw.terminate()
            raise Exception("glfw window can not be created!")

        # set window's position
        glfw.set_window_pos(window, 400, 200)


        # set the callback function for window resize
        glfw.set_window_size_callback(window, window_resize_clb)
        # set the mouse position callback
        glfw.set_cursor_pos_callback(window, Player.mouse_look_clb)
        # set the keyboard input callback
        glfw.set_key_callback(window, Player.key_input_clb)
        # capture the mouse cursor
        # make the context current
        glfw.make_context_current(window)

        glUseProgram(ShaderProgram.shader)
        glClearColor(0, 0.1, 0.1, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        projection = pyrr.matrix44.create_perspective_projection_matrix(45, WIDTH / HEIGHT, 0.1, 100)

        glUniformMatrix4fv(Game.proj_loc, 1, GL_FALSE, projection)

        while not glfw.window_should_close(window):
            glfw.poll_events()
            Player.CameraMovement()
            # glClearColor(1, 0, 0, 1)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            view = cam.get_view_matrix()
            glUniformMatrix4fv(Game.view_loc, 1, GL_FALSE, view)

            # loadTerrain()

            glfw.swap_buffers(window)

        glfw.terminate()


def window_resize_clb(width, height):
    glViewport(0, 0, width, height)
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
    glUniformMatrix4fv(Game.proj_loc, 1, GL_FALSE, projection)


if __name__ == '__main__':
    game = Game()
    game.create_Display()

