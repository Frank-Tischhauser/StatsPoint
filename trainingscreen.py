import webbrowser


from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.button import MDFloatingActionButton
from drill_manager import DrillManager


class Tab(MDFloatLayout, MDTabsBase):
    """Class implementing content for a tab."""


def open_url(url):
    webbrowser.open(url)


class TrainingScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.drill_manager = None
        self.youtube_button = [None, None, None]

    def on_pre_enter(self, *args):
        index = 0
        pages = [self.ids.drill1, self.ids.drill2, self.ids.drill3]
        for widget in self.youtube_button:  # Remove youtube button, if there is one
            if widget is not None:
                pages[index].remove_widget(widget)
                self.youtube_button[index] = None
            index += 1
        self.app.root.ids.my_toolbar.right_action_items = [["cog", lambda x:
                                                            self.app.root.ids.my_toolbar.show_dialog_confirmation()]]
        self.app.root.ids.my_toolbar.title = 'Training'
        self.ids.android_tabs.background_color = self.app.root.ids.my_toolbar.md_bg_color
        self.choose_drill()
        self.show_drill()

    def choose_drill(self):
        self.drill_manager = DrillManager()
        self.drill_manager.sort_drills(self.drill_manager.analysis_info['level'])
        if self.drill_manager.analysis_info['level'] != 'beginner':
            self.drill_manager.make_drill_schedule()
        self.drill_manager.pick_drill()

    def show_drill(self):
        i = 0
        for page in [self.ids.drill1, self.ids.drill2, self.ids.drill3]:
            page.ids.title.text = self.drill_manager.picked_drills[i]['title']
            page.ids.body.text = self.drill_manager.picked_drills[i]['description']
            if self.drill_manager.picked_drills[i]['link'] is not None:
                floating_button = MDFloatingActionButton(pos_hint={'center_x': 0.8, 'center_y': 0.1},
                                                         icon='youtube')
                floating_button.md_bg_color = self.app.theme_cls.primary_color
                floating_button.bind(on_release=lambda x, link=self.drill_manager.picked_drills[i]['link']: open_url(link))
                page.add_widget(floating_button)
                self.youtube_button[i] = floating_button
            i += 1

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        instance_tab.name = tab_text
