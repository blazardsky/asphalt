from setuptools import setup

setup(
    name="asphalt",
    version="0.1",
    py_modules=["asphalt"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "asphalt=asphalt:main",
        ],
    },
)
