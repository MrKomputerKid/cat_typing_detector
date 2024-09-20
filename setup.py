from setuptools import setup

APP = ['cat_typing_detector.py']
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,  # Hide the app from the Dock
    },
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
