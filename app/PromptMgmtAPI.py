import logging
import pyodbc
from typing import Dict, List,Optional
from fastapi import  status,  Depends,APIRouter
from fastapi.responses import JSONResponse
from app.models.common import Status
from app.services.promptMgmtService import GetSkillsHelper,InsertUpdateCommentsHelper,\
    InsertUpdateViewHelper,CreatePromptHelper,UpdatePromptHelper,\
        InsertUpdateStaredStatusHelper,GetPromptUserInputByIdHelper,\
            GetPromptUserInputHelper,SharePromptWithUsersHelper,\
                InsertUpdatePromptUserInputLikeStatusHelper,BulkImportPromptHelper,\
                    GetChatPromptUserInputHelper,DeletePromptHelper,BulkImportPromptHelperV2
from app.models.promptMgmt import PromptUserInput,Comments,UpdateStatus,BulkImportPrompts,BulkImportPromptsV2
from app.commons.error_helper import responses, GetJSONResponse, db_unauthorized
from app.commons.jwt_auth import validate_token

logger = logging.getLogger()

router = APIRouter(
    prefix="/prompt",
    tags=["PromptManagement"],
    responses={404: {"description": "Not found"}},
)

@router.get('/GetSkills', responses=responses("422", "500"))
async def GetSkills(token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'Get-Skills Request : PayLoad {token}')
        skills = await GetSkillsHelper() 
        return JSONResponse(status_code=status.HTTP_200_OK, content=skills)
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while fetching Skills: {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)    
    except Exception as ex:
        logging.exception(f'Exception while Get Skills : {ex!r}')
        return GetJSONResponse(500, ex)

@router.post('/CreatePrompt', responses=responses("422", "500"))
async def CreatePrompt(body:PromptUserInput,token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'CreatePrompt Request : PayLoad {token}')
        logger.debug(f'CreatePrompt Request : Body {body}')
        await CreatePromptHelper(data=body,user_id=token["user_id"])
        return JSONResponse(status_code=status.HTTP_200_OK, content=Status(Status= "Prompt Created Successfully.").dict())
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while CreatePrompt: {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)    
    except Exception as ex:
        logging.exception(f'Exception while CreatePrompt : {ex!r}')
        return GetJSONResponse(500, ex)

@router.put('/EditPrompt', responses=responses("422", "500"))
async def EditPrompt(promptId:int,body:PromptUserInput,token: Dict = Depends(validate_token)):
    try:
        await UpdatePromptHelper(data=body,PromptUserInputId=promptId,user_id=token["user_id"])
        return JSONResponse(status_code=status.HTTP_200_OK, content=Status(Status= "Prompt Updated Successfully.").dict())
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while EditPrompt: {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)    
    except Exception as ex:
        logging.exception(f'Exception while EditPrompt : {ex!r}')
        return GetJSONResponse(500, ex)

@router.put('/UpdateViewStatus', responses=responses("422", "500"))
async def UpdateViewStatus(PromptUserInputId: int, token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'UpdateViewStatus Request : PayLoad {token}')
        logger.debug(f'UpdateViewStatus Request : Body {PromptUserInputId}')
        await InsertUpdateViewHelper(PromptUserInputId= PromptUserInputId,
                               user_id=token["user_id"]
                               )
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=Status(Status= "View Status Updated Successfully.").dict())

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while updating View status : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while updating View status : {ex!r}')
        return GetJSONResponse(500, ex)

@router.post('/AddComments', responses=responses("422", "500"))
async def AddComments(body:Comments, token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'AddComments Request : PayLoad {token}')
        logger.debug(f'AddComments Request : Body {body}')
        await InsertUpdateCommentsHelper(data=body,
                               user_id=token["user_id"]
                               )
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=Status(Status= "Comments added Successfully.").dict())

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while adding Comments : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while adding Comments : {ex!r}')
        return GetJSONResponse(500, ex)

@router.put('/UpdateStaredStatus', responses=responses("422", "500"))
async def UpdateStaredStatus(body: UpdateStatus, token: Dict = Depends(validate_token)):
    try:
        await InsertUpdateStaredStatusHelper(status= body,
                               user_id=token["user_id"]
                               )
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=Status(Status= "Stared Status Updated Successfully.").dict())

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while updating Stared status : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while updating Stared status : {ex!r}')
        return GetJSONResponse(500, ex)

