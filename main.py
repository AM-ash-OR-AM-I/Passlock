from kivy import platform
from kivy.animation import Animation
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ColorProperty, get_color_from_hex, ListProperty, NumericProperty

from kivymd.app import MDApp
from kivymd.color_definitions import colors
from kivymd.icon_definitions import md_icons
from kivymd.material_resources import dp
from kivymd.theming import ThemableBehavior
from kivymd.toast import toast
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from libs.uix.root import Root

# Window.keyboard_anim_args = {"d": 0.2, "t": "linear"}
# Window.softinput_mode = "below_target"

if platform != 'android':
	Window.size = (450, 900)
else:
	from libs.JavaAPI import statusbar

KV = '''
#: import HotReloadViewer kivymd.utils.hot_reload_viewer.HotReloadViewer
#: import Window kivy.core.window.Window
HotReloadViewer:
	path: app.path_to_live_ui
	errors: True
	errors_text_color: 0.5, 0.5, 0.5, 1
	errors_background_color: app.theme_cls.bg_dark
'''


class MainApp(MDApp):
	dark_mode = BooleanProperty(False)
	screen_history = []
	key_height = NumericProperty(0)
	LIVE_UI = 1
	fps = True
	path_to_live_ui = 'custom_dialog.kv'
	primary_accent = ColorProperty()
	signup = BooleanProperty(True)
	rv_data = ListProperty()
	HomeScreen = LoginScreen = SettingScreen = update_dialog = exit_dialog = None

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.theme_cls.primary_palette = 'DeepOrange'
		self.light_color = self.generate_light_color()
		self.bg_color_dark = self.generate_dark_color()  # 262626
		self.bg_color_dark2 = self.generate_dark_color(darkness=.26)
		self.light_color1 = self.generate_light_color(lightness=80)
		self.light_color2 = self.generate_light_color(lightness=70)
		self.primary_accent = self.bg_color_dark if self.dark_mode else self.light_color
		self.card_color = self.bg_color_dark if self.dark_mode else [1, 1, 1, 1]
		self.light_hex = self.generate_light_color(return_hex=True)
		self.dark_hex = self.generate_dark_color(return_hex=True)

	def build(self):
		self.root = Root()
		self.root.set_current("LoginScreen")
		self.set_list()
		Builder.load_file("libs/classes.kv")

	def open_update_dialog(self):
		if not self.update_dialog:
			update_content = Factory.UpdateContent()
			self.update_dialog = Dialog(
				title="Update", type="custom", content_cls=update_content,
				size_hint_x=.8,
				buttons=[
					DialogButton(text="Cancel", on_release=lambda x: self.update_dialog.dismiss()),
					DialogButton(text=f"Update [font=Icons]{md_icons['update']}[/font]")
				]
			)
		self.update_dialog.open()

	def on_key_height(self, instance, val):
		print(val)
		if self.root.current == 'LoginScreen':
			if not self.LoginScreen:
				self.LoginScreen = self.root.get_screen("LoginScreen")
			self.diff = (val - self.LoginScreen.ids.lock.y + dp(20)) / Window.height
			if self.diff > 0:
				if val > 0:
					self.box_height = self.LoginScreen.ids.box.pos_hint["top"]
					Animation(pos_hint={"top": self.box_height + self.diff}, t="out_quad", d=.2).start(
						self.LoginScreen.ids.box)
				else:
					Animation(pos_hint={"top": self.box_height}, t="in_quad", d=.2).start(self.LoginScreen.ids.box)
		else:
			if not self.HomeScreen:
				self.HomeScreen = self.root.get_screen("HomeScreen")
			if self.HomeScreen.ids.tab_manager.current == "CreateScreen":
				generate = self.HomeScreen.ids.create.ids.manual.ids.add
				self.HomeScreen.ids.create.ids.auto.scroll_y = 1
				# TODO: use anim only if screen is auto
				self.diff = (val - generate.y + dp(20))
				if self.diff > 0:
					if val > 0:
						Animation(y=self.diff, t="out_quad", d=.2).start(
							self.HomeScreen)
					else:
						Animation(y=0, t="in_quad", d=.2).start(self.HomeScreen)

	def on_signup(self, *args):
		if not self.LoginScreen:
			self.LoginScreen = self.root.get_screen("LoginScreen")
		box = self.LoginScreen.ids.box
		box.pos_hint = {"top": .8}
		box.opacity = 0
		self.animate_login(box)

	def set_list(self):
		def add_list(n):
			text_to_copy = "Demo text"
			self.rv_data.append(
				{
					"viewclass": "List",
					"primary_text": f"Google{n}",
					"button_actions": {
						"copy": lambda: exec(
							f'Clipboard.copy("{text_to_copy}"); toast("Item copied")',
							{"Clipboard": Clipboard, "toast": toast}),
						"update": lambda: exec("MDApp.get_running_app().open_update_dialog()"),
						"delete": lambda: toast("Item deleted")
					},
				}
			)

		for i in range(20):
			add_list(i)

	def animate_login(self, instance, ):
		if instance:
			Animation(pos_hint={"top": .95}, opacity=1, d=.4, t='out_back').start(instance)

	def generate_dark_color(self, color=None, hex_color=False, darkness=None, return_hex=False):
		if not color:
			color = self.generate_light_color(lightness=70)
		mx = max(color)
		if not darkness:
			factor = mx / 0.18
		else:
			factor = mx / (darkness / 100)
		color = [i / factor for i in color[:-1]]
		if not return_hex:
			return color + [1]
		else:
			r, g, b = color
			_hex = hex(round(r * 255))[2:] + hex(round(g * 255))[2:] + hex(round(b * 255))[2:]
			return _hex

	def generate_light_color(self, hex_color=False, color=None, return_hex=False, lightness=87):
		if hex_color:
			color = get_color_from_hex(hex_color)
		elif not color:
			color = self.theme_cls.primary_color[:-1]

		mx = max(color)
		mn = min(color)
		color1 = list(color)
		color1.remove(mx)
		mid = max(color1)
		range_mn = mx - mn
		range_md = mx - mid

		for i in range(3):
			if color[i] == mid:
				color[i] += range_md * lightness / 100
			elif color[i] == mn:
				color[i] += range_mn * lightness / 100
		if not return_hex:
			return color + [1]
		else:
			r, g, b = color
			_hex = hex(round(r * 255))[2:] + hex(round(g * 255))[2:] + hex(round(b * 255))[2:]
			return _hex

	def back_button(self, home_screen=False, *args):
		if not home_screen:
			self.screen_history.pop()
		else:
			self.screen_history = ['HomeScreen']
		self.root.transition.mode = 'pop'
		self.root.transition.direction = 'right'
		self.root.current = self.screen_history[-1]

	def open_exit_dialog(self):
		if not self.exit_dialog:
			self.exit_dialog = Dialog(
				title='Exit', text='Do you want to exit?', buttons=[
					MDFillRoundFlatButton(text='YES', on_release=lambda x: self.stop(), _radius=dp(20)),
					MDFlatButton(
						text='NO', _radius=dp(20), on_release=lambda x: self.exit_dialog.dismiss())])
		self.exit_dialog.open()

	def animation_behavior(self, instance):
		if not instance.opacity:
			Animation(opacity=1, d=.2, t='in_quad').start(instance)

	def change_screen(self, screen_name, *args):
		self.root.transition.mode = 'push'
		self.root.transition.direction = 'left'
		self.root.current = screen_name
		self.screen_history.append(screen_name)
		print(f'{self.screen_history = }')

	def on_dark_mode(self, instance, mode):
		current_screen = self.root.current
		if not self.HomeScreen:
			self.HomeScreen = self.root.get_screen("HomeScreen")
		if current_screen == 'HomeScreen':
			tab_manager = self.root.current_screen.ids.tab_manager
			primary_color = Animation(
				primary_accent=self.bg_color_dark if self.dark_mode else self.light_color,
				duration=.3
			)
			primary_color.start(self)
			if tab_manager.current == 'CreateScreen':
				self.anim = Animation(md_bg_color=self.theme_cls.opposite_bg_normal, duration=.3)
				self.anim.start(self.HomeScreen)

			primary_color.on_complete = self.set_mode

	def set_mode(self, *args):
		print("mode set")
		self.primary_accent = self.bg_color_dark if self.dark_mode else self.light_color
		if self.dark_mode:
			self.theme_cls.theme_style = 'Dark'
			self.theme_cls.primary_hue = '300'
			if platform == 'android':
				statusbar(status_color=self.dark_hex, white_text=False)
		else:
			self.theme_cls.theme_style = 'Light'
			self.theme_cls.primary_hue = '500'
			if platform == 'android':
				statusbar(status_color=self.light_hex, white_text=True)

		self.HomeScreen.ids.create.ids.circle_mode.rad = 0.1

	def toggle_mode(self, *args):
		self.dark_mode = not self.dark_mode

	def on_start(self):
		# self.HomeScreen.ids.create.ids.tab.=''
		if platform == 'android':
			statusbar(
				status_color=colors["Dark"]["CardsDialogs"] if self.dark_mode else self.light_hex,
				white_text=not self.dark_mode
			)


class RoundButton(MDFillRoundFlatButton):
	padding = [0, dp(20), 0, dp(20)]
	_radius = dp(20), dp(20)

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.theme_cls.bind(primary_hue=self.update_md_bg_color)


class Dialog(MDDialog):
	radius = [dp(30)] * 4

	def update_bg_color(self,*args):
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


class CheckboxLabel(ThemableBehavior, RectangularRippleBehavior, MDBoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.ripple_color = self.theme_cls.primary_light
		self.ripple_alpha = .2


if __name__ == "__main__":
	MainApp().run()
