from kivy import platform, Logger
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ColorProperty, StringProperty, BooleanProperty, NumericProperty, ListProperty
from kivymd.app import MDApp
from kivymd.material_resources import dp
from kivymd.theming import ThemableBehavior
from kivymd.uix.button import MDIconButton, MDFillRoundFlatButton
from kivymd.uix.relativelayout import MDRelativeLayout
Window.size=(400,800)
KV = '''
#:import HotReloadViewer kivymd.utils.hot_reload_viewer.HotReloadViewer
#: import Window kivy.core.window.Window
HotReloadViewer:
    path: app.path_to_kv_file
    errors: True
    errors_text_color: 0, 0, 0, 1
    errors_background_color: app.theme_cls.bg_dark
'''


class RoundButton(MDFillRoundFlatButton):
    padding = [0, dp(20), 0, dp(20)]
    _radius = dp(20),dp(20)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.bind(primary_hue=self.update_md_bg_color)


class Example(MDApp):
    path_to_kv_file = "BottomNavigation.kv"
    dark_mode = BooleanProperty(False)

    def build(self):
        # self.dark_mode = True
        self.theme_cls.primary_palette = 'DeepOrange'
        Builder.load_file("LoginScreenDesign.kv")
        return Builder.load_string(KV)

    def on_dark_mode(self, instance,mode):
        print(mode)
        if mode:
            self.theme_cls.theme_style = 'Dark'
            self.theme_cls.primary_hue = '300'
            # statusbar(status_color='ff8d69')
        else:
            self.theme_cls.theme_style = 'Light'
            self.theme_cls.primary_hue = '500'
            # statusbar(status_color='ff7a4f')

    def toggle_mode(self, *args):
        self.dark_mode = not self.dark_mode

    def update_kv_file(self, text):
        with open(self.path_to_kv_file, "w") as kv_file:
            kv_file.write(text)


Example().run()
