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

