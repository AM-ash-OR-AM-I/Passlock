from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.modalview import ModalView
from kivy.animation import Animation
from kivy.clock import Clock

from kivymd.uix.snackbar import Snackbar
from kivymd.app import MDApp
from kivymd.material_resources import dp
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import (
    MDFillRoundFlatButton,
    MDFillRoundFlatIconButton,
    MDFlatButton,
)
from kivymd.uix.dialog import MDDialog


# ---- FloatingButton ----
Builder.load_string("""
<FloatingButton@MDFloatingActionButton+FakeCircularElevationBehavior>
    user_font_size:80
    pos_hint:{'center_x':.5}
    md_bg_color:app.primary_accent
    # theme_text_color:'Custom'
    text_color:self.theme_cls.primary_color
	_no_ripple_effect: True
    """
)


# ---- BorderCard and PasswordCard (Child Classes of CardTextField) ----
Builder.load_string("""              
#: import CardTextField libs.modules.CardTextField.CardTextField
<BorderCard@CardTextField>
	inactive_color:app.theme_cls.primary_light[:-1]+[.4]
	thickness:dp(1) if platform == 'android' else dp(1.4)
	icon_color:app.theme_cls.primary_light

<PasswordCard@BorderCard>
    password: True
    icon_right_action:['eye-off-outline' if self.password else "eye-outline", lambda : exec("self.password = not self.password")]
"""
)


# ---- Sync Widget ----
KV = """
<SyncWidget>
    padding:"14dp"
    pos_hint:{"center_x":.8,"center_y":.1}
    md_bg_color:app.primary_accent
    orientation:"vertical"
    size_hint_y:None
    height: dp(100)
    size_hint_x:None
    width: self.height + dp(10)
    radius:"25dp"
    MDIcon:
        id: sync_icon
        icon: 'cloud-download' if not root.icon else root.icon
        halign:"center"
        theme_text_color:"Custom"
        text_color:app.text_color
        font_size: dp(30)
    MDLabel: 
        id: sync_text
        theme_text_color:"Custom"
        text_color:app.text_color
        font_size: sp(15)
        halign:"center"
        text:"Restoring.." if not root.text else root.text
    """


class SyncWidget(MDBoxLayout):
    Builder.load_string(KV)
    start_anim = None
    stop_anim = None
    text = StringProperty()
    icon = StringProperty()

    def start(self):
        self.opacity = 1
        self.interval = Clock.schedule_interval(self._start_animation, 1.2)

    def stop(self):
        self._stop_animation()
        self.interval.cancel()

    def _stop_animation(self):
        if self.stop_anim is None:
            self.stop_anim = Animation(opacity=0, d=0.3, t="in_quad")
        self.stop_anim.start(self)

    def _start_animation(self, *args):
        if self.start_anim is None:
            self.start_anim = Animation(opacity=0, d=0.5, t="in_quad")
            self.start_anim += Animation(opacity=1, d=0.5, t="out_quad")
        self.start_anim.start(self.ids.sync_icon)


class LoadingScreen(ModalView):
    is_open = False
    Builder.load_string(
        """
<LoadingScreen>:
    auto_dismiss: False
    background_color: 0, 0, 0, 0
    overlay_color: 0, 0, 0, 0.2
    text: "Checking..." 
    FloatLayout:
        MDLabel:
            font_size:"40dp"
            font_name:"Poppins"
            theme_text_color:"Custom"
            pos_hint:{"center_y":.5}
            text_color: app.text_color
            halign:"center"
            text:root.text   
    """
    )

    def on_open(self):
        self.is_open = True
        super().on_open()

    def on_dismiss(self):
        self.is_open = False
        super().on_dismiss()


class RoundButton(MDFillRoundFlatButton):
    Builder.load_string(
        """
<RoundButton>
    md_bg_color:app.primary_accent
    theme_text_color:'Custom'
    text_color:app.theme_cls.primary_color
"""
    )
    _radius = dp(28), dp(28)
    padding = [0, dp(15), 0, dp(15)]


class RoundIconButton(MDFillRoundFlatIconButton):
    _radius = dp(20)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.bind(primary_hue=self.update_md_bg_color)


# ---- The below string loads the update dialog box content ----
Builder.load_string(
    """
<UpdateContent@MDBoxLayout>
    adaptive_height: True
    padding: 0, dp(15), 0, 0
    orientation: "vertical"
    spacing: "5dp"
    MDTextField:
        id: name
        hint_text: "Name"
    MDTextField:
        id: password
        hint_text: "Password"
"""
)


class Dialog(MDDialog):
    radius = [dp(30)] * 4
    _anim_duration = 0.25
    overlay_color = [0, 0, 0, 0.3]

    def update_bg_color(self, *args):
        self.md_bg_color = self.app.primary_accent

    def _opening_animation(self):
        self.opacity = 0
        anim = Animation(opacity=1, duration=self._anim_duration, t="out_quad")
        anim.start(self)

    def _dismiss_animation(self):
        anim = Animation(opacity=0, duration=self._anim_duration - 0.05, t="out_quad")
        anim.start(self)

    def on_pre_open(self):
        self._opening_animation()
        return super().on_pre_open()

    def on_dismiss(self):
        self._dismiss_animation()
        # return super().on_dismiss()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.size_hint_x = 0.85
        self.md_bg_color = self.app.primary_accent
        self.theme_cls.bind(theme_style=self.update_bg_color)
        self.app.bind(primary_accent=self.update_bg_color)


class DialogButton(MDFlatButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_text_color = "Custom"
        self.font_size = "16sp"


class CheckboxLabel(ThemableBehavior, RectangularRippleBehavior, MDBoxLayout):
    Builder.load_string(
        """
<ButtonLabel@ButtonBehavior+MDLabel>
<CheckboxLabel>
	adaptive_size:True
	size_hint_x:.85
	pos_hint: {'center_x': .5}
	spacing:'12dp'
	on_active: None
    active: True
	radius:dp(5),dp(5)
	text:''
	MDCheckbox:
		id: check
		size_hint: None, None
		size: "36dp", "36dp"
        active: root.active
		unselected_color: [.8,.8,.8,1]
        on_active: 
            root.active = check.active
		pos_hint: {'center_x': .5}
	ButtonLabel:
        theme_text_color:"Custom"
        text_color:app.text_color
		on_release:
			check.active = not check.active
		text: root.text
"""
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ripple_alpha = 0.15


class CustomSnackbar(Snackbar):
    is_open = False

    def on_open(self, *args):
        self.is_open = True

    def on_leave(self):
        self.is_open = False
