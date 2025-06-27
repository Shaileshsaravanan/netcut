from setuptools import setup, find_packages

setup(
    name="netcut",
    version="0.1",
    packages=find_packages(),
    install_requires=["click", "psutil", "apscheduler"],
    entry_points={
        "console_scripts": [
            "netcut=netcut.cli:cli",
        ],
    },
)