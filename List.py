from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty, get_color_from_hex
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivymd.uix.behaviors import RectangularRippleBehavior

from kivymd.app import MDApp
from kivymd.material_resources import dp
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout

KV = '''
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
    md_bg_color:app.theme_cls.primary_light[:-1] + [.3] if self.selected else app.theme_cls.primary_light[:-1] + [0]
    MDLabel:
        adaptive_height: True
        text:root.primary_text
    MDBoxLayout:
        id: sec_box
        size_hint_y:None
        height:root.selected*dp(30) 
        opacity: root.selected*1
        MDLabel:
            adaptive_height:True
            text:root.secondary_text
            theme_text_color:'Secondary'
        MDIconButton:
            id: button
            disabled: not root.selected
            md_bg_color_disabled:[0,0,0,0]
            icon:'content-copy'
            pos_hint:{'center_y':.5}
        MDIconButton:
            id: button
            disabled: not root.selected
            md_bg_color_disabled:[0,0,0,0]
            icon:'pencil-outline'
            pos_hint:{'center_y':.5}
            # text_color:[.3,.3,.3,1]
        MDIconButton:
            id: button
            disabled: not root.selected
            md_bg_color_disabled:[0,0,0,0]
            icon:'trash-can-outline'
            pos_hint:{'center_y':.5}

'''


class List(RectangularRippleBehavior, RecycleDataViewBehavior, ThemableBehavior, ButtonBehavior,
		   MDBoxLayout):  # ThemableBehavior, ButtonBehavior, MDBoxLayout or MDCard
	Builder.load_string(KV)
	selected = BooleanProperty(False)
	primary_text = StringProperty('Google')
	ripple_behavior = True
	ripple_alpha = .1
	secondary_text = StringProperty("12345678910111213")

	def on_release(self):
		if self.selected:
			if self.right - self.last_touch.x >= dp(170):
				self.selected = False
				self.parent.clear_selection()
		else:
			self.parent.select_with_touch(self.index, None)

	def refresh_view_attrs(self, rv, index, data):
		self.index = index
		return super().refresh_view_attrs(rv, index, data)

	def apply_selection(self, rv, index, is_selected):
		self.selected = is_selected
		rv.data[index]["selected"] = is_selected

	# def on_selected(self, instance, selected):
	# 	def anim(*args):
	# 		if selected:
	# 			Animation(md_bg_color=app.theme_cls.primary_light[:-1] + [.3], d=.1).start(instance)
	# 		else:
	# 			instance.md_bg_color = app.theme_cls.primary_light[:-1] + [0]
	# 			Animation(height=dp(0), d=.1, opacity=0).start(self.ids.sec_box)
	#
	# 	app = MDApp.get_running_app()
	# 	print(f"{instance} is selected")
	#
	# 	Clock.schedule_once(anim, 1)


if __name__ == '__main__':
	class CardBehavior(MDApp):
		def on_start(self):
			self.bg_color_dark = get_color_from_hex('262626')
			# self.theme_cls.theme_style='Dark'
			self.fps_monitor_start()

		def build(self):
			return Builder.load_string("""
MDScreen:
    md_bg_color:[.8,.8,.8,1]
    # RecycleView:
    MDBoxLayout:
        pos_hint:{'top':0.8}
        adaptive_height: True
        # size_hint_y:.7
        # height:'100dp'
        orientation:'vertical'
        # OneLineListItem:
        #     text:'Hi'
        List:
        List:
        List:
        List:
        # OneLineListItem:
        #     text:'Hi'
        # OneLineListItem:
        #     text:'Hi'
        # OneLineListItem:
        #     text:'Hi'
        # OneLineListItem:
        #     text:'Hi'
        List:
        # OneLineListItem:
        #     text:'Hi'
        
            
            """)


	CardBehavior().run()
