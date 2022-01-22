from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty, get_color_from_hex
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivymd.theming import ThemableBehavior

from kivymd.uix.behaviors import RectangularRippleBehavior

from kivymd.uix.boxlayout import MDBoxLayout

from kivymd.uix.list import OneLineListItem, TwoLineListItem

from kivymd.material_resources import dp

from kivymd.uix.card import MDCard

from kivymd.app import MDApp

KV = '''
<List>
    orientation:'vertical'
    size_hint_y:None
    padding: dp(20),dp(15),0,dp(15)
    size_hint_x:1
    height:'50dp'
    elevation:0
    radius:'25dp'
    disable: True
    MDLabel:
        adaptive_height: True
        text:root.primary_text
    MDBoxLayout:
        id: sec_box
        size_hint_y:None
        height:'0dp'
        opacity: 0
        MDLabel:
            adaptive_height:True
            text:root.secondary_text
            theme_text_color:'Secondary'
        MDIconButton:
            id: button
            disabled: root.disable
            md_bg_color_disabled:[0,0,0,0]
            icon:'content-copy'
            pos_hint:{'center_y':.5}
        MDIconButton:
            id: button
            disabled: root.disable
            md_bg_color_disabled:[0,0,0,0]
            icon:'pencil'
            pos_hint:{'center_y':.5}
            # text_color:[.3,.3,.3,1]
'''


class List(ThemableBehavior, ButtonBehavior, MDBoxLayout):  # ThemableBehavior, ButtonBehavior, MDBoxLayout or MDCard
    Builder.load_string(KV)
    active = BooleanProperty(False)
    primary_text = StringProperty('Google')
    ripple_behavior = False
    ripple_alpha = .15
    secondary_text = StringProperty()


    def on_release(self):
        if self.right - self.last_touch.x >= dp(100):
            self.active = not self.active
        for instance in self.parent.children:
            if not instance == self:
                instance.active = False

        # print(self.last_touch)

    def on_active(self, instance, active):
        app = MDApp.get_running_app()
        if active:
            self.disable = False
            self.height = dp(80)
            self.secondary_text = 'Tiojudv'
            self.ids.sec_box.height = '30dp'
            self.ids.sec_box.opacity = 1
            # Animation(height=dp(30), d=.1, opacity=1).start(self.ids.sec_box)
            # self.elevation = 5
            Animation(md_bg_color=app.theme_cls.primary_light[:-1] + [.3], d=.1).start(self)

        else:
            self.md_bg_color = app.theme_cls.primary_light[:-1] + [0]
            self.height = dp(50)
            self.secondary_text = ''
            self.disable = True
            self.ids.sec_box.height = '0dp'
            self.ids.sec_box.opacity = 0
            # self.ids.sec_box.height = '0dp'
            # Animation(height=dp(0), d=.1, opacity=0).start(self.ids.sec_box)
            # self.elevation = 0


if __name__ == '__main__':
    class CardBehavior(MDApp):
        def on_start(self):
            self.bg_color_dark = get_color_from_hex('262626')
            # self.theme_cls.theme_style='Dark'
            self.fps_monitor_start()

        def build(self):
            return Builder.load_string("""
MDScreen:
    md_bg_color:[.8,.8,.8,1]
    # RecycleView:
    MDBoxLayout:
        pos_hint:{'top':0.8}
        adaptive_height: True
        # size_hint_y:.7
        # height:'100dp'
        orientation:'vertical'
        # OneLineListItem:
        #     text:'Hi'
        List:
        List:
        List:
        List:
        # OneLineListItem:
        #     text:'Hi'
        # OneLineListItem:
        #     text:'Hi'
        # OneLineListItem:
        #     text:'Hi'
        # OneLineListItem:
        #     text:'Hi'
        List:
        # OneLineListItem:
        #     text:'Hi'
        
            
            """)


    CardBehavior().run()
