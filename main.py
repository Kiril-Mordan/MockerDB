from fastapi import FastAPI
from mocker_db import MockerDB, SentenceTransformerEmbedder
from conf.settings import MOCKER_SETUP_PARAMS
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# define datatypes
class Item(BaseModel):
    text: str

class InitializeParams(BaseModel):
    embedder_params: Optional[Dict[str, Any]] = None
    database_name: Optional[str] = None

class InsertItem(BaseModel):
    data: List[Dict[str, Any]]  # List of dictionaries to support various data structures
    var_for_embedding_name: str  # Variable name to be used for embedding
    embed: Optional[bool] = True  # Whether to embed the data
    database_name: Optional[str] = None

class SearchRequest(BaseModel):
    query: str
    database_name: Optional[str] = None
    search_results_n: Optional[int] = None
    filter_criteria: Optional[Dict[str, Any]] = None
    similarity_search_type: Optional[str] = None
    similarity_params: Optional[Dict[str, Any]] = None
    perform_similarity_search: Optional[bool] = None
    return_keys_list: Optional[List[str]] = None

class DeleteItem(BaseModel):
    filter_criteria: Dict[str, str]
    database_name: Optional[str] = None

class UpdateItem(BaseModel):
    filter_criteria: Dict[str, str]
    update_values: Dict[str, str]
    database_name: Optional[str] = None

class EmbeddingRequest(BaseModel):
    texts: List[str]
    embedding_model: Optional[str]

# start the app and activate mockerdb
app = FastAPI()
handlers = {}
handlers['default'] = MockerDB(**MOCKER_SETUP_PARAMS)


# endpoints
@app.get("/")
def read_root():
    return "Still alive!"

@app.get("/active_handlers")
def show_handlers():

    handler_names = [hn for hn in handlers]
    items_in_handlers = [len(handlers[hn].data.keys()) for hn in handlers]

    return {'handlers' : handler_names,
            'items' : items_in_handlers}

@app.post("/initialize")
def initialize_database(params: InitializeParams):
    global handlers  # Use global to modify the handler instance
    # Update the initialization parameters based on input
    init_params = MOCKER_SETUP_PARAMS.copy()  # Start with default setup parameters
    if params.embedder_params is not None:
        init_params["embedder_params"] = params.embedder_params
    if params.database_name is not None:
        init_params["file_path"] = f"./persist/{params.database_name}"  # Assuming the file path format
    # Reinitialize the handler with new parameters
    handlers[params.database_name] = MockerDB(**init_params)
    handlers[params.database_name].establish_connection()
    return {"message": "Database initialized with new parameters"}

@app.post("/insert")
def insert_data(insert_request: InsertItem):
    # Extract values from the request object
    values_list = insert_request.data
    var_for_embedding_name = insert_request.var_for_embedding_name
    embed = insert_request.embed

    if insert_request.database_name is None:
        insert_request.database_name = "default"

    # Call the insert_values method with the provided parameters
    handlers[insert_request.database_name].insert_values(values_list, var_for_embedding_name, embed)
    return {"message": "Data inserted successfully"}

@app.post("/search")
def search_data(search_request: SearchRequest):

    if search_request.database_name is None:
        search_request.database_name = "default"

    results = handlers[search_request.database_name].search_database(query=search_request.query,
         search_results_n=search_request.search_results_n,
         filter_criteria=search_request.filter_criteria,
         similarity_search_type=search_request.similarity_search_type,
         similarity_params=search_request.similarity_params,
         perform_similarity_search=search_request.perform_similarity_search,
        return_keys_list=search_request.return_keys_list
    )

    return {"results": results}

@app.post("/delete")
def delete_data(delete_request: DeleteItem):

    if delete_request.database_name is None:
        delete_request.database_name = "default"

    filter_criteria = delete_request.filter_criteria

    handlers[delete_request.database_name].remove_from_database(filter_criteria)
    return {"message": "Data deleted successfully"}

@app.post("/embed")
def embed_texts(embedding_request: EmbeddingRequest):

    embedding_params = MOCKER_SETUP_PARAMS['embedder_params']

    init_params = MOCKER_SETUP_PARAMS.copy()  # Start with default setup parameters
    # update model
    if embedding_request.embedding_model is not None:
        init_params["embedder_params"]['model_name_or_path'] = embedding_request.embedding_model
    # switch cache location
    init_params["file_path"] = f"./persist/cache_{init_params['embedder_params']['model_name_or_path']}"

    # create insert list of dicts
    insert = [{'text' : text} for text in embedding_request.texts]

    # Reinitialize the handler with new parameters
    handlers['cache'] = MockerDB(**init_params)
    handlers['cache'].establish_connection()

    # Use the embedder instance to get embeddings for the list of texts
    handlers['cache'].insert_values(values_dict_list=insert,
                            var_for_embedding_name='text',
                            embed=True)

    # Retrieve list of embeddings
    embeddings = [handlers['cache'].search_database(query = query,
                                          return_keys_list=['embedding'],
                                          search_results_n=1)[0]['embedding'].tolist() \
        for query in embedding_request.texts]

    return JSONResponse(content={"embeddings": embeddings})
