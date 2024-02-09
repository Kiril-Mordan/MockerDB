import psutil
import gc

def check_and_offload_handlers(handlers: dict ,
                               threshold : int,
                               exception_handlers : list,
                               insert_size : float):

    insert_overhead = insert_size*2

    if insert_overhead > threshold:
        raise MemoryError(f"Insert is larger then alocated memory: {insert_overhead} > {threshold}")

    # Get available memory
    available_memory = psutil.virtual_memory().available + insert_size*2

    if available_memory < threshold:
        # Logic to select handlers to offload (simplified example)
        handler_names_to_offload = select_handlers_to_offload(exception_handlers = exception_handlers)

        # Offload selected handlers
        for handler_name in handler_names_to_offload:
            if handler_name in handlers:
                del handlers[handler_name]
                # Optionally, log the offloading action or notify the system
        # Force garbage collection to immediately free up memory
        gc.collect()

def select_handlers_to_offload(handlers : dict, exception_handlers : list):
    # Implement your policy for selecting handlers to offload
    # This could be based on LRU, handlers with least data, etc.
    # Simplified example: offload the first two handlers



    all_handlers = list(handlers.keys())

    handlers_available_for_removal = [h for h in all_handlers \
        if h not in exception_handlers]


    return handlers_available_for_removal[:2]