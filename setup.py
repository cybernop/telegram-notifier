#!/usr/bin/env python

import setuptools

setuptools.setup(
    name='telnotif',
    version='0.1.0',
    description='Python notifications for Telegramv ia REST',
    author='Alexander Schulze',
    packages=setuptools.find_packages(),
    install_requires=[
        'python-telegram-bot',
    ]
)
