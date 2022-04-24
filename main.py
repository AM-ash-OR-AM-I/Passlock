from os import system
from kivy.clock import mainthread
import threading
from time import time

initial = time()
from colorsys import rgb_to_hls, hls_to_rgb
import os.path
from libs.screens.classes import Dialog
from libs.screens.root import Root
from libs.utils import is_dark_mode, set_dark_mode

from kivy.config import Config
from kivy import platform
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    get_color_from_hex,
    NumericProperty,
)

from kivymd.app import MDApp
from kivymd.material_resources import dp
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatButton

Config.set("kivy", "log_level", "info")
Config.write()


def emulate_android_device(
    pixels_horizontal=1080, pixels_vertical=2240, android_dpi=394, monitor_dpi=157
):
    scale_factor = monitor_dpi / android_dpi
    Window.size = (scale_factor * pixels_horizontal, scale_factor * pixels_vertical)


if platform != "android":
    emulate_android_device()
else:
    from libs.modules.AndroidAPI import statusbar, android_dark_mode

KV = """
#: import HotReloadViewer kivymd.utils.hot_reload_viewer.HotReloadViewer
#: import Window kivy.core.window.Window
HotReloadViewer:
    path: app.path_to_live_ui
    errors: True
    errors_text_color: 0.5, 0.5, 0.5, 1
    errors_background_color: app.theme_cls.bg_dark
"""


