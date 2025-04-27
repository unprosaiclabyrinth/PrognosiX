# How to run the Prognosix dashboard

### If this is the **first** time you’ve cloned the repo  
*(you won’t have the environment yet)*

```bash
conda env create -f environment.yml

### If you already have the `prognosix-ds` environment

```bash
conda activate prognosix-ds
conda env update -f environment.yml --prune


# start both the backend (Voilà) and the React dev server

```bash
./start.sh

# to go out of the conda enviroment

```bash
conda deactivate
