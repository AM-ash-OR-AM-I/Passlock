from kivy import platform
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import (
    ColorProperty,
    StringProperty,
    BooleanProperty,
    NumericProperty,
    ListProperty,
)
from kivy.utils import get_color_from_hex
from kivy.uix.textinput import TextInput

from kivymd.app import MDApp
from kivymd.color_definitions import colors
from kivymd.material_resources import dp
from kivymd.theming import ThemableBehavior
from kivymd.uix.button import MDIconButton
from kivymd.uix.relativelayout import MDRelativeLayout

if platform == "android":
    from libs.modules.AndroidAPI import fix_back_button, keyboard_height

Builder.load_string("""
<CardTextField>
    height: '60dp'
    size_hint_y:None
    size_hint_x:.8
    radius: dp(30)
    set_elevation: 0
    label_name:'Hi there'
    md_bg_color: [1,1,1,1] if app.theme_cls.theme_style=='Light' else get_color_from_hex(self.dark_bg_hex)
    label_size:'15sp'
    hint_text:''
    password: False
    password_mask: "●"
    adaptive_height:True
    spacing:'20dp'
    orientation:'vertical'
    start_anim: app.dark_mode and app.entered_app
    
    MDLabel:
        text:root.label_name
        markup:True
        adaptive_height:True
        y:card.y+card.height+dp(10)
        x:card.x+dp(30)
		theme_text_color:"Custom"
		text_color:app.text_color
        size_hint_x:0.8
        font_size:root.label_size
        font_name:'RobotoMedium'
    MDCard:
        id: card
        height: root.height
        size_hint_y: None
        radius: root.radius
        elevation: root.set_elevation
        md_bg_color:root.md_bg_color
        canvas:
            Color:
                rgba: root.border_color
            Line:
                width:root.thickness
                rounded_rectangle:
                    (self.x,self.y,self.width,self.height,self.radius[0])
    MDBoxLayout:
        id: card_box
        padding:(dp(20),0,0,0)if root.icon_left_action is None else (0,0,0,0)
        spacing:'5dp'
        MDBoxLayout:
            id: left_actions
            adaptive_size: True
        TextInput:
            id: textfield
            size_hint_y:None
            hint_text:root.hint_text
            height: card.height
            background_color:[0,0,0,0]
            font_name:"BigCircleFont" 
            password: root.password
            password_mask: root.password_mask
            font_size:root.text_font_size 
            padding:[0,(self.height-self.font_size)/2,0,dp(0)] if not root.icon_left_action\
             else [0,(self.height-self.font_size)/2,0,dp(6)]
            foreground_color: app.theme_cls.primary_color if not app.dark_mode else app.theme_cls.primary_light
            hint_text_color: root.hint_text_color if root.hint_text_color is not None else [.5,.5,.5,.8]
            cursor_color: app.theme_cls.primary_color
            multiline: root.multiline
            text: root.text
            on_text:
                root.text = self.text
            on_focus:
                root.focus = self.focus
            y: card.y
            center_x: card.center_x
        MDBoxLayout:
            id: right_actions
            adaptive_size: True
"""
)


class CardTextField(MDRelativeLayout, ThemableBehavior):
    inactive_color = ColorProperty([0.5, 0.5, 0.5, 0.1])
    border_color = ColorProperty([0.5, 0.5, 0.5, 0.1])
    active_color = [0, 0.7, 1, 0.7]
    focus = BooleanProperty(False)
    text_font_size = StringProperty("17sp")
    hint_text_color = ColorProperty(None)
    text = StringProperty("")
    thickness = NumericProperty(dp(1) if platform == "android" else dp(1.4))
    hint_text = StringProperty("")
    label_size = StringProperty("20dp")
    label_name = StringProperty("")
    icon_left_action = ListProperty(None)
    multiline = BooleanProperty(False)
    icon_color = ColorProperty([0.5, 0.5, 0.5, 1])
    icon_right_action = ListProperty(None)
    dark_bg_hex = "262626"
    icon_font_size = NumericProperty()
    win = True if platform == "win" else False
    start_anim = BooleanProperty(False)

    app = None
    c = 0

    def on_start_anim(self, instance, dark_mode):
        self.anim = Animation(
            md_bg_color=get_color_from_hex(
                colors["Dark" if dark_mode else "Light"]["CardsDialogs"]
            )
            if not self.dark_bg_hex
            else get_color_from_hex(self.dark_bg_hex if dark_mode else "ffffff"),
            d=0.2,
        )

        self.anim.start(instance)

    def on_icon_left_action(self, instance, icon_list):
        self.ids.left_actions.clear_widgets()
        if len(icon_list) and type(icon_list[0]) != list:
            self.icon_left = MDIconButton(
                    icon=self.icon_left_action[0],
                    theme_text_color="Custom",
                    text_color=self.icon_color,
                    user_font_size=self.icon_font_size,
                    pos_hint={"center_y": 0.5},
                )
            if len(icon_list) != 1:
                self.icon_left.on_release = self.icon_left_action[1]
            self.ids.left_actions.add_widget(self.icon_left, index=1)
        elif type(icon_list[0]) == list:
            for icons in icon_list:
                self.icon_left = MDIconButton(
                        icon=icons[0],
                        theme_text_color="Custom",
                        text_color=self.icon_color,
                        user_font_size=self.icon_font_size,
                        pos_hint={"center_y": 0.5},
                    )
                if len(icons) != 1:
                    self.icon_left.on_release=icons[1]
                    
                self.ids.left_actions.add_widget(self.icon_left, index=1)

    def on_icon_right_action(self, instance, icon_list):
        self.ids.right_actions.clear_widgets()
        if len(icon_list) and type(icon_list[0]) != list:
            self.icon_right = MDIconButton(
                    icon=self.icon_right_action[0],
                    theme_text_color="Custom",
                    text_color=self.icon_color,
                    user_font_size=self.icon_font_size,
                    pos_hint={"center_y": 0.5},
                )
            if len(icon_list) != 1:
                self.icon_right.on_release=self.icon_right_action[1]
            self.ids.right_actions.add_widget(self.icon_right)
        elif type(icon_list[0]) == list:
            for icons in icon_list:
                self.icon_right = MDIconButton(
                        icon=icons[0],
                        theme_text_color="Custom",
                        text_color=self.icon_color,
                        user_font_size=self.icon_font_size,
                        pos_hint={"center_y": 0.5},
                    )
                if len(icons) != 1:
                    self.icon_right.on_release=icons[1]
                self.ids.right_actions.add_widget(self.icon_right)

    def on_icon_color(self, instance, color):
        if self.icon_left_action is not None:
            self.icon_left.text_color = color
        if self.icon_right_action is not None:
            self.icon_right.text_color = color

    def on_inactive_color(self, *args):
        self.border_color = self.inactive_color

    def on_text(self, instance, text):
        """Use this to do what you want"""

    def on_focus(self, instance, focus):
        if self.app is None:
            self.app = MDApp.get_running_app()
        if platform == "android":
            if not focus:
                fix_back_button()

            def call(*args):
                if focus:
                    if (height := keyboard_height()) > 0:
                        self.app.key_height = height
                else:
                    self.app.key_height = 0

            Clock.schedule_once(call, 0.2)

        if focus:
            self.border_color = self.active_color
        else:
            self.border_color = self.inactive_color


if __name__ == "__main__":

    class TestCard(MDApp):
        def build(self):
            Window.size = (500, 900)
            return Builder.load_string(
                """
				"""
            )

    TestCard().run()
