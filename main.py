# api
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
# database
from mocker_db import MockerDB
from conf.settings import MOCKER_SETUP_PARAMS, API_SETUP_PARAMS
# types
from utils.data_types import *
# managing memory
from utils.memory_management import check_and_offload_handlers
from pympler import asizeof
import gc

# start the app and activate mockerdb
app = FastAPI()
handlers = {}
handlers['default'] = MockerDB(**MOCKER_SETUP_PARAMS)



# endpoints
@app.get("/")
def read_root():
    return "Still alive!"

@app.get("/active_handlers",
         responses={
             200: {"description": "Returns a list of active handlers along with their item counts and memory usage.",
                   "content": {
                        "application/json": {
                            "example": {
                                "handlers": ["default", "test_db1"],
                                "items": [0, 103],
                                "memory_usage": [1.2714920043945312, 1.6513137817382812]
                            }
                        }
                    }}})
def show_handlers():

    handler_names = [hn for hn in handlers]
    items_in_handlers = [len(handlers[hn].data.keys()) for hn in handlers]
    memory_usage = [asizeof.asizeof(handlers[hn])/API_SETUP_PARAMS['memory_scaler_from_bytes'] for hn in handlers]

    return {
        'handlers': handler_names,
        'items': items_in_handlers,
        'memory_usage': memory_usage
    }

@app.post("/remove_handlers",
          responses={
            200: {"description": "Removes specified handlers from the application.",
                   "content": {
                        "application/json": {
                            "example": {
                                "message": "Removed handlers: handler1, handler2",
                                "not_found": ["handler3_not_found"]
                                }
                        }
                    }
                   },

            404: {
                "description": "One or more handlers not found.",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "Handlers not found: handler3_not_found"
                        }
                    }
                }}})
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

@app.post("/initialize", responses={
    200: {
        "description": "Database initialization response",
        "content": {
            "application/json": {
                "example": {"message": "Database initialized with new parameters"}
            }
        }
    }
})
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

@app.post("/insert", responses={
    200: {
        "description": "Successful insertion response",
        "content": {
            "application/json": {
                "example": {"message": "Data inserted successfully"}
            }
        }
    },
    400: {
        "description": "Invalid request",
        "content": {
            "application/json": {
                "example": {"detail": "Invalid data provided"}
            }
        }
    }
})
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

@app.post("/search", responses={
    200: {
        "description": "Search results based on query and criteria",
        "content": {
            "application/json": {
                "example": {
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
            }
        }
    }
})
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

@app.post("/delete", responses={
    200: {
        "description": "Confirmation of data deletion",
        "content": {
            "application/json": {
                "example": {"message": "Data deleted successfully"}
            }
        }
    }
})
def delete_data(delete_request: DeleteItem):

    if delete_request.database_name is None:
        delete_request.database_name = "default"

    filter_criteria = delete_request.filter_criteria

    handlers[delete_request.database_name].remove_from_database(filter_criteria)
    return {"message": "Data deleted successfully"}

@app.post("/embed", responses={
    200: {
        "description": "Generates embeddings for the provided list of texts.",
        "content": {
            "application/json": {
                "example": {
                    "embeddings": [
                        [0.06307613104581833, -0.012639996595680714, "...", 0.04296654835343361, 0.06654967367649078],
                        [0.023942897096276283, -0.03624798730015755, "...", 0.061928872019052505, 0.07419337332248688]
                    ]
                }
            }
        }
    }
})
def embed_texts(embedding_request: EmbeddingRequest):


    init_params = MOCKER_SETUP_PARAMS.copy()  # Start with default setup parameters
    # update model
    if embedding_request.embedding_model is not None:
        init_params["embedder_params"]['model_name_or_path'] = embedding_request.embedding_model
    # switch cache location
    init_params["file_path"] = f"./persist/cache_{init_params['embedder_params']['model_name_or_path'].replace('/','_')}"

    # create insert list of dicts
    insert = [{'text' : text} for text in embedding_request.texts]


    # Reinitialize the handler with new parameters
    cache_name = f"cache_{init_params['embedder_params']['model_name_or_path'].replace('/','_')}"

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
