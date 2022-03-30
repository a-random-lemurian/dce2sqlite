from setuptools import setup


setup(
    name="dce2sqlite",
    description="Convert DCE JSON files to SQLite databases",
    license="MIT",
    entry_points={
        "console_scripts": [
            "dce2sqlite=dce2sqlite.main:entry"
        ]
    },
    version="0.1.0",
    author="Lemuria"
)
