import setuptools

setuptools.setup(
    name = "umapbrowser",
    version = "0.0.1",
    author = "Phylliida",
    author_email = "phylliidadev@gmail.com",
    description = "Simple UMAP Webui browser",
    url = "https://github.com/Phylliida/umapbrowser",
    project_urls = {
        "Bug Tracker": "https://github.com/Phylliida/umapbrowser/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages = setuptools.find_packages(),
    python_requires = ">=3.6",
    install_requires = ["setuptools"]
)
