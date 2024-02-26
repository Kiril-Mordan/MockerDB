
# types
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


# define datatypes
class Item(BaseModel):
    text: str

class InitializeParams(BaseModel):
    database_name: Optional[str] = Field(default=None, example="custom_db_name")
    embedder_params: Optional[Dict[str, Any]] = Field(default=None, example={
        "model_name_or_path": "intfloat/multilingual-e5-base",
        "tbatch_size": 64,
        "processing_type": "batch"
    })

class InsertItem(BaseModel):
    data: List[Dict[str, Any]] = Field(
        ...,
        example=[
            {"text": "Example text 1", "other_field": "Additional data"},
            {"text": "Example text 2", "other_field": "Additional data"}
        ]
    )
    var_for_embedding_name: str = Field(..., example="text")
    embed: Optional[bool] = Field(default=True, example=True)
    database_name: Optional[str] = Field(default=None, example="custom_db_name")

class SearchRequest(BaseModel):
    query: str = Field(..., example="example search query")
    database_name: Optional[str] = Field(default=None, example="custom_db_name")
    search_results_n: Optional[int] = Field(default=None, example=3)
    filter_criteria: Optional[Dict[str, Any]] = Field(default=None, example={"other_field": "Additional data 1"})
    similarity_search_type: Optional[str] = Field(default=None, example="linear")
    similarity_params: Optional[Dict[str, Any]] = Field(default=None, example={"space": "cosine"})
    perform_similarity_search: Optional[bool] = Field(default=None, example=True)
    return_keys_list: Optional[List[str]] = Field(default=None, example=["text", "other_field"])

class DeleteItem(BaseModel):
    database_name: Optional[str] = Field(default=None, example="custom_db_name")
    filter_criteria: Dict[str, str] = Field(..., example={"other_field": "Additional data 1"})

class UpdateItem(BaseModel):
    filter_criteria: Dict[str, str]
    update_values: Dict[str, str]
    database_name: Optional[str] = None

class EmbeddingRequest(BaseModel):
    texts: List[str] = Field(..., example=["Short. Variation 1: Short.",
                                           "Another medium-length example, aiming to test the variability in processing different lengths of text inputs. Variation 2: processing lengths medium-length example, in inputs. to variability aiming test of text different the Another"])
    embedding_model: Optional[str] = Field(default="intfloat/multilingual-e5-small", example="intfloat/multilingual-e5-small")

class RemoveHandlersRequest(BaseModel):
    handler_names: List[str] = Field(..., example=["handler1", "handler2"])