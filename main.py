from kivy.lang import Builder
from kivy.properties import BooleanProperty, ColorProperty, NumericProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager
from kivymd.theming import ThemableBehavior

from kivymd.uix.boxlayout import MDBoxLayout

from kivymd.uix.behaviors.ripplebehavior import CircularRippleBehavior
from kivymd.uix.label import MDIcon

from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.animation import Animation
from kivy import platform

from kivymd.color_definitions import colors
from kivymd.material_resources import dp
from kivymd.uix.button import MDFloatingActionButton, MDFillRoundFlatButton
from kivymd.uix.screen import MDScreen

if platform != 'android':
    Window.size = (450, 800)
else:
    from JavaAPI import statusbar

# print(platform)
KV = '''
#:import HotReloadViewer kivymd.utils.hot_reload_viewer.HotReloadViewer
#: import Window kivy.core.window.Window
HotReloadViewer:
    path: app.path_to_live_ui
    errors: True
    errors_text_color: 0.5, 0.5, 0.5, 1
    errors_background_color: app.theme_cls.bg_dark
'''


class RoundButton(MDFillRoundFlatButton):
    padding = [0, dp(20), 0, dp(20)]
    _radius = dp(20), dp(20)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.bind(primary_hue=self.update_md_bg_color)


class TestCard(MDApp):
    dark_mode = BooleanProperty(False)
    screen_history = []
    LIVE_UI = 0
    path_to_live_ui = 'BottomNavigation.kv'

    def build(self):
        if not self.LIVE_UI:
            Builder.load_file('LoginScreenDesign.kv')
            Builder.load_file('BottomNavigation.kv')
            Builder.load_file('HomeScreenDesign.kv')
        self.theme_cls.primary_palette = 'DeepOrange'
        self.dark_mode = True
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name='Login'))
        self.sm.add_widget(HomeScreen(name='Home'))
        return Builder.load_string(KV) if self.LIVE_UI else self.sm

    def back_button(self, home_screen=False, *args):
        if not home_screen:
            self.screen_history.pop()
        else:
            self.screen_history = ['HomeScreen']
        self.sm.transition.mode = 'pop'
        self.sm.transition.direction = 'right'
        self.sm.current = self.screen_history[-1]

    def change_screen(self, screen_name, *args):
        self.sm.transition.mode = 'push'
        self.sm.transition.direction = 'left'
        self.sm.current = screen_name
        self.screen_history.append(screen_name)
        print(f'{self.screen_history = }')

    def on_dark_mode(self, instance, mode):
        print(mode)
        if mode:
            self.theme_cls.theme_style = 'Dark'
            self.theme_cls.primary_hue = '300'
            if platform == 'android':
                statusbar(status_color=colors["Dark"]["CardsDialogs"])
        else:
            self.theme_cls.theme_style = 'Light'
            self.theme_cls.primary_hue = '500'
            if platform == 'android':
                statusbar(status_color='ff7a4f')

    def toggle_mode(self, *args):
        self.dark_mode = not self.dark_mode
        return self.dark_mode

    def on_start(self):
        if platform == 'android':
            statusbar(status_color=colors["Dark"]["CardsDialogs"] if self.dark_mode else 'ff7a4f')

    # def on_stop(self):
    #     self.root.ids.box.export_to_png("gradient.png")


# class IconButton(MDIcon, ButtonBehavior, CircularRippleBehavior): pass


class RoundButton(MDFillRoundFlatButton):
    padding = [0, dp(20), 0, dp(20)]
    _radius = '20dp'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.bind(primary_hue=self.update_md_bg_color)


class LoginScreen(MDScreen): pass


class HomeScreen(MDScreen): pass


class LabelIcon(MDBoxLayout, ThemableBehavior):
    active = BooleanProperty(False)
    text_color = ColorProperty([1, 1, 1, 1])
    scale= NumericProperty(1)
    opac = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text_color = self.theme_cls.primary_color if self.active else [1, 1, 1, .7]

    def on_active(self, instance, active):
        app = MDApp.get_running_app()
        print(app.root.children)
        for instances in app.root.children[0].ids.bottom_nav.ids.box.children:
            print(instances, instance)
            if instances != instance:
                instances.text_color = [.5, .5, .5, 1]
                self.animate = Animation(scale=1, d=.15)
                instances.scale = 1
                instances.opac=0
            else:
                instances.text_color=self.theme_cls.primary_color
                instances.opac = 1
                self.animate=Animation(scale=1.4, d=.15)
                self.animate.start(instances)


TestCard().run()
