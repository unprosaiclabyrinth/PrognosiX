# How to run the PrognosiX dashboard

### If this is the **first** time you’ve cloned the repo:
*(you won’t have the environment yet)*

```bash
conda env create -f environment.yml
```

### If you already have the `prognosix-ds` environment:

```bash
conda activate prognosix-ds
conda env update -f environment.yml --prune
```


### Start both the backend (Voilà) and the React dev server:

```bash
./start.sh
```

### To go out of the conda enviroment:

```bash
conda deactivate
```