class MainApp(MDApp):
    dark_mode = BooleanProperty(False)
    key_height = NumericProperty(0)
    text_color = ColorProperty()
    primary_accent = ColorProperty()
    bg_color = ColorProperty()
    system_dark_mode = False
    encryption_class = None
    passwords = {}
    encrypted_keys = {}
    screen_history = []
    LIVE_UI = 1
    fps = True
    path_to_live_ui = "OtherStuff/custom_dialog.kv"
    entered_app = False
    HomeScreen = LoginScreen = SettingScreen = update_dialog = exit_dialog = None

    def __init__(self):
        super().__init__()
        self.theme_cls.primary_palette = "DeepOrange"
        self.text_color = get_color_from_hex("611c05")
        self.signup = False if os.path.exists("data/user_id.txt") else True
        self.secondary_text_color = get_color_from_hex("a8928a")
        self.light_color = self.generate_color()
        self.bg_color_light = self.generate_color(lightness=0.98)
        self.bg_color_dark = self.generate_color(darkness=0.1)
        self.bg_color = self.bg_color_dark if self.dark_mode else self.bg_color_light
        self.dark_color = self.generate_color(darkness=0.18)  # 262626
        self.login_circle_light = self.generate_color(lightness=0.85)
        self.primary_accent = self.dark_color if self.dark_mode else self.light_color
        self.light_hex = self.generate_color(return_hex=True)
        self.dark_hex = self.generate_color(darkness=0.18, return_hex=True)
        threading.Thread(target = self.set_dark_mode, daemon=True).start()
    
    def set_dark_mode(self):
        self.system_dark_mode = is_dark_mode(system=True)
        if platform == "android":
            self.dark_mode = (
                android_dark_mode() if self.system_dark_mode else is_dark_mode()
            )
        else:
            self.dark_mode = is_dark_mode()
        self.entered_app = True
        

    def build(self):
        self.root = Root()
        self.root.load_screen("SignupScreen" if self.signup else "LoginScreen")

    def animate_signup(self, instance):

        """Animation to be shown when user enters the signup screen"""
        print(f"Time taken = {time() - initial}")
        if instance:
            Animation(pos_hint={"top": 0.95}, opacity=1, d=0.5, t="out_back").start(
                instance
            )

    def generate_color(
        self, hex_color=False, color=None, return_hex=False, lightness=0.92, darkness=0
    ):
        """
        :param hex_color:  Instead of passing color as list hexadecimal value can be passed.
        :param color: Takes color like [.5,.5,.5, 1] as Parameter
        :param return_hex: Boolean value if set true the function will return hexadecimal value.
        :param lightness: Value from 0-1. If set to 1 it will return white and 0 will return original color.
        :return:
        """
        if hex_color:
            color = get_color_from_hex(hex_color)
        elif not color:
            color = self.theme_cls.primary_color[:-1]

        h, l, s = rgb_to_hls(*color)
        l = lightness if not darkness else darkness
        s = 0.7 if not darkness else 0.15
        color = list(hls_to_rgb(h, l, s))

        if not return_hex:
            return color + [1]
        else:
            r, g, b = color
            _hex = (
                hex(round(r * 255))[2:]
                + hex(round(g * 255))[2:]
                + hex(round(b * 255))[2:]
            )
            return _hex

    def back_button(self, home_screen=False, *args):
        if not home_screen:
            self.screen_history.pop()
        else:
            self.screen_history = ["HomeScreen"]
        self.root.transition.mode = "pop"
        self.root.transition.direction = "right"
        self.root.current = self.screen_history[-1]

    def open_exit_dialog(self):
        if not self.exit_dialog:
            self.exit_dialog = Dialog(
                title="Exit",
                text="Do you want to exit?",
                buttons=[
                    MDFillRoundFlatButton(
                        text="YES", on_release=lambda x: self.stop(), _radius=dp(20)
                    ),
                    MDFlatButton(
                        text="NO",
                        _radius=dp(20),
                        on_release=lambda x: self.exit_dialog.dismiss(),
                    ),
                ],
            )
        self.exit_dialog.open()

    def on_dark_mode(self, instance, mode):
        if self.entered_app:
            current_screen = self.root.current
            if current_screen == "HomeScreen":
                tab_manager = self.root.current_screen.ids.tab_manager
                primary_color = Animation(
                    primary_accent=self.dark_color
                    if self.dark_mode
                    else self.light_color,
                    duration=0.2,
                )
                primary_color.start(self)
                if tab_manager.current == "CreateScreen":
                    self.anim = Animation(
                        md_bg_color=self.bg_color_dark if mode else self.bg_color_light,
                        duration=0.2,
                    )
                    self.anim.start(self.root.HomeScreen)

                primary_color.on_complete = self.set_theme_style
        else:
            self.set_theme_style()

    def set_theme_style(self, *args):
        print("theme_style set")
        self.text_color = (
            get_color_from_hex("611c05")
            if not self.dark_mode
            else get_color_from_hex("fde9e2")
        )
        self.bg_color = self.bg_color_dark if self.dark_mode else self.bg_color_light
        self.primary_accent = self.dark_color if self.dark_mode else self.light_color
        if self.entered_app:
            self.root.HomeScreen.ids.create.ids.dark_animation.rad = 0.1
        else:
            self.entered_app = True

        if self.dark_mode:
            self.theme_cls.theme_style = "Dark"
            self.theme_cls.primary_hue = "300"
            if platform == "android":
                statusbar(status_color=self.dark_hex, white_text=False)
        else:
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_hue = "500"
            if platform == "android":
                statusbar(status_color=self.light_hex, white_text=True)

    def toggle_mode(self, *args):
        self.dark_mode = not self.dark_mode

    def on_key_height(self, instance, val):

        """Used to move screen up/down so that UI elements are visible when keyboard is shown."""

        print(val)
        signup = self.root.SignupScreen
        if self.root.current == "LoginScreen":
            self.diff = (val - signup.ids.lock.y + dp(20)) / Window.height
            if self.diff > 0:
                if val > 0:
                    self.box_height = signup.ids.box.pos_hint["top"]
                    Animation(
                        pos_hint={"top": self.box_height + self.diff},
                        t="out_quad",
                        d=0.2,
                    ).start(signup.ids.box)
                else:
                    Animation(
                        pos_hint={"top": self.box_height}, t="in_quad", d=0.2
                    ).start(signup.ids.box)
        else:
            if self.root.HomeScreen.ids.tab_manager.current == "CreateScreen":
                generate = self.root.HomeScreen.ids.create.ids.manual.ids.add
                self.root.HomeScreen.ids.create.ids.auto.scroll_y = 1
                self.diff = val - generate.y + dp(20)
                if self.diff > 0:
                    if val > 0:
                        Animation(y=self.diff, t="out_quad", d=0.2).start(
                            self.root.HomeScreen
                        )
                    else:
                        Animation(y=0, t="in_quad", d=0.2).start(self.root.HomeScreen)
            else:
                Window.softinput_mode = "below_target"

    def on_start(self):
        """Sets status bar color in android."""
        if platform == "android":
            statusbar(
                status_color=self.dark_hex if self.dark_mode else self.light_hex,
                white_text=not self.dark_mode,
            )

    def on_pause(self):
        set_dark_mode(app=self.dark_mode, system=self.system_dark_mode)
        return True

    def on_stop(self):
        set_dark_mode(app=self.dark_mode, system=self.system_dark_mode)


if __name__ == "__main__":
    MainApp().run()
