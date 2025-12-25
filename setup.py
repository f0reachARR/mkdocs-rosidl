from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mkdocs-rosidl",
    version="0.1.0",
    author="mkdocs-rosidl contributors",
    description="MkDocs plugin for generating ROS2 interface documentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/f0reachARR/mkdocs-rosidl",
    packages=find_packages(),
    package_data={
        "mkdocs_rosidl": ["templates/*"],
    },
    install_requires=[
        "mkdocs>=1.0",
        "jinja2>=2.11",
        "rosidl-runtime-py",
        "rosidl-parser",
        "ament-index-python",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    entry_points={
        "mkdocs.plugins": [
            "rosidl = mkdocs_rosidl.plugin:RosidlPlugin",
        ]
    },
)
