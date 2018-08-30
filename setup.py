from setuptools import setup

long_description = open('README.md').read()

setup(
    name="pycereal",
    version='1.0',
    packages=["cereal"],
    include_package_data=True,
    description="A simple object and Django model JSON serializer",
    url="https://github.com/istrategylabs/cereal",
    author="Jeremy Carbaugh",
    author_email="jeremy@isl.co",
    license='BSD',
    long_description=long_description,
    long_description_content_type="text/markdown",
    platforms=["any"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
