from setuptools import setup, find_packages

setup(
    name="speakeasy",
    version="1.0.0",
    author="Ваше имя",
    author_email="ваш.email@example.com",
    description="Приложение для изучения иностранных слов",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ваш-проект",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi==0.115.6",
        "uvicorn==0.23.0",
        "pandas==2.2.3",
        "numpy==2.2.0",
        "pytest==8.3.4",
        "colorama==0.4.6",
        "tabulate==0.9.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
