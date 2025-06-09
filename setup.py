from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="terminal-typist",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A MonkeyType-like typing speed test for the terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/terminal-typist",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Games/Entertainment",
    ],
    python_requires=">=3.6",
    install_requires=[
        "windows-curses; platform_system=='Windows'",
    ],
    entry_points={
        "console_scripts": [
            "typist=terminal_typist.main:main",
            "terminal-type=terminal_typist.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "terminal_typist": ["data/*.txt"],
    },
)
