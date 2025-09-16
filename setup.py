#!/usr/bin/env python3
"""
Setup script for ADB Wireless Connection Script
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="adb-wireless-connector",
    version="1.0.0", (UPDATES - N/A)
    author="Piyush Golan",
    author_email="golanpiyush32.com",
    description="Automatically set up wireless ADB connections for Android devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/golanpiyush/ADB-IPAddr-Script",
    py_modules=["adb_wireless"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "ADB-IPAddr-Script:main",
        ],
    },
    keywords="adb android debug wireless development mobile",
)
