
Repository Structure
--------------------

The bedload-seasons repository holds the following structure (``HOME/``). Relevant files for running code and adapting fundamental arguments are **marked in bold**.

* CONTRIBUTING
* LICENSE
* README
* **bedload_base_stats.py makes boxplots with Kruskal-Wallis H (KWH) tests (p-values)**
* **plot_dataset.py calculates Spearman ranked correlations**
* **plot_histograms.py make histograms of numbers of measurements per variable category**
* data/
    + bedload-data.xlsx
    + bedload-data-valid-samplers.xlsx
    + readme-data.md
* pyBedLoad/
    + __init__.py
    + categorize.py
    + **config.py**
    + get_data.py
    + mor_fun.py
    + workbook_fun.py
    + missingno/ (modified fork of `missingno <https://github.com/ResidentMario/missingno>`_)
* docs/
    + codedocs.rst (sphinx-based parsing of Python scripts; reads script docstrings)
    + conf.py (ignore)
    + index.rst (this)
    + license.rst
    + setup.py
* environment.yml
* requirements.txt
* requirements-dev (ignore)
* setup.py (ignore)


