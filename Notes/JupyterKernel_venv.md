# Elamparithi's Short notes
## _How to create Jupyter Kernel for python Virtual environment?_

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Jupiter notebook is important when coming to exploration. But to get your virtual environment with jupiter notebook. needs following steps.

- Create a Virtual Environment (using venv)
- Activate Virtual Environment
- Install the IPython Kernel
- Create a New Jupyter Kernel
- Deleting an Jupyter Kernel

## Create a Virtual Environment (using venv)
```sh
python -m venv myenv
```
## Activate Virtual Environment
```sh
.venv\Scripts\activate
```
## Install the IPython Kernel
```sh
python -m pip install ipykernel
```
## Create a New Jupyter Kernel
Ipython module is very important here to install.
```sh
python -m ipykernel install --user --name=myenv --display-name "Python (myenv)"
```
**command Break down**
 - `python -m ipykernel install`: This part of the command invokes the ipykernel module to install a new kernel.
 - `--user`: This flag indicates that the kernel will be installed for the current user, making it available only for your user account.
 - `--name=myenv`: This sets the name of the kernel to myenv. This is the name that will be used internally.
 - `--display-name "Python (myenv)"`: This sets the display name of the kernel as it appears in Jupyter Notebook's interface. You can customize this to something more descriptive if desired.

In Jupyter Notebook, when you create a new notebook or open an existing one, you can select your virtual environment kernel from the `Kernel` menu > `Change kernel` > `Python (myenv)` or from the dropdown list when creating a new notebook.

## Deleting an Jupyter Kernel
**For listing kernels in the Virtual Environment**
```sh
jupyter kernelspec list
```
**Delete the Kernel**
```sh
jupyter kernelspec uninstall myenv
```
