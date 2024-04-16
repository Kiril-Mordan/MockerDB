# RESPONSE DESCRIPTIONS FOR MOCKER-DB ENDPOINTS

ActivateHandlersDesc = {
             200: {"description": "Returns a list of active handlers along with their item counts and memory usage.",
                   "content": {
                        "application/json": {
                            "example": {
                                "handlers": ["default", "test_db1"],
                                "items": [0, 103],
                                "memory_usage": [1.2714920043945312, 1.6513137817382812]
                            }
                        }
                    }}}

RemoveHandlersDesc = {
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
                }}}

InitializeDesc = {
    200: {
        "description": "Database initialization response",
        "content": {
            "application/json": {
                "example": {"message": "Database initialized with new parameters"}
            }
        }
    }
}

InsertDesc = {
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
}

SearchDesc = {
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
}

DeleteDesc = {
    200: {
        "description": "Confirmation of data deletion",
        "content": {
            "application/json": {
                "example": {"message": "Data deleted successfully"}
            }
        }
    }
}

EmbedDesc = {
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
}