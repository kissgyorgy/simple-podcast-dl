from setuptools import setup

# fmt: off
install_requires = [
    "lxml",
    "requests",
]

console_scripts = [
    "podcast-dl = podcast_dl:main",
]

classifiers = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
]
# fmt: on

setup(
    name="podcast-dl",
    version="0.2",
    description="Podcast downloader",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=classifiers,
    keywords="podcasts",
    author="Kiss György",
    author_email="kissgyorgy@me.com",
    url="https://github.com/kissgyorgy/podcast-dl",
    license="MIT",
    py_modules=["podcast_dl"],
    install_requires=install_requires,
    tests_require=["pytest", "pytest-sugar"],
    entry_points={"console_scripts": console_scripts},
)
