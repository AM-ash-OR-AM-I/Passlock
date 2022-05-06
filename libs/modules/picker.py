from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import OptionProperty, get_color_from_hex
from kivymd.app import MDApp
from libs.modules.dialogs import AKAlertDialog
from kivymd.color_definitions import colors
from kivymd.uix.button import MDIconButton

MY_PALETTE = ["DeepOrange", "Blue", "Purple"]

KV = """
#: import colors kivymd.color_definitions.colors
<ColorSelector>
    canvas:
        Color:
            rgba: root.rgb_hex(root.color_name)
        Ellipse:
            size: self.size
            pos: self.pos
    theme_text_color:'Custom'
    text_color: [0,0,0,0]
            
<PrimaryColorSelector@ColorSelector>
    on_release: 
        app.primary_palette = root.color_name
    
<ColorGrid@MDGridLayout>
    cols: 5
    rows: 4
    adaptive_size: True
    spacing: "8dp"
    padding: (dp(20),20,dp(20),20)
    pos_hint: {"center_x": .5, "top": 1}

"""
Builder.load_string(KV)


class ColorSelector(MDIconButton):
    color_name = OptionProperty("Indigo", options=MY_PALETTE)

    def rgb_hex(self, col):
        return get_color_from_hex(colors[col][self.theme_cls.primary_hue])


class MDThemePicker(AKAlertDialog):
    header_icon = "palette"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.bind(theme_style=self.update_selector)
        self.content_cls = Factory.ColorGrid()
        self.header_font_size = "40dp"
        self.header_height_portrait = "90dp"
        self.update_bg_color()
        MDApp.get_running_app().bind(primary_palette=self.update_bg_color)
        self.size_portrait = ["320dp", "180dp"]
    
    def update_bg_color(self, *args):
        self.bg_color = MDApp.get_running_app().primary_accent

    def update_selector(self, *args):
        self.content_cls.clear_widgets()

    def on_open(self):
        if not self.content_cls.children:
            for name_palette in MY_PALETTE:
                self.content_cls.add_widget(
                    Factory.PrimaryColorSelector(color_name=name_palette)
                )
