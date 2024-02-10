import psutil
import gc
from pympler import asizeof

def check_and_offload_handlers(handlers: dict ,
                               allocated_bytes : int,
                               exception_handlers : list,
                               insert_size_bytes : float):

    # Assume larger size
    insert_overhead = insert_size_bytes*3
    # Size of handlers
    size_of_handlers = asizeof.asizeof(handlers)

    # Get available memory
    if allocated_bytes == 0:
        available_memory = psutil.virtual_memory().available
    else:
        available_memory = max(allocated_bytes, size_of_handlers)
        # Check if insert can even fit into memory
        insert_larger_then_memory = insert_overhead > available_memory
        if insert_larger_then_memory:
            raise MemoryError(f"Insert is larger then alocated memory: {insert_overhead} > {allocated_bytes}")
        # if no handlers to offload, check both usage and insert
        insert_larger_then_memory2 = (size_of_handlers + insert_overhead > available_memory) and (len(handlers)<=1)
        if insert_larger_then_memory2:
            raise MemoryError(f"Insert is larger then alocated memory: {size_of_handlers + insert_overhead} > {allocated_bytes}")

    anticipated_usage = size_of_handlers + insert_overhead

    if anticipated_usage > available_memory:
        # Logic to select handlers to offload (simplified example)
        handler_names_to_offload = select_handlers_to_offload(handlers = handlers,
                                                              exception_handlers = exception_handlers,
                                                              insert_overhead = insert_overhead)

        # Offload selected handlers
        for handler_name in handler_names_to_offload:
            if handler_name in handlers:
                del handlers[handler_name]
                # Optionally, log the offloading action or notify the system
        # Force garbage collection to immediately free up memory
        gc.collect()

def select_handlers_to_offload(handlers: dict, exception_handlers: list, insert_overhead : float):
    # Calculate scaled memory usage for each handler
    memory_usage = {hn: asizeof.asizeof(handlers[hn]) for hn in handlers}

    # Sort handlers by memory usage in descending order
    sorted_handlers_by_memory = sorted(memory_usage.items(), key=lambda x: x[1], reverse=True)

    # Free up memory until insert can fit
    handlers_to_offload = []
    accumulated_memory_freed = 0

    print(f"Attempting to free {insert_overhead/1024**2} MB")

    for hn, memory in sorted_handlers_by_memory:
        if hn in exception_handlers:
            continue  # Skip exception handlers
        if accumulated_memory_freed >= insert_overhead:
            break  # Stop if we have freed enough memory
        handlers_to_offload.append(hn)
        accumulated_memory_freed += memory

    print(f"Offloading {handlers_to_offload} handlers")

    return handlers_to_offload