import setuptools

with open("README.md", "r") as doc:
    long_description = doc.read()

setuptools.setup(
    name="example-pkg-jobveldhuis",
    version="0.0.1",
    author="Job Veldhuis",
    author_email="job@baukefrederik.me",
    description="Python wrapper for qr-code-generator.com API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/jobveldhuis/qr-code-generator-wrapper',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
