import ttkbootstrap.constants as tc
from ttkbootstrap.scrolled import ScrolledFrame


class CustomizedScrolledFrame(ScrolledFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def _on_mousewheel(self, event):
        """Callback for when the mouse wheel is scrolled."""
        if self.winsys.lower() == "win32":
            delta = -int(event.delta / 120)
        elif self.winsys.lower() == "aqua":
            delta = -int(event.delta / 12)
        elif event.num == 4:
            delta = -10
        elif event.num == 5:
            delta = 10
        self.yview_scroll(delta, tc.UNITS)
