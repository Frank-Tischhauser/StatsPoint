from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class AnalysisScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.match_stats = None

    def on_pre_enter(self, *args):
        self.match_stats = self.app.root.ids.data_screen.match_stats
        self.app.root.ids.my_toolbar.right_action_items = [["arrow-left",
                                                            lambda x: self.app.change_screen('data_screen', 'right')]]
        print(self.match_stats)
