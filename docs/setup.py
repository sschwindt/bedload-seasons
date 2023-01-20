from setuptools import setup, find_packages
from pathlib import Path


lines = Path(".").joinpath("__init__.py")
version = "1.0.0"
for line in lines.read_text().split("\n"):
    if line.startswith("__version__ ="):
        version = line.split(" = ")[-1].strip('"')
        break


setup(
    name="BedloadSeasons",
    version=version,
    python_requires=">=3.6",
    author="sschwindt, beatriznegreiros",
    author_email="sebastian.schwindt@iws.uni-stuttgart.de",
    url="https://github.com/sschwindt/bedload-seasons",
    project_urls={
        "Documentation": "https://bedload-seasons.readthedocs.io/",
        "Funding": "https://hydro-informatics.com/",
        "Source": "https://github.com/sschwindt/bedload-seasons",
    },
    # this should be a whitespace separated string of keywords, not a list
    keywords="bedload, sediment transport, seasonality, timing, fall, spring, summer, winter, generalized extreme value, Weibull, snowmelt, glacier, climate change",
    description="Codes and data for analysis of enriched bedload dataset supporting manuscript findings",
    license="BSD License",
    long_description=Path("./README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "pyyaml",
        "docutils>=0.15",
        "sphinx",
        "click",
        "pydata-sphinx-theme~=0.4.1",
        "beautifulsoup4",
        'importlib-resources~=3.0.0; python_version < "3.7"',
    ],
    # dependency_links=[
    #     "git+https://github.com/ecohydraulics/flusstools-pckg#egg=flusstools-pckg"
    # ],
    include_package_data=True,
    extras_require={
        "code_style": ["pre-commit~=2.7.0"],
        "sphinx": [
            "folium",
            "numpy",
            "matplotlib",
            "ipywidgets",
            "openpyxl",
            "pandas",
            "nbclient",
            "myst-nb~=0.10.1",
            "sphinx-togglebutton>=0.2.1",
            "sphinx-copybutton",
            "seaborn",
            "sphinxcontrib-bibtex",
            "sphinx-thebe",
            "ablog~=0.10.11",
        ],
        "testing": [
            "myst_nb~=0.10.1",
            "sphinx_thebe",
            "coverage",
            "pytest~=6.0.1",
            "pytest-cov",
            "pytest-regressions~=2.0.1",
        ],
        "live-dev": ["sphinx-autobuild", "web-compile~=0.2.1"],
    },
    entry_points={
        "sphinx.html_themes": ["sphinx_book_theme = sphinx_book_theme"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 4 - Beta",
    ],
)
