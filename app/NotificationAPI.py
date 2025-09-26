import logging
import pyodbc
from typing import Dict, List
from fastapi import  status,  Depends,APIRouter
from fastapi.responses import JSONResponse
from app.services.notificationService import GetNotificationListByUserHelper,\
    UpdateNotificationReadStatusHelper
from app.models.common import Status
from app.commons.error_helper import responses, GetJSONResponse, db_unauthorized
from app.commons.jwt_auth import validate_token

logger = logging.getLogger()

router = APIRouter(
    prefix="/notification",
    tags=["Notification"],
    responses={404: {"description": "Not found"}},
)

@router.get('/GetNotifications', responses=responses("422", "500"))
async def GetNotification(token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'GetNotification Request : PayLoad {token}')
        PromptUserInputs = await GetNotificationListByUserHelper(user_id=token["user_id"]) 
        return JSONResponse(status_code=status.HTTP_200_OK, content=PromptUserInputs)
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while fetching Notifications: {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)    
    except Exception as ex:
        logging.exception(f'Exception while Get Notifications : {ex!r}')
        return GetJSONResponse(500, ex)

@router.put('/UpdateNotificationReadStatus', responses=responses("422", "500"))
async def UpdateNotificationReadStatus(notificationId: int, token: Dict = Depends(validate_token)):
    try:
        await UpdateNotificationReadStatusHelper(notificationId= notificationId,
                               user_id=token["user_id"]
                               )
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=Status(Status= "Read Status Updated Successfully.").dict())

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while updating Notification read status : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)