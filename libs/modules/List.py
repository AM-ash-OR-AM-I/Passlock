from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty, ColorProperty, DictProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior

from kivymd.app import MDApp
from kivymd.material_resources import dp
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivymd.uix.boxlayout import MDBoxLayout

app = MDApp.get_running_app()

KV = """
<List>
	orientation:'vertical'
	size_hint_y:None
	padding: dp(28),dp(0),dp(10),dp(15)
	size_hint_x:1
	spacing:'6dp'
	height:'90dp' if self.selected else "56dp"
	elevation:0
	radius:'28dp'
	disable: True
	md_bg_color:self.list_color_active if self.selected else app.theme_cls.primary_light[:-1] + [0]
	MDLabel:
		adaptive_height: True
		text:root.name
		theme_text_color:"Custom"
		text_color: app.text_color
	MDBoxLayout:
		id: sec_box
		size_hint_y:None
		height:root.selected*dp(30) 
		opacity: root.selected*1
		MDLabel:
			adaptive_height:True
			text:root.password
			theme_text_color:"Secondary"
		MDIconButton:
			id: copy_button
			disabled: not root.selected
			md_bg_color_disabled:[0,0,0,0]
			theme_text_color:"Custom"
			text_color: app.text_color
			icon:'content-copy'
			pos_hint:{'center_y':.5}
		MDIconButton:
			id: update_button
			disabled: not root.selected
			md_bg_color_disabled:[0,0,0,0]
			icon:'pencil-outline'
			theme_text_color:"Custom"
			text_color: app.text_color
			pos_hint:{'center_y':.5} 
			# text_color:[.3,.3,.3,1]
		MDIconButton:
			id: delete_button
			disabled: not root.selected
			md_bg_color_disabled:[0,0,0,0]
			icon:'trash-can-outline'
			theme_text_color:"Custom"
			text_color: app.text_color
			pos_hint:{'center_y':.5}

"""


class List(
    RectangularRippleBehavior,
    RecycleDataViewBehavior,
    ThemableBehavior,
    ButtonBehavior,
    MDBoxLayout,
):
    Builder.load_string(KV)

    name = StringProperty("Google")
    password = StringProperty("12345678910111213")
    selected = BooleanProperty()
    list_color_active = ColorProperty()
    button_actions = DictProperty()

    _no_ripple_effect = True
    ripple_alpha = 0.1

    def on_button_actions(self, *args):
        if len(self.button_actions) == 3:
            self.ids.copy_button.on_release = self.button_actions["copy"]
            self.ids.update_button.on_release = self.button_actions["update"]
            self.ids.delete_button.on_release = self.button_actions["delete"]

    def on_release(self):
        if self.selected:
            if self.right - self.last_touch.x >= dp(170):
                self.parent.clear_selection()
        else:
            recycle_list = self.parent.children
            snack = app.root.HomeScreen.ids.find.snackbar

            if not (snack and snack.is_open) or self not in recycle_list[:2] or len(recycle_list) <=13:
                self.parent.select_with_touch(self.index, None)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super().refresh_view_attrs(rv, index, data)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        rv.data[index]["selected"] = is_selected

    def on_selected(self, instance, selected):
        if selected:
            self.list_color_active = self.theme_cls.primary_light[:-1] + [0]
            Animation(
                list_color_active=self.theme_cls.primary_light[:-1] + [0.3], d=0.1
            ).start(self)
