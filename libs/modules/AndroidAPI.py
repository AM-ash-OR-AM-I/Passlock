from kivy.utils import platform

if platform == "android":
    from android.runnable import run_on_ui_thread
    from jnius import autoclass
    from jnius import JavaException

    Color = autoclass("android.graphics.Color")
    WindowManager = autoclass("android.view.WindowManager$LayoutParams")
    activity = autoclass("org.kivy.android.PythonActivity").mActivity
    View = autoclass("android.view.View")
    Configuration = autoclass("android.content.res.Configuration")

    def _class_call(cls, args: tuple, instantiate: bool):
        if not args:
            return cls() if instantiate else cls
        else:
            return cls(*args)

    def Rect(*args, instantiate: bool = False):
        return _class_call(autoclass("android.graphics.Rect"), args, instantiate)

    @run_on_ui_thread
    def fix_back_button():
        activity.onWindowFocusChanged(False)
        activity.onWindowFocusChanged(True)

    def keyboard_height():
        try:
            decor_view = activity.getWindow().getDecorView()
            height = activity.getWindowManager().getDefaultDisplay().getHeight()
            decor_view.getWindowVisibleDisplayFrame(Rect)
            return height - Rect().bottom

        except JavaException:
            return 0

    @run_on_ui_thread
    def statusbar(
        theme="Custom",
        status_color="121212",
        nav_color=None,
        white_text=None,
        full=False,
    ):
        window = activity.getWindow()
        print("Setting StatusBar Color")  # Updates everytime color is changed
        window.clearFlags(WindowManager.FLAG_TRANSLUCENT_STATUS)
        try:
            window.addFlags(WindowManager.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS)
            if theme == "black":
                window.setNavigationBarColor(Color.parseColor("#" + status_color))
                window.setStatusBarColor(Color.parseColor("#" + status_color))
                window.getDecorView().setSystemUiVisibility(0)
            elif theme == "white":
                window.setNavigationBarColor(Color.parseColor("#FAFAFA"))
                window.setStatusBarColor(Color.parseColor("#FAFAFA"))
                window.getDecorView().setSystemUiVisibility(
                    View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR
                    | View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR
                )
            elif theme == "Custom":
                if nav_color is None:
                    nav_color = status_color
                window.setNavigationBarColor(Color.parseColor("#" + nav_color))
                window.setStatusBarColor(Color.parseColor("#" + status_color))
                if white_text is True:
                    window.getDecorView().setSystemUiVisibility(
                        View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR
                        | View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR
                    )
                elif white_text is False:
                    window.getDecorView().setSystemUiVisibility(0)

        except Exception:
            pass

    def android_dark_mode():
        night_mode_flags = (
            activity.getContext().getResources().getConfiguration().uiMode
            & Configuration.UI_MODE_NIGHT_MASK
        )
        if night_mode_flags == Configuration.UI_MODE_NIGHT_YES:
            return True
        elif night_mode_flags in [
            Configuration.UI_MODE_NIGHT_NO,
            Configuration.UI_MODE_NIGHT_UNDEFINED,
        ]:
            return False

    def orientation():
        config = activity.getResources().getConfiguration()
        if config.orientation == 1:
            return "Portrait"
        else:
            return "Landscape"
