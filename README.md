# MockerDB

<a><img src="https://github.com/Kiril-Mordan/MockerDB/raw/main/docs/mocker_db_logo.png" width="35%" height="35%" align="right" /></a>

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

# API Endpoints


### Read Root

- **Method**: GET
- **URL**: `/`
- **Description**: No description provided.
- **Response 200**: Successful Response
  ```json
  {}
  ```


### Show Handlers

- **Method**: GET
- **URL**: `/active_handlers`
- **Description**: Displays the current active handlers, the number of items they manage, and their memory usage in megabytes.
- **Response 200**: A list of active handlers along with their item counts and memory usage.
  ```json
  {
    "handlers": [
      "default",
      "test_db1"
    ],
    "items": [
      0,
      103
    ],
    "memory_usage": [
      1.2714920043945312,
      1.6513137817382812
    ]
  }
  ```


### Remove Handlers

- **Method**: POST
- **URL**: `/remove_handlers`
- **Description**: Removes specified handlers from the application.
- **Request Body**:
  ```json
  {
    "handler_names": [
      "handler1",
      "handler2"
    ]
  }
  ```
- **Response 200**: Specified handlers are removed from the application.
  ```json
  {
    "message": "Removed handlers: handler1, handler2",
    "not_found": [
      "handler3_not_found"
    ]
  }
  ```

- **Response 404**: One or more handlers not found.
  ```json
  {
    "detail": "Handlers not found: handler3_not_found"
  }
  ```

- **Response 422**: Validation Error
  ```json
  {}
  ```


### Initialize Database

- **Method**: POST
- **URL**: `/initialize`
- **Description**: Initializes the database with custom parameters.
- **Request Body**:
  ```json
  {
    "database_name": "custom_db_name",
    "embedder_params": {
      "model_name_or_path": "intfloat/multilingual-e5-base",
      "processing_type": "batch",
      "tbatch_size": 64
    }
  }
  ```
- **Response 200**: Database initialization response
  ```json
  {
    "message": "Database initialized with new parameters"
  }
  ```

- **Response 422**: Validation Error
  ```json
  {}
  ```


### Insert Data

- **Method**: POST
- **URL**: `/insert`
- **Description**: Inserts data into the specified database.
- **Request Body**:
  ```json
  {
    "data": [
      {
        "other_field": "Additional data",
        "text": "Example text 1"
      },
      {
        "other_field": "Additional data",
        "text": "Example text 2"
      }
    ],
    "var_for_embedding_name": "text",
    "embed": true,
    "database_name": "custom_db_name"
  }
  ```
- **Response 200**: Successful insertion response
  ```json
  {
    "message": "Data inserted successfully"
  }
  ```

- **Response 400**: Invalid request
  ```json
  {
    "detail": "Invalid data provided"
  }
  ```

- **Response 422**: Validation Error
  ```json
  {}
  ```


### Search Data

- **Method**: POST
- **URL**: `/search`
- **Description**: Searches the database based on the provided query and criteria.
- **Request Body**:
  ```json
  {
    "query": "example search query",
    "database_name": "custom_db_name",
    "search_results_n": 3,
    "filter_criteria": {
      "other_field": "Additional data 1"
    },
    "similarity_search_type": "linear",
    "similarity_params": {
      "space": "cosine"
    },
    "perform_similarity_search": true,
    "return_keys_list": [
      "text",
      "other_field"
    ]
  }
  ```
- **Response 200**: Searched results from selected database.
  ```json
  {
    "results": [
      {
        "text": "Short. Variation 37: Short.",
        "other_field": "Additional data 1"
      },
      {
        "text": "The quick brown fox jumps over the lazy dog. Variation 38: the dog. quick brown lazy The fox jumps over",
        "other_field": "Additional data 1"
      },
      {
        "text": "The quick brown fox jumps over the lazy dog. Variation 39: over lazy the jumps brown quick The dog. fox",
        "other_field": "Additional data 1"
      }
    ]
  }
  ```

- **Response 422**: Validation Error
  ```json
  {}
  ```


### Delete Data

- **Method**: POST
- **URL**: `/delete`
- **Description**: Deletes data from the database based on filter criteria.
- **Request Body**:
  ```json
  {
    "database_name": "custom_db_name",
    "filter_criteria": {
      "other_field": "Additional data 1"
    }
  }
  ```
- **Response 200**: Confirmation of data deletion
  ```json
  {
    "message": "Data deleted successfully"
  }
  ```

- **Response 422**: Validation Error
  ```json
  {}
  ```


### Embed Texts

- **Method**: POST
- **URL**: `/embed`
- **Description**: Generates embeddings for the provided list of texts.
- **Request Body**:
  ```json
  {
    "texts": [
      "Short. Variation 1: Short.",
      "Another medium-length example, aiming to test the variability in processing different lengths of text inputs. Variation 2: processing lengths medium-length example, in inputs. to variability aiming test of text different the Another"
    ],
    "embedding_model": "intfloat/multilingual-e5-small"
  }
  ```
- **Response 200**: A list of embeddings for each of provided text elements.
  ```json
  {
    "embeddings": [
      [
        0.06307613104581833,
        -0.012639996595680714,
        "...",
        0.04296654835343361,
        0.06654967367649078
      ],
      [
        0.023942897096276283,
        -0.03624798730015755,
        "...",
        0.061928872019052505,
        0.07419337332248688
      ]
    ]
  }
  ```

- **Response 422**: Validation Error
  ```json
  {}
  ```

