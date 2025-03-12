"""
Setup script for Integrity Assistant
"""
from setuptools import setup, find_packages
import os

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="integrity-assistant",
    version="1.0.2",
    description="Intelligent digital teammate with contextual awareness",
    author="Integrity Team",
    author_email="support@integrity.ai",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'integrity-assistant=integrity_assistant.main:main',
        ],
    },
    package_data={
        'integrity_assistant': ['.env.template'],
    },
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
    ],
) 