import yaml
import os
from dotenv import load_dotenv
import json
import logging


with open("./conf/mocker_setup_params.yaml", 'r') as yaml_file:
    MOCKER_SETUP_PARAMS = yaml.safe_load(yaml_file)