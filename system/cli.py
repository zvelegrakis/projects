import pathlib
import shutil

import click

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "projects"
TEMPLATES = ROOT / "templates"


@click.group()
def main():
    pass


@main.command("init")
@click.argument("template")
@click.argument("name")
def init_project(template, name):
    path = scaffold(template, name)
    click.echo(str(path))


def next_index():
    PROJECTS.mkdir(exist_ok=True)
    dirs = [p for p in PROJECTS.iterdir() if p.is_dir()]
    if not dirs:
        return "000"

    nums = []
    for d in dirs:
        head = d.name.split("_", 1)[0]
        try:
            nums.append(int(head))
        except ValueError:
            continue

    if not nums:
        return "000"

    return f"{max(nums) + 1:03d}"


def scaffold(template_name, project_name):
    src = TEMPLATES / template_name / "skeleton"
    if not src.exists():
        raise RuntimeError(f"missing template: {template_name}")

    idx = next_index()
    dest = PROJECTS / f"{idx}_{project_name}"
    shutil.copytree(src, dest)
    return dest
