"""
MyToolbar

Represents a KivyMD toolbar.
"""

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.toolbar import MDToolbar


class MyToolbar(MDToolbar):
    """
    Represents KivyMD Toolbar.
    ...
    Attributes
    ----------
    app : object
        Instance of the class TennistatsApp.

    confirmation : object
        Instance of the class MDDialog.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.confirmation = None

    def show_dialog_confirmation(self):
        """Shows a dialog box to confirm the user's choice"""
        if not self.confirmation:
            self.confirmation = MDDialog(
                title='Do you want to leave this screen?', size_hint=(0.7, 1), buttons=[
                    MDFlatButton(text='Yes', text_color=self.app.theme_cls.primary_color,
                                 on_press=lambda x: self.app.change_screen('setting_screen'),
                                 on_release=lambda x: self.dismiss_confirmation()),
                    MDFlatButton(text='No, Cancel', text_color=self.app.theme_cls.primary_color,
                                 on_release=lambda x: self.dismiss_confirmation())])
        self.confirmation.open()

    def dismiss_confirmation(self):
        """Dismisses confirmation dialog box"""
        self.confirmation.dismiss()
