from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, ListProperty, ColorProperty
from kivy.uix.boxlayout import BoxLayout

from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix import SpecificBackgroundColorBehavior
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton

Builder.load_string('''
<Toolbar>
    id: toolbox
    set_opacity: root.set_opacity
    size_hint_y: None
    elevation: root.elevation
    md_bg_color: root.md_bg_color if root.md_bg_color !=[0,0,0,0] else [0,0,0,0] 
    pos_hint:{'top':1}
    spacing : '5dp'
    height: root.theme_cls.standard_increment + root.increase_height

    MDBoxLayout:
        id: left_action_box
        adaptive_size: True
        pos_hint: {'center_y': .5}  
    
    MDBoxLayout:
        
        adaptive_height: True
        pos_hint: {'center_y': .5} 
        MDLabel:
            id:setting_label
            text: root.title
            theme_text_color:'Custom'
            font_size: root.text_height  if root.text_height else 0
            font_style: "H6"
            font_name:'Poppins' 
            text_color:app.theme_cls.text_color if root.icon_color is None else root.icon_color
            shorten: True
            shorten_from: "right"
            height: root.height-root.padding[0]/2
            
    MDBoxLayout:
        id: right_action_box
        adaptive_size: True
        spacing:'5dp'
        pos_hint: {'center_y': .5}
        
        
    
        
''')


class Toolbar(MDBoxLayout, ThemableBehavior, FakeRectangularElevationBehavior, SpecificBackgroundColorBehavior):
    elevation = NumericProperty(0)
    adaptive_height = True
    md_bg_color = ColorProperty()
    title = StringProperty('')
    increase_height= NumericProperty(0)
    left_action_items = ListProperty()
    right_action_items = ListProperty()
    icon_color = ColorProperty(None)
    text_height = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_left_action_items(self, instance, value):
        self.ids.left_action_box.clear_widgets()
        for icon_left_action in self.left_action_items:
            if len(icon_left_action) == 1:
                self.icon_left = MDIconButton(icon=icon_left_action[0], theme_text_color='Custom',
                                              text_color=self.icon_color, user_font_size=self.text_height,
                                              pos_hint={'center_y': .5})

            else:
                self.icon_left = MDIconButton(icon=icon_left_action[0], theme_text_color='Custom',
                                              text_color=self.icon_color, user_font_size=self.text_height,
                                              pos_hint={'center_y': .5}, on_release=icon_left_action[1])

            self.ids.left_action_box.add_widget(self.icon_left)

    def on_right_action_items(self, instance, value):
        self.ids.right_action_box.clear_widgets()
        for icon_right_action in self.right_action_items:
            if len(icon_right_action) == 1:
                self.icon_right = MDIconButton(icon=icon_right_action[0], theme_text_color='Custom',
                                               text_color=self.icon_color, user_font_size=self.text_height,
                                               pos_hint={'center_y': .5})

            else:
                self.icon_right = MDIconButton(icon=icon_right_action[0], theme_text_color='Custom',
                                               text_color=self.icon_color, user_font_size=self.text_height,
                                               pos_hint={'center_y': .5}, on_release=icon_right_action[1])
            self.ids.right_action_box.add_widget(self.icon_right)

    def on_icon_color(self, instance, color):
        for icon in self.ids.left_action_box.children:
            icon.text_color = color
        for icon in self.ids.right_action_box.children:
            icon.text_color = color


if __name__ == '__main__':
    class ToolbarApp(MDApp):
        def build(self):
            return Builder.load_string('''
Screen:
    Toolbar: 
        title:'Test'
        icon_color: [1,0,.4,1]
        right_action_items:[['cog',lambda x: print('Call any function you want like this.')]]
                ''')


    ToolbarApp().run()
