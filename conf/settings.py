import yaml
import os

# read-in default paramerst
with open("./conf/mocker_setup_params.yaml", 'r') as yaml_file:
    MOCKER_SETUP_PARAMS = yaml.safe_load(yaml_file)

with open("./conf/api_setup_params.yaml", 'r') as yaml_file:
    API_SETUP_PARAMS = yaml.safe_load(yaml_file)

# api version
with open("./env_spec/lsts_versions.yaml", 'r') as yaml_file:
    LSTS_VERSIONS = yaml.safe_load(yaml_file)

API_VERSION = LSTS_VERSIONS['api_version']

# read-in paramers values from env
EMBEDDER_PARAMS = os.getenv("EMBEDDER_PARAMS")
SIMILARITY_PARAMS = os.getenv("SIMILARITY_PARAMS")
PERSIST_FILEPATH = os.getenv("PERSIST_FILEPATH")
PERSIST = os.getenv("PERSIST")
EMBEDDER_ERROR_TOLERANCE = os.getenv("EMBEDDER_ERROR_TOLERANCE")

MEMORY_SCALER_FROM_BYTES = os.getenv("MEMORY_SCALER_FROM_BYTES")
MEMORY_RESET_LIMIT_MB = os.getenv("MEMORY_RESET_LIMIT_MB")


# update default paramers if any env parameters were provided
if EMBEDDER_PARAMS:
    MOCKER_SETUP_PARAMS['embedder_params'] = EMBEDDER_PARAMS
if SIMILARITY_PARAMS:
    MOCKER_SETUP_PARAMS['similarity_params'] = SIMILARITY_PARAMS
if PERSIST_FILEPATH:
    MOCKER_SETUP_PARAMS['file_path'] = PERSIST_FILEPATH
if PERSIST:
    MOCKER_SETUP_PARAMS['persist'] = PERSIST
if EMBEDDER_ERROR_TOLERANCE:
    MOCKER_SETUP_PARAMS['embedder_error_tolerance'] = EMBEDDER_ERROR_TOLERANCE

if MEMORY_SCALER_FROM_BYTES:
    API_SETUP_PARAMS['memory_scaler_from_bytes'] = MEMORY_SCALER_FROM_BYTES
if MEMORY_RESET_LIMIT_MB:
    API_SETUP_PARAMS['memory_reset_limit_mb'] = MEMORY_RESET_LIMIT_MB