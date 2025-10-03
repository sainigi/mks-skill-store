import logging
import pyodbc
from typing import Dict, List
from fastapi import  status,  Depends,APIRouter
from fastapi.responses import JSONResponse
from app.models.common import Status
from app.models.skillStore import DisableFollowupQuestions,CreateUpdateSkillStore,SkillResourceCost,DailySkillResourceCost
from app.services.skillStoreService import InsertUpdateLikeStatusHelper,\
        InsertUpdateUsedStatusHelper,GetSkillStoreHelper,GetSkillStoreByIdHelper,\
            CheckSkillsAvailabilityHelper,AddUpdateUsersSkillShowFollowupQuestionStateHelper,\
                CreateSkillHelper,UpdateSkillHelper,DeleteSkillHelper,GetSkillDetailsHelper,GetSkillResourceCostByDaysHelper,GetSkillResourceDetailHelper,AddDailySkillResourceCostBulkHelper
from app.models.skillStore import UpdateStatus
from app.commons.error_helper import responses, GetJSONResponse, db_unauthorized
from app.commons.jwt_auth import validate_token
from app.commons import auth
from fastapi.security.api_key import APIKey

logger = logging.getLogger()

router = APIRouter(
    prefix="/skillstore",
    tags=["SkillStore"],
    responses={404: {"description": "Not found"}},
)

@router.put('/UpdateLikeStatus', responses=responses("422", "500"))
async def UpdateLikeStatus(body: UpdateStatus, token: Dict = Depends(validate_token)):
    try:
        await InsertUpdateLikeStatusHelper(status= body,
                               user_id=token["user_id"]
                               )
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=Status(Status= "Like Status Updated Successfully.").dict())

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while updating like status : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while updating like status : {ex!r}')
        return GetJSONResponse(500, ex)

@router.put('/DisableFollowupQuestions', responses=responses("422", "500"))
async def DisableFollowupQuestions(body: DisableFollowupQuestions, token: Dict = Depends(validate_token)):
    try:
        await AddUpdateUsersSkillShowFollowupQuestionStateHelper(status= body,
                               user_id=token["user_id"]
                               )
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=Status(Status= "Followup Question Status Updated Successfully.").dict())

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while updating followup Question status : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while updating followup Question status : {ex!r}')
        return GetJSONResponse(500, ex)

@router.put('/UpdateUsedStatus', responses=responses("422", "500"))
async def UpdateUsedStatus(SkillStoreId:int, token: Dict = Depends(validate_token)):
    try:
        await InsertUpdateUsedStatusHelper(SkillStoreId= SkillStoreId,
                               user_id=token["user_id"]
                               )
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=Status(Status= "used Status Updated Successfully.").dict())

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while updating used status : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while updating like status : {ex!r}')
        return GetJSONResponse(500, ex)

@router.get('/GetSkillStore', responses=responses("422", "500"))
async def GetSkillStore(token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'Get-Skill-Store Request : PayLoad {token}')
        skillStores = await GetSkillStoreHelper(user_id=token["user_id"]) 
        return JSONResponse(status_code=status.HTTP_200_OK, content=skillStores)
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while fetching Skill-Store: {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)    
    except Exception as ex:
        logging.exception(f'Exception while Get Skill-Store : {ex!r}')
        return GetJSONResponse(500, ex)

@router.get('/GetSkillStoreById', responses=responses("422", "500"))
async def GetSkillStoreById(SkillStoreId:int,token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'Get-Skill-Store-by-Id Request : PayLoad {token}')
        skillStoreDetails = await GetSkillStoreByIdHelper(SkillStoreId=SkillStoreId,user_id=token["user_id"]) 
        return JSONResponse(status_code=status.HTTP_200_OK, content=skillStoreDetails)
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while fetching Skill-Store by Id: {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)    
    except Exception as ex:
        logging.exception(f'Exception while Get Skill-Store : {ex!r}')
        return GetJSONResponse(500, ex)

@router.get('/CheckSkillsAvailability', responses=responses("422", "500"))
async def CheckSkillsAvailability(token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'Check-Skills-Availability Request : PayLoad {token}')
        skills = await CheckSkillsAvailabilityHelper() 
        return JSONResponse(status_code=status.HTTP_200_OK, content=skills)
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while fetching CheckSkillsAvailability: {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)    
    except Exception as ex:
        logging.exception(f'Exception while Get CheckSkillsAvailability : {ex!r}')
        return GetJSONResponse(500, ex)

@router.post('/CreateSkillStore', responses=responses("422", "500"))
async def CreateSkillStore(body:CreateUpdateSkillStore,token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'CreateSkillStore Request : PayLoad {token}')
        logger.debug(f'CreateSkillStore Request : Body {body}')
        await CreateSkillHelper(data=body,user_id=token["user_id"])
        return JSONResponse(status_code=status.HTTP_200_OK, content=Status(Status= "Skill Created Successfully.").dict())
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while CreateSkillStore: {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)    
    except Exception as ex:
        logging.exception(f'Exception while CreateSkillStore : {ex!r}')
        return GetJSONResponse(500, ex)

