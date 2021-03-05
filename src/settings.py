import os
from dotenv import load_dotenv
from src.utils.common_logger import logger


# Load .ENV file
# After this, you can access to environment like os.environ.get("VAR")
def load_config(env_file_path: str):
    if os.path.isfile(env_file_path):
        load_dotenv(dotenv_path=env_file_path)
    else:
        logger.error(f"ENV file does not exist on {env_file_path}")
