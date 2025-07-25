#!/usr/bin/env python3
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vid-to-gif",
    version="1.0.0",
    description="A command-line tool to convert videos to high-quality GIFs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="aousabdo",
    author_email="aousabdo@example.com",
    url="https://github.com/aousabdo/vid-to-gif",
    py_modules=['vid_to_gif'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'vid-to-gif=vid_to_gif:main',
        ],
    },
    python_requires='>=3.6',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Integrity :: Command-Line Utilities",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="video gif converter ffmpeg",
)