from setuptools import setup, find_packages

setup(
    name="learn-and-speak-pro",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask",
        "pytest"
    ],
)
