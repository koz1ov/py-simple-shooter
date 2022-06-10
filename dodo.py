import glob
from doit.tools import create_folder
from functools import partial
import shutil
from doit.task import clean_targets

DOIT_CONFIG = {'default_tasks': ['compile']}


def task_extract() -> dict:
    """Generate *.pot file for translation."""
    return {
        "actions": [
            (create_folder, ['src/py-simple-shooter/po']),
            'pybabel extract -o src/py-simple-shooter/po/py-simple-shooter.pot src/py-simple-shooter'
            ],
        "file_dep": glob.glob('**/*.py', recursive=True),
        "targets": ['src/py-simple-shooter/po/py-simple-shooter.pot'],
        "clean": True,
    }


def task_init() -> dict:
    """Generate *.po for writing translations."""
    return {
        "actions": [
            (create_folder, ['src/py-simple-shooter/locale']),
            'pybabel init -D py-simple-shooter -i src/py-simple-shooter/po/py-simple-shooter.pot -d src/py-simple-shooter/locale -l ru',
            'pybabel init -D py-simple-shooter -i src/py-simple-shooter/po/py-simple-shooter.pot -d src/py-simple-shooter/locale -l en',
            ],
        "file_dep": ['src/py-simple-shooter/po/py-simple-shooter.pot'],
        "targets": [
            'src/py-simple-shooter/locale/ru/LC_MESSAGES/py-simple-shooter.po',
            'src/py-simple-shooter/locale/en/LC_MESSAGES/py-simple-shooter.po',
            ],
    }


def task_compile() -> dict:
    """Compile *.po files to *.mo files."""
    return {
        "actions": [
            "pybabel compile -D py-simple-shooter -d src/py-simple-shooter/locale -l ru",
            "pybabel compile -D py-simple-shooter -d src/py-simple-shooter/locale -l en"
            ],
        # "file_dep": [
        #     'src/py-simple-shooter/locale/ru/LC_MESSAGES/py-simple-shooter.po',
        #     'src/py-simple-shooter/locale/en/LC_MESSAGES/py-simple-shooter.po',],
        "targets": [
            'src/py-simple-shooter/locale/ru/LC_MESSAGES/py-simple-shooter.mo',
            'src/py-simple-shooter/locale/en/LC_MESSAGES/py-simple-shooter.mo',
            ],
        "clean": True,
    }


def task_update() -> dict:
    """Update existing message catalogs from a *.pot file."""
    return {
        "actions": [
            "pybabel update -D py-simple-shooter -i src/py-simple-shooter/po/py-simple-shooter.pot -d src/py-simple-shooter/locale -l en",
            "pybabel update -D py-simple-shooter -i src/py-simple-shooter/po/py-simple-shooter.pot -d src/py-simple-shooter/locale -l ru"
            ],
        "task_dep": ['extract'],
        "file_dep": ['src/py-simple-shooter/po/py-simple-shooter.pot'],
        "clean": True,
    }


def task_check_code_style():
    """Check style for flake8."""
    return {
        "actions": ['flake8 --config .flake8 src/py-simple-shooter'],
    }


def task_check_docstyle():
    """Check docstrings for pydocstyle."""
    return {
        "actions": ['pydocstyle src/py-simple-shooter'],
    }


def task_wheel():
    """Create wheel distribution."""
    clean_build = partial(shutil.rmtree, 'build', ignore_errors=True)
    clean_egg = partial(shutil.rmtree, 'py-simple-shooter.egg-info', ignore_errors=True)
    return {
        "actions": ['python3 -m build '],
        "verbosity": 2,
        "task_dep": ['compile'],
        "targets": glob.glob("dist/*.whl") if glob.glob("dist/*.whl") else ['.whl'],
        "clean": [clean_targets, clean_build, clean_egg],
    }
