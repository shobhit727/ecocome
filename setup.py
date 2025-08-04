from setuptools import setup, find_packages

setup(
    name="market",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "websockets",
        "httpx",
        "pytest",
    ],
)
