import setuptools
import tgmi

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tgmi",
    version=tgmi.__version__,
    author="h3r0cybersec",
    author_email="h3r0cybersec@protonmail.com",
    description="Gemini Protocol Server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/h3r0cybersec/tiny-gemini",
    project_urls={
        "Bug Tracker": "https://github.com/h3r0cybersec/tiny-gemini/issues",
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Natural Language :: Italian"
    ],
    package_data={"tgmi": ["*.crt", "*.key"]},
    packages=["tgmi", "tgmi/core", "tgmi/toolbox"],
    python_requires=">=3.8"
)
