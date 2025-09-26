import logging
import pyodbc
from typing import Dict, List
from fastapi import  status,  Depends,APIRouter
from fastapi.responses import JSONResponse
from app.models.common import Status
from app.services.skillStoreService import GetFunctionHelper,GetSubFunctionHelper,\
    GetSkillTagsHelper,GetSkillScopeHelper,GetDepartmentHelper,GetDefaultChatbotConfigHelper,\
        GetAdditivesHelper
from app.services.promptMgmtService import GetCreativityHelper
from app.models.skillStore import UpdateStatus
from app.commons.error_helper import responses, GetJSONResponse, db_unauthorized
from app.commons.jwt_auth import validate_token

logger = logging.getLogger()

router = APIRouter(
    prefix="/common",
    tags=["Common"],
    responses={404: {"description": "Not found"}},
)

@router.get('/GetFunction', responses=responses("422", "500"))
async def GetFunction(LookupDepartmentId:int,token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'Get-Function Request : PayLoad {token}')
        function = await GetFunctionHelper(LookupDepartmentId) 
        return JSONResponse(status_code=status.HTTP_200_OK, content=function)
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while fetching Function: {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)    
    except Exception as ex:
        logging.exception(f'Exception while Get Function : {ex!r}')
        return GetJSONResponse(500, ex)

@router.post('/GetSubFunction', responses=responses("422", "500"))
async def GetSubFunction(body:List[int],token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'Get-SubFunction Request : PayLoad {token}')
        subFunction = await GetSubFunctionHelper(FunctionIds=body) 
        return JSONResponse(status_code=status.HTTP_200_OK, content=subFunction)
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while fetching SubFunction: {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)    
    except Exception as ex:
        logging.exception(f'Exception while Get SubFunction : {ex!r}')
        return GetJSONResponse(500, ex)

@router.get('/GetTags', responses=responses("422", "500"))
async def GetTags(token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'Get-Tags Request : PayLoad {token}')
        skillTag = await GetSkillTagsHelper() 
        return JSONResponse(status_code=status.HTTP_200_OK, content=skillTag)
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while fetching Tags: {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)    
    except Exception as ex:
        logging.exception(f'Exception while Get Tags : {ex!r}')
        return GetJSONResponse(500, ex)

@router.get('/GetDepartments', responses=responses("422", "500"))
async def GetDepartments(token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'Get-Departments Request : PayLoad {token}')
        skillTag = await GetDepartmentHelper() 
        return JSONResponse(status_code=status.HTTP_200_OK, content=skillTag)
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while fetching Get-Departments: {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)    
    except Exception as ex:
        logging.exception(f'Exception while Get Get-Departments : {ex!r}')
        return GetJSONResponse(500, ex)

@router.get('/GetSkillScope', responses=responses("422", "500"))
async def GetSkillScope(token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'Get-Skill-Scope Request : PayLoad {token}')
        skillScope = await GetSkillScopeHelper() 
        return JSONResponse(status_code=status.HTTP_200_OK, content=skillScope)
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while fetching Skill-Scope: {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)    
    except Exception as ex:
        logging.exception(f'Exception while Get Skill-Scope : {ex!r}')
        return GetJSONResponse(500, ex)

@router.get('/GetCreativity', responses=responses("422", "500"))
async def GetCreativity(token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'Get-creativity Request : PayLoad {token}')
        creativity = await GetCreativityHelper() 
        return JSONResponse(status_code=status.HTTP_200_OK, content=creativity)
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while fetching creativity: {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)    
    except Exception as ex:
        logging.exception(f'Exception while Get creativity : {ex!r}')
        return GetJSONResponse(500, ex)

@router.get('/GetDefaultChatbotConfig', responses=responses("422", "500"))
async def GetDefaultChatbotConfig(token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'Get-Default-Chatbot-Config Request : PayLoad {token}')
        chatbotConfig = await GetDefaultChatbotConfigHelper() 
        return JSONResponse(status_code=status.HTTP_200_OK, content=chatbotConfig)
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while fetching Get Default Chatbot Config: {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)    
    except Exception as ex:
        logging.exception(f'Exception while Get Default Chatbot Config : {ex!r}')
        return GetJSONResponse(500, ex)

@router.get('/GetAdditives', responses=responses("422", "500"))
async def GetAdditives(token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'Get-Additives Request : PayLoad {token}')
        Additives = await GetAdditivesHelper() 
        return JSONResponse(status_code=status.HTTP_200_OK, content=Additives)
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while fetching Additives: {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)    
    except Exception as ex:
        logging.exception(f'Exception while Get Additives : {ex!r}')
        return GetJSONResponse(500, ex)