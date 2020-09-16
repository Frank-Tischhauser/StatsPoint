import webbrowser


from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase


class Tab(MDFloatLayout, MDTabsBase):
    """Class implementing content for a tab."""
    def open_url(self, url):
        webbrowser.open(url)


class TrainingScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def on_pre_enter(self, *args):
        self.app.root.ids.my_toolbar.right_action_items = [["settings", lambda x:
                                                            self.app.root.ids.my_toolbar.show_dialog_confirmation()]]
        self.app.root.ids.my_toolbar.title = 'Training'
        self.ids.android_tabs.background_color = self.app.root.ids.my_toolbar.md_bg_color

    def on_tab_switch(
        self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        instance_tab.name = tab_text


