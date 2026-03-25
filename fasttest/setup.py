#############################################
# File Name: setup.py
# Created Time: 2024-5-1
#############################################

import sys
import setuptools

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

info = sys.version_info
requires = [
    'colorama',
    'PyYAML',
    'jinja2',
    'playwright',
    'Faker',
    'pyperclip',
    'python-dotenv'
]
setuptools.setup(
    name="xffasttest",
    version="1.0.0",
    author="IMJIE",
    author_email="imjie@outlook.com",
    keywords=['xffasttest', 'playwright', 'WEB自动化'],
    description="playwright自动化框架",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jodeee/xffasttest",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'xffasttest/runner':['resource/*']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.8',
    install_requires=requires,
    entry_points={
        'console_scripts':[
            'xffasttest = xffasttest.main:main'
        ]
    }
)