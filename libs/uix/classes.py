from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.material_resources import dp
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton, MDFillRoundFlatIconButton, MDFlatButton
from kivymd.uix.dialog import MDDialog


class RoundButton(MDFillRoundFlatButton):
    Builder.load_string("""
# kv_start
<RoundButton>
	canvas:
		RoundedRectangle:
			size: self.size
			pos: self.pos
			radius:dp(20),dp(20)
			texture: Gradient.horizontal([1,1,1,0], [1,1,1,.2])
			
# kv_end
""")
    padding = [0, dp(20), 0, dp(20)]
    _radius = dp(20), dp(20)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.bind(primary_hue=self.update_md_bg_color)


class RoundIconButton(MDFillRoundFlatIconButton):
    _radius = dp(20)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.bind(primary_hue=self.update_md_bg_color)


# ------- The below string loads the update dialog box content --------
Builder.load_string("""
<UpdateContent@MDBoxLayout>
    adaptive_height: True
    padding: 0, dp(40), 0, 0
    orientation: "vertical"
    spacing: "5dp"
    MDTextField:
        hint_text: "Name"
    MDTextField:
        hint_text: "Password"
""")


class Dialog(MDDialog):
    radius = [dp(30)] * 4

    def update_bg_color(self, *args):
        self.md_bg_color = MDApp.get_running_app().primary_accent

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = MDApp.get_running_app().primary_accent
        self.theme_cls.bind(theme_style=self.update_bg_color)


class DialogButton(MDFlatButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_text_color = "Custom"
        self.font_name = "RobotoMedium"
        self.font_size = "16sp"
        self.text_color = self.theme_cls.primary_color



checkbox = """
# kv_start
<CheckboxLabel>
	adaptive_size:True
	size_hint_x:.8
	pos_hint: {'center_x': .5}
	spacing:'12dp'
	active: False
	radius:dp(5),dp(5)
	text:''
	MDCheckbox:
		id: check
		size_hint: None, None
		size: "36dp", "36dp"
		selected_color:app.theme_cls.primary_light
		unselected_color: [.8,.8,.8,1]
		pos_hint: {'center_x': .5}
	ButtonLabel:
		on_release:
			check.active = not check.active
		text: root.text
# kv_end
"""


class CheckboxLabel(ThemableBehavior, RectangularRippleBehavior, MDBoxLayout):
    Builder.load_string(checkbox)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ripple_color = self.theme_cls.primary_light
        self.ripple_alpha = .2
