__all__ = ("MDDialog",)

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import (
    ColorProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    OptionProperty,
    StringProperty,
)
from kivy.uix.modalview import ModalView

from kivymd.material_resources import DEVICE_TYPE
from kivymd.theming import ThemableBehavior
from kivymd.uix.button import BaseButton
from kivymd.uix.card import MDSeparator
from kivymd.uix.list import BaseListItem

Builder.load_string(
    """
#:import images_path kivymd.images_path


<BaseDialog>
    background: '{}/transparent.png'.format(images_path)

    canvas.before:
        PushMatrix
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: root.radius
        Scale:
            origin: self.center
            x: root._scale_x
            y: root._scale_y
    canvas.after:
        PopMatrix


<MDDialog>

    MDCard:
        id: container
        orientation: "vertical"
        size_hint_y: None
        height: self.minimum_height
        elevation: 20
        padding: "30dp", "30dp", "30dp", "15dp"
        radius: root.radius
        md_bg_color:
            root.theme_cls.bg_dark \
            if not root.md_bg_color else root.md_bg_color

        MDLabel:
            id: title
            text: root.title
            font_style: "H5"
            bold: True
            markup: True
            size_hint_y: None
            height: self.texture_size[1]
            valign: "top"

        BoxLayout:
            id: spacer_top_box
            size_hint_y: None
            height: root._spacer_top

        MDLabel:
            id: text
            text: root.text
            font_style: "Body1"
            theme_text_color: "Custom"
            text_color: root.theme_cls.disabled_hint_text_color
            size_hint_y: None
            height: self.texture_size[1]
            markup: True

        ScrollView:
            id: scroll
            size_hint_y: None
            height: root._scroll_height

            MDGridLayout:
                id: box_items
                adaptive_height: True
                cols: 1

        BoxLayout:
            id: spacer_bottom_box
            size_hint_y: None
            height: self.minimum_height

        AnchorLayout:
            id: root_button_box
            size_hint_y: None
            height: "52dp"
            anchor_x: "right"

            MDBoxLayout:
                id: button_box
                adaptive_size: True
                spacing: "8dp"
"""
)


class BaseDialog(ThemableBehavior, ModalView):
    radius = ListProperty([20, 20, 20, 20])
    _scale_x = NumericProperty(1)
    _scale_y = NumericProperty(1)


class MDDialog(BaseDialog):
    title = StringProperty()

    text = StringProperty()

    buttons = ListProperty()

    items = ListProperty()

    width_offset = NumericProperty(dp(48))

    type = OptionProperty(
        "alert", options=["alert", "simple", "confirmation", "custom"]
    )

    content_cls = ObjectProperty()

    md_bg_color = ColorProperty(None)

    _scroll_height = NumericProperty("28dp")
    _spacer_top = NumericProperty("24dp")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_resize=self.update_width)

        if self.size_hint == [1, 1] and (
                DEVICE_TYPE == "desktop" or DEVICE_TYPE == "tablet"
        ):
            self.size_hint = (None, None)
            self.width = min(dp(560), Window.width - self.width_offset)
        elif self.size_hint == [1, 1] and DEVICE_TYPE == "mobile":
            self.size_hint = (None, None)
            self.width = min(dp(280), Window.width - self.width_offset)

        if not self.title:
            self._spacer_top = 0

        if not self.buttons:
            self.ids.root_button_box.height = 0
        else:
            self.create_buttons()

        update_height = False
        if self.type in ("simple", "confirmation"):
            if self.type == "confirmation":
                self.ids.spacer_top_box.add_widget(MDSeparator())
                self.ids.spacer_bottom_box.add_widget(MDSeparator())
            self.create_items()
        if self.type == "custom":
            if self.content_cls:
                self.ids.container.remove_widget(self.ids.scroll)
                self.ids.container.remove_widget(self.ids.text)
                self.ids.spacer_top_box.add_widget(self.content_cls)
                self.ids.spacer_top_box.padding = (0, "24dp", "16dp", 0)
                update_height = True
        if self.type == "alert":
            self.ids.scroll.bar_width = 0

        if update_height:
            Clock.schedule_once(self.update_height)

    def update_width(self, *args):
        self.width = max(
            self.height + self.width_offset,
            min(
                dp(560) if DEVICE_TYPE != "mobile" else dp(280),
                Window.width - self.width_offset,
            ),
        )

    def update_height(self, *args):
        self._spacer_top = self.content_cls.height + dp(24)

    def on_open(self):
        # TODO: Add scrolling text.
        self.height = self.ids.container.height

    def get_normal_height(self):
        return (
                (Window.height * 80 / 100)
                - self._spacer_top
                - dp(52)
                - self.ids.container.padding[1]
                - self.ids.container.padding[-1]
                - 100
        )

    def edit_padding_for_item(self, instance_item):
        instance_item.ids._left_container.x = 0
        instance_item._txt_left_pad = "56dp"

    def create_items(self):
        if not self.text:
            self.ids.container.remove_widget(self.ids.text)
            height = 0
        else:
            height = self.ids.text.height

        for item in self.items:
            if issubclass(item.__class__, BaseListItem):
                height += item.height  # calculate height contents
                self.edit_padding_for_item(item)
                self.ids.box_items.add_widget(item)

        if height > Window.height:
            self.ids.scroll.height = self.get_normal_height()
        else:
            self.ids.scroll.height = height

    def create_buttons(self):
        for button in self.buttons:
            if issubclass(button.__class__, BaseButton):
                self.ids.button_box.add_widget(button)
