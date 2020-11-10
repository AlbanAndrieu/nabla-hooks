# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

import hooks

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='nabla_hooks',
    version=hooks.__version__,
    packages=find_packages(),
    # scripts=["hooks/get_msg.py"],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    #install_requires=["docutils>=0.3", "jira>=2.0.0", "termcolor>=1.1.0"],
    install_requires=requirements,

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the "hooks" package, too:
        'hooks': ['*.msg'],
    },

    # metadata to display on PyPI
    author='Alban Andrieu',
    author_email='alban.andrieu@free.fr',
    description='This is nabla_custom hooks package',
    long_description=open('README.md').read(),
    keywords='nabla hooks',
    url='https://github.com/AlbanAndrieu/nabla-hooks',
    project_urls={
        'Bug Tracker': 'https://github.com/AlbanAndrieu/nabla-hooks',
        'Documentation': 'https://github.com/AlbanAndrieu/nabla-hooks',
        'Source Code': 'https://github.com/AlbanAndrieu/nabla-hooks',
    },
    classifiers=[
        'Programming Language :: Python',
    ],

    entry_points={
        'console_scripts': [
            'nabla-hooks = hooks.get_msg:main',
        ],
    },

    # could also include long_description, download_url, etc.
)
