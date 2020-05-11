from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivymd.uix.button import MDRectangleFlatButton

from Tennis_app.score import Player

Window.size = 350, 500


class HomeScreen(Screen):
    pass


class InputScreen(Screen):
    pass


class CreateButton(MDRectangleFlatButton, Player):
    def __init__(self, **kwargs):
        super(CreateButton, self).__init__(**kwargs)

    def on_press(self):
        player1 = Player(self.player1_name)
        player2 = Player(self.player2_name)
        GameScreen.player1 = player1
        GameScreen.player2 = player2


class GameScreen(Screen):
    player1 = Player()
    player2 = Player()

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)


class TennisApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        return Builder.load_file("main.kv")


if __name__ == "__main__":
    TennisApp().run()
