import os
import sys


def get_file(project_path: str) -> str:
    """Get the absolute path to a resource file, works both in development and PyInstaller bundle."""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Running in a PyInstaller bundle
        base_path = sys._MEIPASS
    else:
        # Running in development
        base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    
    return os.path.join(base_path, project_path)
