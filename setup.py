"""
Setup script for Smart Function Recommender.
"""

from setuptools import setup, find_packages
import os

# Read README for long description
readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
long_description = ""
if os.path.exists(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='smart-func',
    version='0.1.0',
    description='Smart Function Recommender - Convert natural language to reusable code snippets',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/smart-func',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'smart_func': ['database.json'],
    },
    install_requires=[
        # No external dependencies for basic functionality
        # Add optional dependencies for future enhancements:
        # 'spacy>=3.0.0',  # For advanced NLP
        # 'transformers>=4.0.0',  # For AI-powered generation
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'smart-func=smart_func.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='developer-tools code-snippets nlp function-recommender productivity',
)
