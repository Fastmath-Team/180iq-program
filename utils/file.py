import os


def get_file(project_path: str) -> str:
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)), f"../{project_path}"
    )
