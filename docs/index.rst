.. documentation parent file.


Bedload Seasons
===============

This is the documentation of supplemental materials for a scientific study on the time dimension of bedload.


.. admonition:: How to cite FlussTools

    If our study and codes helped you to accomplish your work, we won't ask you for a coffee, but to cite and spread the utility of our code - Thank you!

    .. code::

        @software{bedload_seasons_2023,
                  author       = {Sebastian Schwindt and
                                  Beatriz Negreiros},
                  title        = {Bedload Seasons - Codes and Data},
                  year         = 2023,
                  publisher    = {GitHub \& Center for Open Science (OSF)},
                  version      = {v1},
                  doi          = {10.17605/OSF.IO/3ZMKN},
                  url          = {https://doi.org/10.17605/OSF.IO/3ZMKN}
                }



.. note::

    This documentation is also as available as `style-adapted PDF <https://bedload-seasons.readthedocs.io/_/downloads/en/latest/pdf/>`_.


Requirements
------------

*Time requirement: 5-10 min.*

To get the code running, the following software is needed and their installation instructions are provided below:

.. code::

    fitter>=1.5.2
    matplotlib>=3.1.2
    numpy>=1.17.4
    openpyxl>=3.0.9
    pandas>=1.3.5
    scikit_learn>=1.2.0
    scikit_posthocs>=0.7.0
    scipy>=1.7.3
    seaborn>=0.12.2
    statannotations>=0.5.0
    statsmodels>=0.13.5


.. tip:: New to Python?

    Start with downloading and installing the latest version of `Anaconda Python <https://www.anaconda.com/products/individual>`_.  Alternatively, downloading and installing a pure `Python <https://www.python.org/downloads/>`_ interpreter will also work. Detailed information about installing Python is available in the `Anaconda Docs <https://docs.continuum.io/anaconda/install/windows/>`_ and at `hydro-informatics.com/python-basics <https://hydro-informatics.com/python-basics/pyinstall.html#https://hydro-informatics.com/python-basics/pyinstall.html#conda-env>`_.

To install the requirements in a new conda environment, download our specific `environment.yml <https://github.com/sschwindt/bedload-seasons/raw/main/environment.yml>`_. Then open Anaconda Prompt (e.g., click on the Windows icon, tap ``anaconda prompt``, and hit enter``). In Anaconda Prompt, enter the following command sequence to install the libraries in the **base** environment. The installation may take a while depending on your internet speed.

.. code-block::

    conda env create -f environment.yml

This will have created a new conda environment named ``bed-data-env``. After the installation, activate the environment:

.. code-block::

    conda activate bed-data-env

If you are struggling with the dark window and blinking cursor of Anaconda Prompt, worry not. You can also pip-install the requirements following the instructions on `hydro-informatics.com for virtual environments <https://hydro-informatics.com/python-basics/pyinstall.html#pip-and-venv-linux-preference>`_.



Get Code and Data
-----------------

Open any git-able Terminal (get git at `https://git-scm.com <https://git-scm.com/>`_), and enter:

.. code::

    https://github.com/sschwindt/bedload-seasons.git

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


Usage
-----

Configure
+++++++++

The ``pyBedLoad/config.py`` script imports all relevant packages an can be used to:

* modify constants, such as grain or water density
* switch between using all samplers in ``data/bedload-data.xlsx`` or comparable samplers only (default) in ``data/bedload-data-valid-samplers.xlsx``

In addition, modifications to plot properties can be made in  ``pyBedLoad/mor_fun.py`` (for *morphology fun* or *more fun* - choose your favorite), which provides the core functions for boxplots including Kruskal-Wallis H (KWH) tests, dataset completeness (application not explained in the docs), and global Spearman rank correlation matrix.

Global Correlations
+++++++++++++++++++

To create a plot of the Spearman ranked correlation matrix shown in the manuscript, run the following command in an active Python environment (make sure to be in the repository ``HOME/``):

.. code-block::

    python plot_correlations.py

After a successful run, this script will have saved a plot of the correlation matrix in ``HOME/figures/`` with the name ``dataset-corr-spearman.png``. The code also creates a workbook correlation with the correlation matrix (``HOME/corr-spearman.xlsx``). Note that we hard-coded the Spearman rank correlation method in ``pyBedLoad/mor_fun.py`` (line 323 defining ``corr_mat = df.corr(method='spearman')`` -- sorry for the laziness), which can also be changed to ``pearson`` or ``kendall``.

Boxplots and (KWH) tests
++++++++++++++++++++++++

To create the boxplots with with Kruskal-Wallis H (KWH) tests shown in the manuscript and supplemental material, run the following command in an active Python environment (make sure to be in the repository ``HOME/``):

.. code-block::

    python bedload_base_stats.py

Running this script can take a couple of minutes on a slow computer, create logfiles with information on the fitting process, and boxplot-figures in the directory ``HOME/figures/``.

Histograms of Variable Frequency
++++++++++++++++++++++++++++++++

To re-make the histogram-like frequency plots showing the number of measurements per category in the supplemental material, run the following command in an active Python environment (make sure to be in the repository ``HOME/``):

.. code-block::

    python plot_histograms.py

This script will have created multiple figures showing the histograms in the directory ``HOME/figures/histograms/``.

.. toctree::
    :hidden:
    :maxdepth: 2

    Bedload Season Analyst <self>

.. toctree::
    :hidden:

    Code Documentation <codedocs>

.. toctree::
    :hidden:

    License <license>


