from setuptools import setup, find_packages
import os

# Read version from a file
def get_version():
    version_file = os.path.join(os.path.dirname(__file__), "VERSION")
    if os.path.exists(version_file):
        with open(version_file) as f:
            return f.read().strip()
    return "1.0.0"  # Default version if file doesn't exist

# Read requirements
def get_requirements():
    with open("requirements.txt") as f:
        return [line.split('#')[0].strip() for line in f if line.strip() and not line.startswith('#')]

# Extract dev requirements
def get_dev_requirements():
    with open("requirements.txt") as f:
        return [line.split('#')[0].strip() for line in f if 'extra == \'dev\'' in line]

setup(
    name="muscle5-sequence-alignment-tool",
    version=get_version(),
    description="A Python interface for MUSCLE5 with visualization and conservation analysis",
    author="Taher Akbari Saeed",
    author_email="taherakbarisaeed@gmail.com",
    url="https://github.com/tayden1990/bioinformatic-python-alignment-muscle5",
    packages=find_packages(),
    include_package_data=True,
    install_requires=get_requirements(),
    extras_require={
        'dev': get_dev_requirements(),
    },
    entry_points={
        'console_scripts': [
            'muscle5-tool=run_app:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)
