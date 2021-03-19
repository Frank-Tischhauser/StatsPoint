"""
Tennistats.

This module helps tennis players to improve their game by saving the data of their games.
The user / spectator enters the result of every point until the end of the match.
He also gives additional information on every point.

Example : Bob wins the first point (Backhand winner)

Then the app saves all the data and shows interesting and useful statistics.
The app also helps the player by giving interesting drills depending on the results.
"""
import logging as log
import json
from os import path

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.color_definitions import palette, colors
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

from kivy.lang import Builder
from kivy.uix.screenmanager import SlideTransition
from kivy.core.window import Window
from kivy.utils import platform
from kivy.utils import get_color_from_hex
from kivy.core.text import LabelBase
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
    """
    Navigation Drawer controlled by the toolbar
    ...
    Attributes
    ----------
    app : object
        Instance of the class TennistatsApp.

    confirmation_leave : object
        Instance of MDDialog.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = TennistatsApp.get_running_app()
        self.confirmation_leave = None

    def check_game_screen(self, screen_name):
        """Shows a dialog if the user is on the game_screen"""
        self.confirmation_leave = None
        if self.app.root.ids.manager.current == 'game_screen':
            self.show_confirmation_leave(screen_name)
        else:
            self.set_state('close')
            self.app.change_screen(screen_name)

    def show_confirmation_leave(self, screen_name):
        """Shows a dialog box to confirm the user's choice"""
        if not self.confirmation_leave:
            self.confirmation_leave = MDDialog(
                title="Leave the game and loose your save?",
                size_hint=(0.7, 1), buttons=[
                    MDFlatButton(text='[size=16sp]Yes[/size]', text_color=self.app.theme_cls.primary_color,
                                 on_release=lambda x: self.dismiss_confirmation_leave(screen_name),
                                 markup=True),
                    MDFlatButton(text='[size=16sp]No, Cancel[/size]',
                                 text_color=self.app.theme_cls.primary_color,
                                 markup=True,
                                 on_release=lambda x: self.dismiss_confirmation_leave(close=False))])
        self.confirmation_leave.open()

    def dismiss_confirmation_leave(self, screen_name='homepage', close=True):
        """Dismisses confirmation dialog box"""
        self.confirmation_leave.dismiss()
        if close:
            self.set_state('close')
            self.app.change_screen(screen_name)


class HomeScreen(MDScreen):
    """
    Homepage screen.

    ...
    Attributes
    ----------
    app : object
        Instance of the class TennistatsApp.

    condition : bool
        Condition to avoid the calling of some functions during app launch (could cause crash).

    Methods
    -------
    on_pre_enter():
        Is called just before the user sees the screen.

    on_leave():
        Is called when the user leaves the screen.

    check_json_save():
        Checks if the save file exists, and if not creates it.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = TennistatsApp.get_running_app()
        self.condition = False

    def on_pre_enter(self, *args):
        """Is called just before the user sees the screen"""
        if self.condition:  # Makes sure it doesn't happen the first time
            self.app.root.ids.my_toolbar.right_action_items = [
                ["information-outline", lambda x: self.app.root.ids.my_toolbar.show_dialog_confirmation()]]

    def on_leave(self, *args):
        """Is called when the user leaves the screen"""
        self.condition = True
        if self.app.root.ids.manager.current != 'save_screen':
            self.check_json_save()

    def check_json_save(self):
        """Checks if the save file exists, and if not creates it"""
        if not path.exists('../tennistats_data.json'):
            with open('json_files/data_template.json', 'r') as template_file:
                template = json.load(template_file)
            with open('../tennistats_data.json', 'w') as save_file:
                json.dump(template, save_file, indent=4, sort_keys=True)


class SettingScreen(MDScreen):
    """
    Screen that contains all the settings
    ...
    Attributes
    ----------
    app : object
        Instance of the class TennistatsApp.

    dialog : object
        Instance of MDDialog class. It is a UI widget.

    Methods
    -------
    on_pre_enter():
        Is called just before the user sees the screen.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = TennistatsApp.get_running_app()
        self.dialog = None

    def on_pre_enter(self, *args):
        """Is called just before the user sees the screen"""
        self.app.root.ids.my_toolbar.title = 'Help'
        self.app.root.ids.my_toolbar.right_action_items = [
            ["home", lambda x: self.app.change_screen('home_screen')]]

    def show_dialog(self):
        """Shows a dialog box to confirm the user's choice"""

        if not self.dialog:
            self.dialog = MDDialog(
                title="Do you want to quit Tennistats?",
                size_hint=(0.7, 1), buttons=[
                    MDFlatButton(text='[size=16sp]Yes[/size]', text_color=self.app.theme_cls.primary_color,
                                 on_release=lambda x: quit(),
                                 markup=True),
                    MDFlatButton(text='[size=16sp]No, Cancel[/size]',
                                 text_color=self.app.theme_cls.primary_color,
                                 markup=True,
                                 on_release=lambda x: self.dialog.dismiss())])
        self.dialog.open()


class TennistatsApp(MDApp):
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

    on_start():
        Called on launch.

    get_rgba_from_hex(color):
        Converts the hex color format into rgba color format.

    """
    icon = 'assets/logo.png'

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
            name='Lato',
            fn_regular="fonts/Lato-Regular.ttf")
        self.theme_cls.font_styles["H3"] = [
            "Lato",
            16,
            False,
            0.15,
        ]
        log.info(get_color_from_hex(colors[palette[0]]['500']))

        return Builder.load_file("kv/main.kv")

    def on_start(self):
        """Called on launch"""
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
        """Converts the hex color format into rgba color format."""
        return get_color_from_hex(color)


if __name__ == "__main__":
    TennistatsApp().run()
