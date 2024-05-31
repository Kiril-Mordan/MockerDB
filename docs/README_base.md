# MockerDB

<a><img src="https://github.com/Kiril-Mordan/MockerDB/blob/main/docs/mocker_db_logo.png" width="35%" height="35%" align="right" /></a>

This is a crude implementation of a vector database-like solution in python.
Currently its goal is to simplyfy usecases that require extensive use of open source embeddings from [Sentence-Transformers](https://www.sbert.net/docs/pretrained_models.html), while being simple and flexibale enough to add and test custom searching strategies.

Even though it by no means aims to replace any propper vector database, nevertheless it could be
usefull as an ephemeral vector database. Limiting persisting capabilities are available and will be expanded in time.

## Run locally

Use underlying python package from [pypi](https://pypi.org/project/mocker-db/):
```
pip install mocker-db
```


Run API locally:
```
git clone https://github.com/Kiril-Mordan/MockerDB.git
cd MockerDB
uvicorn main:app --port 8000
```

Access localhost at http://127.0.0.1:8000

## Run from pre-built Docker image:

```
docker pull kyriosskia/mocker-db:latest
docker run -p 8000:8080 kyriosskia/mocker-db:latest
```

then access at http://localhost:8000

