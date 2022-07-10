import os
import sys
sys.path.insert(0, os.getcwd())

from src.utils.common_logger import logger
from src.endpoints import DBC

def create(model):
    try:
        session = DBC.get_session()
        session.add(model)
        session.commit()
        session.refresh(model)
    except Exception as err:
        logger.error(f"{err}")


def read(model, field, search_value):
    try:
        session = DBC.get_session()
        result = session.query(model).filter(model.field == search_value).one()
        return result
    except Exception as err:
        logger.error(f"{err}")
