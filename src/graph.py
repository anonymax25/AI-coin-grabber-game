import PIL.Image
import arcade
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure


def render_figure(fig):
    canvas = FigureCanvasAgg(fig)
    data, size = canvas.print_to_buffer()
    return PIL.Image.frombuffer("RGBA", size, data)


class Graph(arcade.View):
    def __init__(self, x, y):
        super().__init__()
        self.__x = x
        self.__y = y
        self.__image = None
        self.setup()

    def draw_figure(self, fig):
        ax = fig.add_subplot(111)
        ax.set_title("statistics", fontsize=22)
        ax.set_xlabel('Iterations', fontsize=18)
        ax.set_ylabel('Score', fontsize=18)
        ax.plot(self.__x, self.__y)

    def setup(self):
        dpi_res = min(self.window.width, self.window.height) / 10
        fig = Figure((self.window.width / dpi_res, self.window.height / dpi_res), dpi=dpi_res)
        self.draw_figure(fig)
        self.__image = render_figure(fig)

    def on_draw(self):
        arcade.start_render()
        self.window.scene.draw()
        width = self.window.width
        height = self.window.height
        arcade.Texture("stats", self.__image).draw_sized(width / 2, height / 2, width, height)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            from src.menu import Menu
            menu_view = Menu()
            self.window.show_view(menu_view)
