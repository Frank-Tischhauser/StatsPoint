"""
Tennis tracker app.

This module helps tennis players to improve their game by saving the data of their games.
The user / spectator enters the result of every point until the end of the match. [x]
He also gives additional information on every point. [x]

Example : Bob wins the first point (Backhand winner)

Then the app saves all the data [x] and shows interesting and useful statistics. []
The app als helps the player by giving interesting advices depending on the results. []

[x] : Done
[] : To Do

Author : Frank Tischhauser
"""
import logging as log

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.font_definitions import theme_font_styles

from kivy.lang import Builder
from kivy.uix.screenmanager import SlideTransition
from kivy.core.window import Window
from kivy.uix.colorpicker import get_color_from_hex
from kivy.core.text import LabelBase


from gamescreen import GameScreen
from mytoolbar import MyToolbar
from inputscreen import InputScreen
from savescreen import SaveScreen
from datascreen import DataScreen

Window.size = (350, 600)
#  Uncomment to simulate a phone screen


class NavDrawer(MDNavigationDrawer):
    """Navigation Drawer controlled by the toolbar"""


class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = TennisApp.get_running_app()
    """Homepage"""


class SettingScreen(MDScreen):
    """Screen that contains all the settings"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = TennisApp.get_running_app()

    def style_switcher(self):
        if not self.ids.style_switch.active:
            self.app.theme_cls.theme_style = 'Light'
        else:
            self.app.theme_cls.theme_style = 'Dark'


class TennisApp(MDApp):
    """
    This class represents the app.
    It is necessary in order to use the kivy/kivyMD module.
    ...
    Methods
    -------
    build():
        Builds the app.
    change_screen(screen_name, direction='left'):
        Switches from one screen to another.
    """
    def __init__(self, **kwargs):  # Temporary, will be probably removed later
        super().__init__(**kwargs)
        self.game_screen = GameScreen()
        self.my_toolbar = MyToolbar()
        self.input_screen = InputScreen()
        self.save_screen = SaveScreen()
        self.data_screen = DataScreen()

    def build(self):
        """
        Creates the app

        Returns
        -------
        file
            A file containing all the kv code
        """
        self.theme_cls.primary_palette = 'Orange'
        self.theme_cls.primary_hue = '600'
        log.info(self.theme_cls.primary_color)
        LabelBase.register(
            name='ProximaNova',
            fn_regular="fonts/ProximaNova-Regular.otf")
        theme_font_styles.append('ProximaNova')
        self.theme_cls.font_styles["H3"] = [
            "ProximaNova",
            16,
            False,
            0.15,
        ]
        return Builder.load_file("kv/main.kv")

    def change_screen(self, screen_name, direction='left'):
        """
        Changes the current screen using the ScreenManager

        Parameters
        ----------
        screen_name : str
            The name of the future current screen
        direction : str
            Chooses the direction of the Slide Transition (It's 'left' by default)
        """
        self.root.ids.manager.transition = SlideTransition(direction=direction)
        self.root.ids.manager.current = screen_name

    def get_rgba_from_hex(self, color):
        return get_color_from_hex(color)


if __name__ == "__main__":
    TennisApp().run()
