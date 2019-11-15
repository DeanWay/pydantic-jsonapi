from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pydantic_jsonapi",
    version="0.9.0",
    author="Dean Way",
    description="an implementation of JSON:api using pydantic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DeanWay/pydantic-jsonapi",
    packages=['pydantic_jsonapi'],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pydantic>=0.32.2',
        'typing-extensions>=3.7.4'
    ],
    python_requires='>=3.7',
)
