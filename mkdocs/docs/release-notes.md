# Release notes

### 0.1.2

    - initital cli interface that allows to clone code from api version of mocker and run it

### 0.1.1

    - initial MockerConnect for using MockerDB API

### 0.0.12

    -  bugfix for similarity search through partly embedded data

### 0.0.11

    - more advanced filtering

### 0.0.10

    - fix for search without embeddings

### 0.0.6

    - fix for embedding storage

### 0.0.5

    - initial implementation of separate caching store for embeddings

### 0.0.4

    - updating hnswlib 0.7.0 -> 0.8.0 to fix vulnerabilities issue

    - fixing a bug with resetting mocker inner state properly after search

### 0.0.3

    - slightly improving logic of embedding with batches in parallel for sentence transformer embedder (default embedder)

    - updating desciption

### 0.0.2

    - better error handling in situations when data was not found with applied filters

### 0.0.1

    - initial version of MockerDB package that evolved from mock classes from redis into a standalone solution