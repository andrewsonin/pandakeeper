from setuptools import setup, find_packages
from toml import load as load_toml
from typing import Tuple
from pathlib import Path


def extract_author_and_email(pyproject_entry: str) -> Tuple[str, str]:
    author, author_email = pyproject_entry.split('<')
    author = author.strip()
    author_email = author_email.replace('>', '').strip()
    return author, author_email


PROJECT_DIR = Path(__file__).resolve().parent

with open(PROJECT_DIR / 'LICENSE', 'r') as f:
    LICENCE = f.read()

with open(PROJECT_DIR / 'README.md', 'r') as f:
    README = f.read()

pyproject_info = load_toml(PROJECT_DIR / 'pyproject.toml')['tool']['poetry']
author, author_email = extract_author_and_email(pyproject_info['authors'][0])

setup(
    name=pyproject_info['name'],
    version=pyproject_info['version'],
    description=pyproject_info['description'],
    long_description=README,
    author=author,
    author_email=author_email,
    url='https://github.com/andrewsonin/pandakeeper',
    license=LICENCE,
    packages=find_packages(exclude=('tests', 'docs'))
)
