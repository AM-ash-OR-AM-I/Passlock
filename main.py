from kivy import platform
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.properties import BooleanProperty, ColorProperty, get_color_from_hex, NumericProperty

from kivymd.app import MDApp
from kivymd.color_definitions import colors
from kivymd.material_resources import dp
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatButton
from libs.uix.classes import Dialog, RoundButton
from libs.uix.root import Root

if platform != 'android':
	Window.size = (450, 900)
else:
	from libs.modules.AndroidAPI import statusbar

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
	path_to_live_ui = 'OtherStuff/custom_dialog.kv'
	primary_accent = ColorProperty()
	signup = BooleanProperty(True)
	HomeScreen = LoginScreen = SettingScreen = update_dialog = exit_dialog = None

	def __init__(self):
		super().__init__()
		self.theme_cls.primary_palette = 'DeepOrange'
		self.light_color = self.generate_light_color()
		self.dark_color = self.generate_dark_color()  # 262626
		self.login_circle_light = self.generate_light_color(lightness=70)
		self.primary_accent = self.dark_color if self.dark_mode else self.light_color
		self.light_hex = self.generate_light_color(return_hex=True)
		self.dark_hex = self.generate_dark_color(return_hex=True)

	def build(self):
		self.root = Root()
		self.root.set_current("LoginScreen")

	def on_key_height(self, instance, val):

		""" Used to move screen up/down so that UI elements are visible when keyboard is shown. """

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
				self.diff = (val - generate.y + dp(20))
				if self.diff > 0:
					if val > 0:
						Animation(y=self.diff, t="out_quad", d=.2).start(
							self.HomeScreen)
					else:
						Animation(y=0, t="in_quad", d=.2).start(self.HomeScreen)
			else:
				Window.softinput_mode = "below_target"

	def on_signup(self, *args):

		""" Animation to be shown when clicking on login or signup """

		if not self.LoginScreen:
			self.LoginScreen = self.root.get_screen("LoginScreen")
		box = self.LoginScreen.ids.box
		box.pos_hint = {"top": .8}
		box.opacity = 0
		self.animate_login(box)

	def animate_login(self, instance, ):

		""" Animation to be shown when user enters the app """

		if instance:
			Animation(pos_hint={"top": .95}, opacity=1, d=.4, t='out_back').start(instance)

	def generate_dark_color(self, color = None, darkness=82, return_hex=False):
		"""
		:param color: Takes color like [.5,.5,.5, 1] as Parameter
		:param darkness: int between 0 - 99 with 99 having max_darkness.
		:param return_hex: Boolean if set true it will return dark color in hex format.
		:return:
		"""
		if not color:
			color = self.generate_light_color(lightness=70)
		mx = max(color)
		if not darkness:
			factor = mx / 0.18
		else:
			factor = mx / ((100 - darkness) / 100)
		color = [i / factor for i in color[:-1]]
		if not return_hex:
			return color + [1]
		else:
			r, g, b = color
			_hex = hex(round(r * 255))[2:] + hex(round(g * 255))[2:] + hex(round(b * 255))[2:]
			return _hex

	def generate_light_color(self, hex_color=False, color=None, return_hex=False, lightness=87):
		"""
		:param hex_color:  Instead of passing color as list hexadecimal value can be passed.
		:param color: Takes color like [.5,.5,.5, 1] as Parameter
		:param return_hex: Boolean value if set true the function will return hexadecimal value.
		:param lightness: Value from 0-100. If set to 100 it will return white and 0 will return original color.
		:return: 
		"""
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

	def on_dark_mode(self, instance, mode):
		current_screen = self.root.current
		if not self.HomeScreen:
			self.HomeScreen = self.root.get_screen("HomeScreen")
		if current_screen == 'HomeScreen':
			tab_manager = self.root.current_screen.ids.tab_manager
			primary_color = Animation(
				primary_accent=self.dark_color if self.dark_mode else self.light_color,
				duration=.3
			)
			primary_color.start(self)
			if tab_manager.current == 'CreateScreen':
				self.anim = Animation(md_bg_color=self.theme_cls.opposite_bg_normal, duration=.3)
				self.anim.start(self.HomeScreen)

			primary_color.on_complete = self.set_mode

	def set_mode(self, *args):
		print("mode set")
		self.primary_accent = self.dark_color if self.dark_mode else self.light_color
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
		""" Sets status bar color in android. """
		if platform == 'android':
			statusbar(
				status_color=colors["Dark"]["CardsDialogs"] if self.dark_mode else self.light_hex,
				white_text=not self.dark_mode
			)


if __name__ == "__main__":
	MainApp().run()
