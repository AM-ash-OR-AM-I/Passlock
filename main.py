from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.uix.screenmanager import ScreenManager

from kivymd.app import MDApp
from kivy.core.window import Window
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
class RoundButton(MDFillRoundFlatButton):
    padding = [0, dp(20), 0, dp(20)]
    _radius = dp(20),dp(20)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.bind(primary_hue=self.update_md_bg_color)


class TestCard(MDApp):
    dark_mode = BooleanProperty(False)
    screen_history=[]

    def build(self):
        Builder.load_file('BottomNavigation.kv')
        Builder.load_file('LoginScreenDesign.kv')
        Builder.load_file('HomeScreenDesign.kv')
        self.theme_cls.primary_palette = 'DeepOrange'
        self.dark_mode = True
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name='Login'))
        self.sm.add_widget(HomeScreen(name='Home'))
        return self.sm

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
            statusbar(status_color=colors["Dark"]["CardsDialogs"]if self.dark_mode else 'ff7a4f')

    # def on_stop(self):
    #     self.root.ids.box.export_to_png("gradient.png")


class RoundButton(MDFillRoundFlatButton):
    padding = [0, dp(20), 0, dp(20)]
    _radius = '20dp'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.bind(primary_hue=self.update_md_bg_color)


class LoginScreen(MDScreen):pass


class HomeScreen(MDScreen):pass



TestCard().run()
'SNX^@_PZ1xG]'
