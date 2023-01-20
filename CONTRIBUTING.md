## Basics

Make sure to understand the basics of building a PyPI package ([example tutorial](https://towardsdatascience.com/build-your-first-open-source-python-project-53471c9942a7)).

## Requirements (PyPI)

* Create a [TestPyPI](https://test.pypi.org/) account
* Create a [PyPI](https://pypi.org/) account
* Install requirements for developers (in *Terminal*)</br>`pip install -r requirements_dev.txt`

## Build and push test version

SHORT VERSION:

```
python setup.py develop
twine upload dist/*
```

TEST:

```
python -m venv test_env
source test_env/bin/activate
pip install TKEanalyst
import TKEanalyst
```


Before adding a new version of *TKEanalyst*, please inform about the severity and version numbering semantics on [python.org](https://www.python.org/dev/peps/pep-0440/).

1. `cd` to your local *TKEanalyst* folder (in *Terminal*)
1. Create *TKEanalyst* locally
	* Linux (in Terminal): `sudo python setup.py sdist bdist_wheel`
	* Windows (in Anaconda Prompt with flussenv): `python setup.py sdist bdist_wheel`
1. Upload the (new version) to TestPyPI (with your TestPyPI account):
	* `twine upload --skip-existing --repository-url https://test.pypi.org/legacy/ dist/*`
	* If any error occurs, fix it and rebuild the package (previous step).
1. Create a new environment and activate it to test if the upload and installation work
    * On *Linux*:</br>`python -m venv test_env`</br>`source test_env/bin/activate`
    * On *Windows* (with Anaconda):</br>`conda activate TKEanalyst-test`
1. Install the new version of *TKEanalyst* in the environment:
	* `pip install -i https://test.pypi.org/simple/ TKEanalyst`
1. Launch python and import *TKEanalyst*:
	* `python`
	* `>>> import TKEanalyst`

## Push to PyPI

If you could build and install the test version successfully, you can push the new version to PyPI. **Make sure to increase the `VERSION="major.minor.micro" in *ROOT/setup.py***. Then push to PyPI (with your PyPI account):

`twine upload dist/*`

## Create a new release on GitHub

Please note that we are currently still in the *growing* phase of *TKEanalyst*. Since *version 0.2*, login at github.com and create a new *release* after merging branches.
