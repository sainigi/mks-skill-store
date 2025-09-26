import json
import logging
import os
import uuid
from typing import Dict

from commons.blob_helper import BlobExists, ReadBlob, WriteFile
from commons.sp_helper import exec_stored_procedure
from commons.utils import ItemExists
from app.models.common import LogBatch, LogObject, ActionType

logger = logging.getLogger()
RMPDB = os.environ["RMPDB"]

async def WriteLogs(x_correlation_store_id: str, log_obj: Dict, action_type: ActionType):
    try:
        await exec_stored_procedure(sp_name="InsertUpdateRMPProcessLogs",
                                    param_names=["BatchID", "ProcessingDateTime", "Status", "x_correlation_store_id",
                                                 "ActionType", "RestId", "GroupId", "Exception"],
                                    param_values=[log_obj["guid"], log_obj["ProcessingDateTime"], log_obj["Status"], x_correlation_store_id,
                                                  action_type, log_obj["restId"], log_obj["groupId"], log_obj["Exception"]],
                                    dbName=RMPDB,
                                    fetch_data=False)

        logger.info(f'Logs written successfully! BatchId: {log_obj["guid"]} correlationId: {x_correlation_store_id} Status: {log_obj["Status"]}')

    except Exception as ex:
        logger.exception(f'Exception while writing logs : {ex!r}')
        raise
