import glob
from doit.tools import create_folder
DOIT_CONFIG = {'default_tasks': ['compile']}


def task_extract() -> dict:
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
    return {
        "actions": [
            (create_folder, ['src/py-simple-shooter/locale']),
            'pybabel init -D py-simple-shooter -i src/py-simple-shooter/po/py-simple-shooter.pot -d src/py-simple-shooter/locale -l ru',
            'pybabel init -D py-simple-shooter -i src/py-simple-shooter/po/py-simple-shooter.pot -d src/py-simple-shooter/locale -l en',
            ],
        "task_dep": ['extract'],
        "file_dep": ['src/py-simple-shooter/po/py-simple-shooter.pot'],
        "targets": [
            'src/py-simple-shooter/locale/ru/LC_MESSAGES/py-simple-shooter.po',
            'src/py-simple-shooter/locale/en/LC_MESSAGES/py-simple-shooter.po',
            ],
        "clean": True,
    }


def task_compile() -> dict:
    return {
        "actions": [
            "pybabel compile -D py-simple-shooter -d src/py-simple-shooter/locale -l ru",
            "pybabel compile -D py-simple-shooter -d src/py-simple-shooter/locale -l en"
            ],
        "task_dep": ['init'],
        "file_dep": [
            'src/py-simple-shooter/locale/ru/LC_MESSAGES/py-simple-shooter.po',
            'src/py-simple-shooter/locale/en/LC_MESSAGES/py-simple-shooter.po',],
        "targets": [
            'src/py-simple-shooter/locale/ru/LC_MESSAGES/py-simple-shooter.mo',
            'src/py-simple-shooter/locale/en/LC_MESSAGES/py-simple-shooter.mo',
            ],
        "clean": True,
    }


def task_update() -> dict:
    return {
        "actions": [
            "pybabel update -D py-simple-shooter -i src/py-simple-shooter/po/py-simple-shooter.pot -d src/py-simple-shooter/locale -l en",
            "pybabel update -D py-simple-shooter -i src/py-simple-shooter/po/py-simple-shooter.pot -d src/py-simple-shooter/locale -l en"
            ],
        "task_dep": ['extract'],
        "file_dep": ['src/py-simple-shooter/po/py-simple-shooter.pot'],
        "clean": True,
    }
