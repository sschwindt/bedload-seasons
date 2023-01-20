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


