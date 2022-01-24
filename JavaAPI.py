from kivy.utils import platform

if platform == 'android':
    from android.runnable import run_on_ui_thread
    from jnius import autoclass

    Color = autoclass("android.graphics.Color")
    WindowManager = autoclass('android.view.WindowManager$LayoutParams')
    activity = autoclass('org.kivy.android.PythonActivity').mActivity
    Rect = autoclass('android.graphics.Rect')()
    View = autoclass('android.view.View')
    # WindowInsetsControllerCompat = autoclass('androidx.core.view.WindowInsetsControllerCompat')
    # ViewCompat = autoclass('androidx.core.view.ViewCompat')
    # Configuration = autoclass("android.content.res.Configuration")
    # WindowInsetsCompat=autoclass("androidx.core.view.WindowInsetsCompat")


    @run_on_ui_thread
    def fix_back_button():
        activity.onWindowFocusChanged(False)
        activity.onWindowFocusChanged(True)


    def keyboard_height():
        try:
            decor_view = activity.getWindow().getDecorView()
            height = activity.getWindowManager().getDefaultDisplay().getHeight()
            decor_view.getWindowVisibleDisplayFrame(Rect)
            return height - Rect.bottom

        except:
            return 0


    @run_on_ui_thread
    def statusbar(theme='Custom', status_color='121212', nav_color="FAFAFA", full=False):
        window = activity.getWindow()
        print('Setting StatusBar Color')  # Updates everytime color is changed
        window.clearFlags(WindowManager.FLAG_TRANSLUCENT_STATUS)
        try:
            """
            Below code (Comment Line) is kinda useless still I've it incase I need it future.
            """
            # if full:
            #     windowInsetsController = ViewCompat.getWindowInsetsController(
            #         window.getDecorView())
            #     windowInsetsController.setSystemBarsBehavior(
            #         WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE)
            #     windowInsetsController.hide(WindowInsetsCompat.Type.systemBars())
            #
            #     window.clearFlags(WindowManager.FLAG_TRANSLUCENT_STATUS)
            #     window.addFlags(WindowManager.FLAG_TRANSLUCENT_STATUS, true)
            #     window.setStatusBarColor(Color.TRANSPARENT)
            #     window.setNavigationBarColor(Color.TRANSPARENT)
            # else:
            window.addFlags(WindowManager.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS)
            if theme == 'black':
                window.setNavigationBarColor(Color.parseColor('#' + status_color))
                window.setStatusBarColor(Color.parseColor('#' + status_color))
                window.getDecorView().setSystemUiVisibility(0)
            elif theme == 'white':
                window.setNavigationBarColor(Color.parseColor('#FAFAFA'))
                window.setStatusBarColor(Color.parseColor('#FAFAFA'))
                window.getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR |
                                                            View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR)
            elif theme == 'Custom':
                window.setNavigationBarColor(Color.parseColor('#' + nav_color))
                window.setStatusBarColor(Color.parseColor('#' + status_color))

        except Exception:
            pass


    def dark_mode():
        night_mode_flags = activity.getContext().getResources().getConfiguration().uiMode & Configuration.UI_MODE_NIGHT_MASK
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
            return 'Portrait'
        else:
            return 'Landscape'
