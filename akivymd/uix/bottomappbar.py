from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.properties import ListProperty, StringProperty, NumericProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock

from kivymd.uix.behaviors import MagicBehavior
from kivymd.theming import ThemableBehavior

Builder.load_string(
    """
<AKFloatingRoundedAppbarItemBase>:
    orientation: 'vertical'
    size_hint: None, None 
    height: self.parent.height- dp(5)
    width: self.minimum_width
    pos_hint: {'center_x': .5, 'center_y': .5}

<AKFloatingRoundedAppbarButtonItem>:
    MDIcon:
        icon: root.icon
        halign: 'center'
        valign: 'center'
        theme_text_color: 'Custom'
        text_color: root.icon_color if root.icon_color else 1,1,1,1
        font_size: dp(20)
        pos_hint: {'center_x': .5, 'center_y': .5}
        size_hint: None, None 
        size: self.font_size, self.font_size 

    Label:
        text: root.text
        halign: 'center'
        valign: 'center'
        font_size: dp(10)
        color: root.text_color if root.text_color else 1,1,1,1
        size_hint: None,None 
        size: self.texture_size 

<AKFloatingRoundedAppbarAvatarItem>:
    BoxLayout:
        size_hint: None,None 
        size : [self.parent.height,self.parent.height]
        pos_hint: {'center_x': .5, 'center_y': .5}
        canvas.after:
            Color: 
                rgba: 1,1,1,1
            Ellipse: 
                pos: self.pos 
                size: self.size 
                source: root.source

<AKFloatingRoundedAppbar>:
    size_hint: None,None 
    size: self.minimum_width, dp(40)
    pos_hint: {'center_x': .5}
    y: dp(10)
    spacing: dp(40)
    padding: dp(40)
    canvas.before:
        Color:
            rgba: root.bg_color if root.bg_color else root.theme_cls.primary_color
        RoundedRectangle:
            pos: self.pos 
            size: self.size 
            radius: [root.height/2,]

    """
)

class AKFloatingRoundedAppbarItemBase(ThemableBehavior, ButtonBehavior, MagicBehavior, BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda x: self._update() )

    def _update(self):
        if self.parent.press_effect:
            self.bind(on_press=lambda x: self.grow() )

class AKFloatingRoundedAppbarButtonItem(AKFloatingRoundedAppbarItemBase):
    text_color= ListProperty() 
    icon_color= ListProperty()
    icon= StringProperty()
    text= StringProperty()

class AKFloatingRoundedAppbarAvatarItem(AKFloatingRoundedAppbarItemBase):
    source= StringProperty() 

class AKFloatingRoundedAppbar(ThemableBehavior, BoxLayout):
    bg_color= ListProperty()
    press_effect= BooleanProperty(True)
