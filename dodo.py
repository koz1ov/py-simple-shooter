"""Automatization of work pypeline."""
import glob
from doit.tools import create_folder
from functools import partial
import shutil
import os
from doit.task import clean_targets

DOIT_CONFIG = {'default_tasks': ['compile', 'wheel']}


def task_extract() -> dict:
    """Generate *.pot file for translation."""
    return {
        "actions": [
            (create_folder, ['shooter/po']),
            'pybabel extract -o shooter/po/shooter.pot shooter'
        ],
        "file_dep": glob.glob('**/*.py', recursive=True),
        "targets": ['shooter/po/shooter.pot'],
        "clean": True,
    }


def task_init() -> dict:
    """Generate *.po for writing translations."""
    return {
        "actions": [
            (create_folder, ['shooter/locale']),
            'pybabel init -D shooter -i shooter/po/shooter.pot -d shooter/locale -l ru',
            'pybabel init -D shooter -i shooter/po/shooter.pot -d shooter/locale -l en',
        ],
        "file_dep": ['shooter/po/shooter.pot'],
        "targets": [
            'shooter/locale/ru/LC_MESSAGES/shooter.po',
            'shooter/locale/en/LC_MESSAGES/shooter.po',
        ],
    }


def task_compile() -> dict:
    """Compile *.po files to *.mo files."""
    return {
        "actions": [
            "pybabel compile -D shooter -d shooter/locale -l ru",
            "pybabel compile -D shooter -d shooter/locale -l en"
        ],
        # "file_dep": [
        #     'src/py-simple-shooter/locale/ru/LC_MESSAGES/py-simple-shooter.po',
        #     'src/py-simple-shooter/locale/en/LC_MESSAGES/py-simple-shooter.po',],
        "targets": [
            'shooter/locale/ru/LC_MESSAGES/shooter.mo',
            'shooter/locale/en/LC_MESSAGES/shooter.mo',
        ],
        "clean": True,
    }


def task_update() -> dict:
    """Update existing message catalogs from a *.pot file."""
    return {
        "actions": [
            "pybabel update -D shooter -i shooter/po/shooter.pot -d shooter/locale -l en",
            "pybabel update -D shooter -i shooter/po/shooter.pot -d shooter/locale -l ru",
        ],
        "task_dep": ['extract'],
        "file_dep": ['shooter/po/shooter.pot'],
        "clean": True,
    }


def task_check_code_style():
    """Check style for flake8."""
    return {
        "actions": ['flake8 --config .flake8 shooter'],
    }


def task_check_docstyle():
    """Check docstrings for pydocstyle."""
    return {
        "actions": ['pydocstyle shooter'],
    }


def task_wheel():
    """Create wheel distribution."""
    clean_egg = partial(shutil.rmtree, 'shooter.egg-info', ignore_errors=True)
    clean = partial(shutil.rmtree, 'dist', ignore_errors=True)
    return {
        "actions": ['python3 -m build -w'],
        "verbosity": 2,
        "task_dep": ['compile'],
        "targets": glob.glob("dist/*.whl") + glob.glob("*.egg-info")
        if glob.glob("dist/*.whl") else ['.whl'],
        "clean": [clean_egg, clean, clean_targets],
    }


def task_source():
    """Create source distribution."""
    clean = partial(shutil.rmtree, 'dist', ignore_errors=True)
    clean_build = partial(shutil.rmtree, 'build', ignore_errors=True)
    return {
        "actions": ['python3 -m build -s'],
        "verbosity": 2,
        "targets": glob.glob("dist/*.tar.gz") if glob.glob("dist/*.tar.gz") else ['.tar.gz'],
        "clean": [clean, clean_build],
    }


def task_html_documentation():
    """Generate html documentation using sphinx."""
    build_dir = 'docs/_build'
    clean_build = partial(shutil.rmtree, build_dir, ignore_errors=False)
    return {
        "actions": ['sphinx-build docs %(targets)s'],
        "file_dep": glob.glob("**/*.py", recursive=True) + glob.glob("**/*.rst", recursive=True),
        "task_dep": ["compile"],
        "targets": [build_dir],
        "clean": [clean_build],
    }
