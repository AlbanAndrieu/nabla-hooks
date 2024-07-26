# pylint: skip-file
import os

from setuptools import find_packages
from setuptools import setup

# import hooks
# from hooks._version import get_versions
# import versioneer

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="nabla-hooks",
    # version=hooks.__version__,
    # version=get_versions()['version'],
    # version="1.0.5",
    version=os.getenv("PACKAGE_VERSION"),
    # version=versioneer.get_version(),
    # cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    # scripts=["hooks/get_msg.py"],
    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    setup_requires="setuptools-pipfile",
    # install_requires=["docutils>=0.3", "jira>=3.0.1", "termcolor>=1.1.0"],
    # install_requires=requirements,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.txt", "*.rst"],
        # And include any *.msg files found in the "hooks" package, too:
        "hooks": ["*.msg"],
    },
    # metadata to display on PyPI
    author="Alban Andrieu",
    author_email="alban.andrieu@free.fr",
    description="This is nabla_custom hooks package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="nabla hooks",
    url="https://github.com/AlbanAndrieu/nabla-hooks",
    project_urls={
        "Bug Tracker": "https://github.com/AlbanAndrieu/nabla-hooks",
        "Documentation": "https://github.com/AlbanAndrieu/nabla-hooks",
        "Source Code": "https://github.com/AlbanAndrieu/nabla-hooks",
    },
    classifiers=[
        "Programming Language :: Python",
    ],
    entry_points={
        "console_scripts": [
            "nabla-hooks = hooks.get_msg:main",
        ],
    },
    # could also include long_description, download_url, etc.
)
