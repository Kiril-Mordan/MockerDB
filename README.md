# MockerDB

This is a crude implementation of a vector database-like solution in python, inspired by simplicity of Redis HASH.
Its goal is be usable in development in particulr using complex and custom searching strategies.

Even though it by no means aims to replace any propper vector database, nevertheless it could be
usefull as an ephemeral vector database.

Its purpuse is to uefull for aplications that either don't need to access previouly stored data, can get away with accessing only small portion of it (fits into RAM) or do not need to persist at all.

The source code for the python tool itself is available in the reusables repo. This repository is meant to create deployment ready version that one could realistically use to make API with.

## Install package from pypi

```
pip install mocker-db
```

## Run locally

```
uvicorn main:app --reload
```