@router.get('/GetPromptUserInputs', responses=responses("422", "500"))
async def GetPromptUserInputs(token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'GetPromptUserInput Request : PayLoad {token}')
        PromptUserInputs = await GetPromptUserInputHelper(user_id=token["user_id"]) 
        return JSONResponse(status_code=status.HTTP_200_OK, content=PromptUserInputs)
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while fetching GetPromptUserInput: {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)    
    except Exception as ex:
        logging.exception(f'Exception while Get GetPromptUserInput : {ex!r}')
        return GetJSONResponse(500, ex)

@router.get('/GetPromptUserInputById', responses=responses("422", "500"))
async def GetPromptUserInputById(PromptUserInputId:int,token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'GetPromptUserInputById Request : PayLoad {token}')
        PromptUserInputDetails = await GetPromptUserInputByIdHelper(PromptUserInputId=PromptUserInputId,user_id=token["user_id"]) 
        return JSONResponse(status_code=status.HTTP_200_OK, content=PromptUserInputDetails)
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while fetching GetPromptUserInputById: {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)    
    except Exception as ex:
        logging.exception(f'Exception while Get GetPromptUserInputById : {ex!r}')
        return GetJSONResponse(500, ex)

@router.put('/SharePromptWithUsers', responses=responses("422", "500"))
async def SharePromptWithUsers(PromptUserInputId:int,body:List[str], token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'SharePromptWithUsers Request : PayLoad {token}')
        await SharePromptWithUsersHelper(user_ids=body,PromptUserInputId= PromptUserInputId,
                               user_id=token["user_id"]
                               )
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=Status(Status= "User Mapping added Successfully.").dict())

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while updating user mapping : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while updating user mapping : {ex!r}')
        return GetJSONResponse(500, ex)

@router.put('/UpdateLikeStatus', responses=responses("422", "500"))
async def UpdateLikeStatus(body: UpdateStatus, token: Dict = Depends(validate_token)):
    try:
        await InsertUpdatePromptUserInputLikeStatusHelper(status= body,
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

@router.post('/BulkImportPrompt', responses=responses("422", "500"))
async def BulkImportPrompt(body: List[BulkImportPrompts], token: Dict = Depends(validate_token)):
    try:
        await BulkImportPromptHelper(prompts= body,
                               user_id=token["user_id"]
                               )
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=Status(Status= "Prompt imported Successfully.").dict())

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while bulk import : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while bulk import : {ex!r}')
        return GetJSONResponse(500, ex)

@router.post('/BulkImportPromptV2', responses=responses("422", "500"))
async def BulkImportPromptV2(body: List[BulkImportPromptsV2], token: Dict = Depends(validate_token)):
    try:
        await BulkImportPromptHelperV2(prompts= body,
                               user_id=token["user_id"]
                               )
        
        return JSONResponse(status_code=status.HTTP_200_OK, content=Status(Status= "Prompt(s) imported successfully.").dict())

    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while bulk import V2 : {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)

    except Exception as ex:
        logging.exception(f'Exception while bulk import V2 : {ex!r}')
        return GetJSONResponse(500, ex)

@router.get('/GetChatPromptUserInput', responses=responses("422", "500"))
async def GetChatPromptUserInput(SkillStoreId: Optional[int], token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'GetChatPromptUserInput Request : PayLoad {token}')
        chatPrompts = await GetChatPromptUserInputHelper(SkillStoreId=SkillStoreId,user_id=token["user_id"]) 
        return JSONResponse(status_code=status.HTTP_200_OK, content=chatPrompts)
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while fetching chatPrompts: {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)    
    except Exception as ex:
        logging.exception(f'Exception while Get chatPrompts : {ex!r}')
        return GetJSONResponse(500, ex)

@router.delete('/deletepromptbyId', responses=responses("422", "500"))
async def GetPromptById(PromptUserInputId:int,token: Dict = Depends(validate_token)):
    try:
        logger.debug(f'deletepromptbyId Request : PayLoad {token}')
        await DeletePromptHelper(PromptUserInputId=PromptUserInputId,user_id=token["user_id"]) 
        return JSONResponse(status_code=status.HTTP_200_OK, content=Status(Status= "Prompt Deleted Successfully.").dict())
    except pyodbc.Error as ex:
        logging.exception(f'DB Exception while fetching deletepromptbyId: {ex!r}')
        if db_unauthorized in ex.args[1]:
            return GetJSONResponse(401, db_unauthorized)
        return GetJSONResponse(500, ex)    
    except Exception as ex:
        logging.exception(f'Exception while Get deletepromptbyId : {ex!r}')
        return GetJSONResponse(500, ex)