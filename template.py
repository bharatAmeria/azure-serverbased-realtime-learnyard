import os
from pathlib import Path

project_name = "src"

list_of_files = [
    ".github/workflows/docker_image.yaml",
    ".github/workflows/pipeline.yaml",
    "app/templates/index.html",
    "app/__init__.py",
    "app/app.py",
    "app/Dockerfile",
    "app/requirements.txt",
    f"{project_name}/__init__.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/processing.py",
    f"{project_name}/config/__init__.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/logger/__init__.py",
    "main.py",
    ".dockerignore",
    ".env",
    ".project-root",
    "config.json",
    "project_flow.txt",
    "pyproject.toml",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
    else:
        print(f"file is already present at: {filepath}")