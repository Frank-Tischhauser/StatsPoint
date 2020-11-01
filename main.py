"""
StatsPoint.

This module helps tennis players to improve their game by saving the data of their games.
The user / spectator enters the result of every point until the end of the match.
He also gives additional information on every point.

Example : Bob wins the first point (Backhand winner)

Then the app saves all the data and shows interesting and useful statistics.
The app also helps the player by giving interesting drills depending on the results.

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
from kivy.utils import platform
from kivy.utils import get_color_from_hex
from kivy.core.text import LabelBase
from kivymd.color_definitions import palette, colors
from kivy.config import Config


# All the imports below are actually necessary (Do not remove them!!)

from gamescreen import GameScreen
from mytoolbar import MyToolbar
from inputscreen import InputScreen
from savescreen import SaveScreen
from datascreen import DataScreen
from formscreen import FormScreen
from diagramscreen import DiagramScreen
from trainingscreen import TrainingScreen


if platform == 'win':
    Window.size = (350, 600)
#  Simulate a phone screen

Config.set('kivy', 'exit_on_escape', '0')  # To avoid app shutdown by pressing 'return' on phone


class NavDrawer(MDNavigationDrawer):
    """Navigation Drawer controlled by the toolbar"""


class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = StatsPointApp.get_running_app()
        self.condition = False

    def on_pre_enter(self, *args):
        if self.condition:  # Makes sure it doesn't happen the first time
            self.app.root.ids.my_toolbar.right_action_items = [["cog", lambda x:
                                                                self.app.root.ids.my_toolbar.show_dialog_confirmation()]]
        else:
            self.condition = True
    """Homepage"""


class SettingScreen(MDScreen):
    """Screen that contains all the settings"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = StatsPointApp.get_running_app()

    def on_pre_enter(self, *args):
        self.app.root.ids.my_toolbar.title = 'Settings'


class StatsPointApp(MDApp):
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
    icon = 'windows_logo.png'

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
        log.info(get_color_from_hex(colors[palette[0]]['500']))

        return Builder.load_file("kv/main.kv")

    def on_start(self):
        self.root.ids.data_screen.start()

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
    StatsPointApp().run()
