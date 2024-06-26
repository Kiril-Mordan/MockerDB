# essential
import numpy as np
# api
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
# database
from mocker_db import MockerDB
from conf.settings import MOCKER_SETUP_PARAMS, API_SETUP_PARAMS, API_VERSION
# types
from utils.data_types import *
# endpoint descriptions
from utils.response_descriptions import *
# managing memory
from utils.memory_management import check_and_offload_handlers
from pympler import asizeof
import gc

# start the app and activate mockerdb
app = FastAPI(version=API_VERSION)
handlers = {}
handlers['default'] = MockerDB(**MOCKER_SETUP_PARAMS)


# Mount the MkDocs static files
app.mount("/mkdocs", StaticFiles(directory="mkdocs/site", html=True), name="mkdocs")

# endpoints
@app.get("/")
def read_root():
    return "Still alive!"

@app.get("/active_handlers",
         description= "Displays the current active handlers, the number of items they manage, and their memory usage in megabytes.",
         responses = ActivateHandlersDesc)
def show_handlers():

    handler_names = [hn for hn in handlers]
    items_in_handlers = [len(handlers[hn].data.keys()) for hn in handlers]
    memory_usage = [asizeof.asizeof(handlers[hn])/API_SETUP_PARAMS['memory_scaler_from_bytes'] \
        for hn in handlers]

    return {
        'handlers': handler_names,
        'items': items_in_handlers,
        'memory_usage': memory_usage
    }

@app.post("/remove_handlers",
          description = "Removes specified handlers from the application.",
          responses = RemoveHandlersDesc)
def remove_handlers(request: RemoveHandlersRequest):
    removed_handlers = []
    not_found_handlers = []

    for handler_name in request.handler_names:
        if handler_name in handlers:
            # Remove the handler
            del handlers[handler_name]
            removed_handlers.append(handler_name)
        else:
            not_found_handlers.append(handler_name)

    # Force garbage collection
    gc.collect()

    if not removed_handlers and not_found_handlers:
        raise HTTPException(status_code=404, detail=f"Handlers not found: {', '.join(not_found_handlers)}")

    return {"message": f"Removed handlers: {', '.join(removed_handlers)}",
            "not_found": not_found_handlers}

@app.post("/initialize",
          description = "Initializes the database with custom parameters.",
          responses = InitializeDesc)
def initialize_database(params: InitializeParams):
    global handlers  # Use global to modify the handler instance
    # Update the initialization parameters based on input
    init_params = MOCKER_SETUP_PARAMS.copy()  # Start with default setup parameters
    if params.embedder_params is not None:
        init_params["embedder_params"] = params.embedder_params
    if params.database_name is not None:
        init_params["file_path"] = f"./persist/mocker_{params.database_name}"  # Assuming the file path format
        init_params["embs_file_path"] = f"./persist/embs_{params.database_name}"
    # Reinitialize the handler with new parameters
    handlers[params.database_name] = MockerDB(**init_params)
    handlers[params.database_name].establish_connection()
    return {"message": "Database initialized with new parameters"}

@app.post("/insert",
          description = "Inserts data into the specified database.",
          responses = InsertDesc)
def insert_data(insert_request: InsertItem):

    # Extract values from the request object
    values_list = insert_request.data
    var_for_embedding_name = insert_request.var_for_embedding_name
    embed = insert_request.embed

    if insert_request.database_name is None:
        insert_request.database_name = "default"

    # Free up memory if needed
    check_and_offload_handlers(handlers = handlers,
                               allocated_bytes = API_SETUP_PARAMS['allocated_mb']*1024**2,
                               exception_handlers = [insert_request.database_name],
                               insert_size_bytes = asizeof.asizeof(values_list))

    # Call the insert_values method with the provided parameters
    handlers[insert_request.database_name].insert_values(values_list, var_for_embedding_name, embed)
    return {"message": "Data inserted successfully"}

@app.post("/search",
          description = "Searches the database based on the provided query and criteria.",
          responses = SearchDesc)
def search_data(search_request: SearchRequest):

    if search_request.database_name is None:
        search_request.database_name = "default"

    results = handlers[search_request.database_name].search_database(
        query=search_request.query,
        search_results_n=search_request.search_results_n,
        filter_criteria=search_request.filter_criteria,
        similarity_search_type=search_request.similarity_search_type,
        similarity_params=search_request.similarity_params,
        perform_similarity_search=search_request.perform_similarity_search,
        return_keys_list=search_request.return_keys_list
    )

    # Ensure all numpy arrays are converted to lists
    json_compatible_results = []
    for result in results:
        processed_result = {}
        for key, value in result.items():
            if isinstance(value, np.ndarray):
                processed_result[key] = value.tolist()  # Convert numpy arrays to lists
            else:
                processed_result[key] = value
        json_compatible_results.append(processed_result)

    return {"results": json_compatible_results}

@app.post("/delete",
          description = "Deletes data from the database based on filter criteria.",
          responses = DeleteDesc)
def delete_data(delete_request: DeleteItem):

    if delete_request.database_name is None:
        delete_request.database_name = "default"

    filter_criteria = delete_request.filter_criteria

    if filter_criteria is None:
        handlers[delete_request.database_name].flush_database()
    else:
        handlers[delete_request.database_name].remove_from_database(filter_criteria)
    return {"message": "Data deleted successfully"}

@app.post("/embed",
          description = "Generates embeddings for the provided list of texts.",
          responses = EmbedDesc)
def embed_texts(embedding_request: EmbeddingRequest):


    init_params = MOCKER_SETUP_PARAMS.copy()  # Start with default setup parameters
    # update model
    if embedding_request.embedding_model is not None:
        init_params["embedder_params"]['model_name_or_path'] = embedding_request.embedding_model
    # switch cache location
    init_params["file_path"] = f"./persist/cache_mocker_{init_params['embedder_params']['model_name_or_path'].replace('/','_')}"
    init_params["embs_file_path"] = f"./persist/cache_embs_{init_params['embedder_params']['model_name_or_path'].replace('/','_')}"

    # create insert list of dicts
    insert = [{'text' : text} for text in embedding_request.texts]


    # Reinitialize the handler with new parameters
    cache_name = f"cache_mocker_{init_params['embedder_params']['model_name_or_path'].replace('/','_')}"

    # Free up memory if needed
    check_and_offload_handlers(handlers = handlers,
                               allocated_bytes = API_SETUP_PARAMS['allocated_mb']*1024**2,
                               exception_handlers = [cache_name],
                               insert_size_bytes = asizeof.asizeof(insert))

    if cache_name not in [hn for hn in handlers]:

        handlers[cache_name] = MockerDB(**init_params)
        handlers[cache_name].establish_connection()

    # Use the embedder instance to get embeddings for the list of texts
    handlers[cache_name].insert_values(values_dict_list=insert,
                                        var_for_embedding_name='text',
                                        embed=True)

    # Retrieve list of embeddings
    embeddings = [handlers[cache_name].search_database(query = query,
                                          return_keys_list=['embedding'],
                                          search_results_n=1)[0]['embedding'].tolist() \
        for query in embedding_request.texts]

    return JSONResponse(content={"embeddings": embeddings})