@router.put('/UpdateSkillStore', responses=responses("422", "500"))
async def UpdateSkillStore(SkillStoreId:int,body:CreateUpdateSkillStore,token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'UpdateSkillStore Request : PayLoad {token}')
        logger.debug(f'UpdateSkillStore Request : Body {body}')
        await UpdateSkillHelper(data=body,SkillStoreId=SkillStoreId,user_id=token["user_id"])
        return JSONResponse(status_code=status.HTTP_200_OK, content=Status(Status= "Skill Updated Successfully.").dict())
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while UpdateSkillStore: {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)    
    except Exception as ex:
        logging.exception(f'Exception while UpdateSkillStore : {ex!r}')
        return GetJSONResponse(500, ex)

@router.delete('/DeleteSkillById', responses=responses("422", "500"))
async def DeleteSkillById(SkillStoreId:int,token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'DeleteSkillById Request : PayLoad {token}')
        await DeleteSkillHelper(SkillStoreId=SkillStoreId,user_id=token["user_id"]) 
        return JSONResponse(status_code=status.HTTP_200_OK, content=Status(Status= "Skill Deleted Successfully.").dict())
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while fetching DeleteSkillById: {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)    
    except Exception as ex:
        logging.exception(f'Exception while Get DeleteSkillById : {ex!r}')
        return GetJSONResponse(500, ex)

@router.get('/GetSkillDetails', responses=responses("422", "500"))
async def GetSkillDetails(SkillStoreId:int,token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'GetSkillDetails Request : PayLoad {token}')
        skillStoreDetails = await GetSkillDetailsHelper(SkillStoreId=SkillStoreId) 
        return JSONResponse(status_code=status.HTTP_200_OK, content=skillStoreDetails)
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while fetching Skill by Id: {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)    
    except Exception as ex:
        logging.exception(f'Exception while Get Skill : {ex!r}')
        return GetJSONResponse(500, ex)
    

@router.post('/GetSkillResourceCostByDays', responses=responses("422", "500"))
async def GetSkillResourceCostByDays(body:SkillResourceCost,token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'GetSkillResourceCostByDays Request : PayLoad {token}')
        logger.debug(f'GetSkillResourceCostByDays Request : Body {body}')
        skillResourceCost = await GetSkillResourceCostByDaysHelper(data=body)
        return JSONResponse(status_code=status.HTTP_200_OK, content=skillResourceCost)
    except pyodbc.Error as ex:
        logging.exception(f'Exception while getting Skill Resource Cost by days: {ex!r}')
        err_msg = str(ex)
        if 'SkillId' in err_msg and 'does not exist in SkillStore' in err_msg:
            return GetJSONResponse(404, f"SkillId not found: {body.SkillID}")
        elif 'Combination of SkillId' in err_msg and 'already exists' in err_msg:
            return GetJSONResponse(409, f"Duplicate entry: SkillId {body.SkillID}, ResourceId {body.ResourceId} exists.")
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)    
    except Exception as ex:
        logging.exception(f'Exception while getting Skill Resource Cost by days : {ex!r}')
        return GetJSONResponse(500, ex)
    
@router.get('/GetSkillResourceDetail', responses=responses("422","500"))
async def GetSkillResourceDetail( Authorization:APIKey = Depends(auth.get_api_key)):
    try:
        logger.debug(f"CreateSkillResourceDetail: token {Authorization}")
        skillResourceDetail = await GetSkillResourceDetailHelper()
        return JSONResponse(status_code=status.HTTP_200_OK, content=skillResourceDetail)
    except pyodbc.Error as ex:
        logging.exception(f'Db Exception while getting skill resource detail: {ex!r} ')
        err_msg = str(ex)
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex) 
    except Exception as ex:
        logging.exception(f'Exceptiopn While Getting Skill Resource Detail: {ex!r}')
        return GetJSONResponse(500,ex)
    
@router.post('/AddDailySkillResourceCostBulk', responses=responses("422","500"))
async def AddDailySkillResourceCostBulk(body:List[DailySkillResourceCost], Authorization:APIKey = Depends(auth.get_api_key)):
    try:
        logger.debug(f"AddDailySkillResourceCostBulk: token {Authorization}")
        logger.debug(f"AddDailySkillResourceCostBulk: body {body}")
        bulkResult = await AddDailySkillResourceCostBulkHelper(body)
        return JSONResponse(status_code=status.HTTP_200_OK, content=bulkResult) 
    except pyodbc.Error as ex:
        logging.exception(f"Db Exception while creating SkillResourceDetail: {ex!r}")
        err_msg = str(ex)
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500,ex)
    except Exception as ex:
        logging.exception(f'line2 ---> Exceptiopn While Getting Skill Resource Detail: {ex!r}')
        return GetJSONResponse(500,ex)