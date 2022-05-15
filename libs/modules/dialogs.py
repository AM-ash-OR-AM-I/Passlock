from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.properties import (
    ListProperty,
    NumericProperty,
    ObjectProperty,
    OptionProperty,
    StringProperty,
)
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.dialog import BaseDialog
from kivymd.material_resources import dp

Builder.load_string("""
#: import md_icons kivymd.icon_definitions.md_icons
#: import Window kivy.core.window.Window

<AKAlertDialog>:
    background_color: [0,0,0,0]
    overlay_color: [0,0,0,0.25]
    size_hint: alert.width / Window.width, alert.height / Window.height
    MainAlertBox:   
        id: alert
        size_hint: None,None
        elevation: root.elevation
        size: root.size_portrait if root._orientation == "portrait" \
        else root.size_landscape
        orientation: "vertical" if root._orientation == "portrait" \
            else "horizontal"

        canvas.before:
            Color:
                rgba: root.bg_color if root.bg_color else root.theme_cls.bg_light
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [root.dialog_radius, ]

        canvas.after:
            Color:
                rgba: root.progress_color if root.progress_color else root.theme_cls.primary_dark
            RoundedRectangle:
                pos: self.pos[0] + root.dialog_radius, self.pos[1] + root.height - root.progress_width
                size: root._progress_value, root.progress_width
                radius: [root.progress_width / 2, ]

        BoxLayout:
            size_hint_y: None if root._orientation == "portrait"  \
                else 1

            size_hint_x: None if root._orientation == "landscape" \
                else 1

            size: (root.width, root.header_height_portrait) if root._orientation == "portrait" \
                else (root.header_width_landscape, root.height)

            canvas.before:
                Color:
                    rgba: root.header_bg if root.header_bg else root.theme_cls.primary_color
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [root.dialog_radius, root.dialog_radius, 0, 0] if root._orientation == "portrait" \
                        else [root.dialog_radius, 0, 0, root.dialog_radius]

            MDLabel:
                font_style: "Icon" if root.header_text_type == "icon" else "Body1"
                bold: True
                text: u"{}".format(md_icons[root.header_icon]) if root.header_text_type == "icon" else root.header_text
                theme_text_color: "Custom"
                text_color: root.header_color if root.header_color else [1, 1, 1, 1]
                valign: root.header_v_pos
                halign: root.header_h_pos
                font_size: root.header_font_size

        BoxLayout:
            id: content
    """
)


class MainAlertBox(FakeRectangularElevationBehavior, BoxLayout):
    pass


class AKAlertDialog(BaseDialog):

    dialog_radius = NumericProperty(dp(30))
    radius = [dp(30)] * 4
    bg_color = ListProperty()
    auto_dismiss = True
    size_portrait = ListProperty(["250dp", "350dp"])
    size_landscape = ListProperty(["400dp", "250dp"])
    header_width_landscape = NumericProperty("110dp")
    header_height_portrait = NumericProperty("110dp")
    fixed_orientation = OptionProperty(None, options=["portrait", "landscape"])
    header_bg = ListProperty()
    header_text_type = OptionProperty("icon", options=["icon", "text"])
    header_text = StringProperty()
    header_icon = StringProperty("android")
    header_color = ListProperty()
    header_h_pos = StringProperty("center")
    header_v_pos = StringProperty("center")
    header_font_size = NumericProperty("55dp")
    progress_interval = NumericProperty(None)
    progress_width = NumericProperty("2dp")
    progress_color = ListProperty()
    elevation = NumericProperty(5)
    content_cls = ObjectProperty()
    _anim_duration = 0.25
    _orientation = StringProperty()
    _progress_value = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_resize=self._get_orientation)
        self.register_event_type("on_progress_finish")
        Clock.schedule_once(self._update)

    def _update(self, *args):
        self._get_orientation()

    def _get_orientation(self, *args):
        if self.fixed_orientation:
            self._orientation = self.fixed_orientation
        elif self.theme_cls.device_orientation == "portrait":
            self._orientation = "portrait"
        else:
            self._orientation = "landscape"

    def on_content_cls(self, *args):
        if not self.content_cls:
            return

        self.ids.content.clear_widgets()
        self.ids.content.add_widget(self.content_cls)

    def on_open(self):
        self._start_progress()
        return super().on_open()

    def on_pre_open(self):
        self._opening_animation()
        return super().on_pre_open()

    def on_dismiss(self):
        self._dismiss_animation()
        return super().on_dismiss()

    def _opening_animation(self):
        self.opacity = 0
        anim = Animation(opacity=1, duration=self._anim_duration, t="out_quad")
        anim.start(self)

    def _dismiss_animation(self):
        anim = Animation(opacity=0, duration=self._anim_duration - .05, t="out_quad")
        anim.start(self)

    def _start_progress(self):
        if not self.progress_interval:
            return
        max_width = self.size[0] - self.dialog_radius * 2
        anim = Animation(_progress_value=max_width, duration=self.progress_interval)
        anim.bind(on_complete=lambda x, y: self.dispatch("on_progress_finish"))
        anim.start(self)

    def on_progress_finish(self, *args):
        pass
