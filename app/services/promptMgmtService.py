from typing import List,Optional
from app.models.skillStore import Filter
from app.models.promptMgmt import PromptUserInput,Comments,UpdateStatus,\
    PromptSystemGeneratedInputList,PromptUserInputList,PromptUserInputComments,\
        BulkImportPrompts,ChatbotConfiguration,Skills,BulkImportPromptsV2
from app.commons.sp_helper import exec_store_proc,exec_stored_procedure_multiple_sets
import logging
import os
from app.commons.utils import stringify_dt

logger = logging.getLogger()

SkillStoreDBCon = os.environ["SkillStoreDB"]

async def GetSkillsHelper():
    try:
        skills,chatbotBaseConfig,dynamicParam = await exec_stored_procedure_multiple_sets(sp_name="GetSkills",
                                            param_names=[], 
                                            param_values=[],
                                            conStr=SkillStoreDBCon, 
                                            fetch_data=True)
        chatbotConfig_List = []
        
        for chatconfig in chatbotBaseConfig:
            dynamicParam_dict = [x for x in dynamicParam if x[0] == chatconfig[1]]
            curlRequest = await BuildCurlRequest(curlRequest=chatconfig[8],dynamicProperty=dynamicParam_dict)
            
            chatbotConfig = ChatbotConfiguration(SkillStoreId=chatconfig[0],
                                                Id=chatconfig[1],
                                                IsDefault=chatconfig[2],
                                                InputType=chatconfig[3],
                                                OutputType=chatconfig[4],
                                                FileType=chatconfig[5],
                                                ChatbotUIView=chatconfig[6],
                                                LastMessagesCount=chatconfig[7],
                                                ChatGPTVersion=chatconfig[9],
                                                IsChatbotTestable=chatconfig[10],
                                                UserMessageFormat=chatconfig[11],
                                                AssistantMessageFormat=chatconfig[11].replace("user","assistant").replace("$Message","$replyMsg") if chatconfig[11] else None,
                                                SecurityGroupId=chatconfig[12],
                                                ShowCitation=chatconfig[13],
                                                ShowFollowUpQuestions=chatconfig[14],
                                                DisableFollowUpQuestions=chatconfig[15],
                                                CitationURL=chatconfig[16],
                                                CitationParams=chatconfig[17],
                                                ImageURL=chatconfig[18],
                                                ImageParams=chatconfig[19],
                                                CurlRequestString=curlRequest
                                                ).dict()
            chatbotConfig_List.append(chatbotConfig)
        
        logger.debug(f'{skills}')
        skill_list=[]
        for sl in skills:
            chatbotConfig_dict = [x for x in chatbotConfig_List if x["SkillStoreId"] == sl[0]]
            if len(chatbotConfig_dict) == 0:
                chatbotConfig_dict = [x for x in chatbotConfig_List if x["IsDefault"] == True]
            
            skill_list.append(Skills(
                Id=sl[0],
                Name=sl[1],
                SecurityGroupId=chatbotConfig_dict[0].get("SecurityGroupId"),
                ChatbotConfiguration=chatbotConfig_dict[0],
            ).dict())
        return skill_list
    except Exception as ex:
        raise

async def InsertUpdateViewHelper(PromptUserInputId:int,user_id:str):
    try:
        await exec_store_proc(sp_name="InsertUpdatePromptViewStatus",
                                param_names=["ViewBy","PromptUserInputId"], 
                                param_values=[user_id,PromptUserInputId],
                                conStr=SkillStoreDBCon, 
                                fetch_data=False)
    except Exception as ex:
        raise

async def InsertUpdateCommentsHelper(data:Comments,user_id:str):
    try:
        await exec_store_proc(sp_name="InsertUpdatePromptComments",
                                param_names=["CommentBy","Comment","PromptUserInputId","ParentCommentId"], 
                                param_values=[user_id,data.Comment,data.PromptUserInputId,data.ParentCommentId],
                                conStr=SkillStoreDBCon, 
                                fetch_data=False)
    except Exception as ex:
        raise

async def CreatePromptHelper(data:PromptUserInput,user_id:str):
    try:
        functions = []
        subFunctions = []
        tags = []
        promptSystemGeneratedInputs = []
        for id in data.functions:
            functions.append((id,))
        
        for id in data.subFunctions:
            subFunctions.append((id,))
        
        for text in data.tags:
            tags.append((text,))
            
        for sysgen in data.PromptSystemGeneratedInputs:
            promptSystemGeneratedInputs.append((sysgen.ModelAPIURL,sysgen.PromptStyle,
                                                sysgen.WordCount if sysgen.WordCount else -1,
                                                sysgen.PromptGenerated,sysgen.PromptText,sysgen.Status))
        
        logger.debug(f'promptSystemGeneratedInputs: {promptSystemGeneratedInputs}')
        
        await exec_store_proc(sp_name="InsertPrompt",
                                param_names=["UserId","SkillStoreId","IsDisclaimerAccepted",
                                             "DisclaimerText","Title","ShortDescription",
                                             "PromptBackground","DesiredPromptOutput","SourceOnInputOutput",
                                             "IsConfidentialAccepted","ConfidentialText","LookupDepartmentId","IsPublic",
                                             "CardImage_Base64","ImageName","MimeType","WordCount","LookupCreativityId","Result","PromptSystemGeneratedInput",
                                             "LookupFunction","LookupSubFunction","Tags"], 
                                param_values=[user_id,data.SkillStoreId,data.IsDisclaimerAccepted,data.DisclaimerText,
                                              data.Title,data.ShortDescription,data.PromptBackground,data.DesiredPromptOutput,
                                              data.SourceOnInputOutput,data.IsConfidentialAccepted,data.ConfidentialText,
                                              data.LookupDepartmentId,data.IsPublic,data.CardImage_Base64,
                                              data.ImageName,data.MimeType,data.WordCount,data.LookupCreativityId,data.Result,promptSystemGeneratedInputs,functions,
                                              subFunctions,tags],
                                conStr=SkillStoreDBCon, 
                                fetch_data=False)
    except Exception as ex:
        raise

async def UpdatePromptHelper(data:PromptUserInput,PromptUserInputId:int,user_id:str):
    try:
        functions = []
        subFunctions = []
        tags = []
        promptSystemGeneratedInputs = []
        for id in data.functions:
            functions.append((id,))
        
        for id in data.subFunctions:
            subFunctions.append((id,))
        
        for text in data.tags:
            tags.append((text,))
            
        for sysgen in data.PromptSystemGeneratedInputs:
            promptSystemGeneratedInputs.append((sysgen.ModelAPIURL,sysgen.PromptStyle,
                                                sysgen.WordCount if sysgen.WordCount else -1,
                                                sysgen.PromptGenerated,sysgen.PromptText,sysgen.Status))
            
        await exec_store_proc(sp_name="UpdatePrompt",
                                param_names=["PromptId","UserId","SkillStoreId","IsDisclaimerAccepted",
                                             "DisclaimerText","Title","ShortDescription",
                                             "PromptBackground","DesiredPromptOutput","SourceOnInputOutput",
                                             "IsConfidentialAccepted","ConfidentialText","LookupDepartmentId","IsPublic",
                                             "CardImage_Base64","ImageName","MimeType","WordCount","LookupCreativityId","Result","PromptSystemGeneratedInput",
                                             "LookupFunction","LookupSubFunction","Tags"], 
                                param_values=[PromptUserInputId,user_id,data.SkillStoreId,data.IsDisclaimerAccepted,data.DisclaimerText,
                                              data.Title,data.ShortDescription,data.PromptBackground,data.DesiredPromptOutput,
                                              data.SourceOnInputOutput,data.IsConfidentialAccepted,data.ConfidentialText,
                                              data.LookupDepartmentId,data.IsPublic,data.CardImage_Base64,
                                              data.ImageName,data.MimeType,data.WordCount,data.LookupCreativityId,data.Result,promptSystemGeneratedInputs,functions,
                                              subFunctions,tags],
                                conStr=SkillStoreDBCon, 
                                fetch_data=False)
    except Exception as ex:
        raise

async def InsertUpdateStaredStatusHelper(status:UpdateStatus,user_id:str):
    try:
        await exec_store_proc(sp_name="InsertUpdateStaredStatus",
                                param_names=["IsStared","StaredBy","PromptUserInputId"], 
                                param_values=[status.Status,user_id,status.PromptUserInputId],
                                conStr=SkillStoreDBCon, 
                                fetch_data=False)
    except Exception as ex:
        raise
    
async def GetPromptUserInputHelper(user_id:str):
    try:
        promptUserInput,skillTag,skillFunction,skillSubFunction,promptSystemGeneratedInput,Comments,users,chatbotBaseConfig,dynamicParam = await exec_stored_procedure_multiple_sets(sp_name="GetPromptUserInputs",
                                            param_names=["UserId"], 
                                            param_values=[user_id],
                                            conStr=SkillStoreDBCon, 
                                            fetch_data=True) 
        
        
        chatbotConfig_List = []
        for chatconfig in chatbotBaseConfig:
            dynamicParam_dict = [x for x in dynamicParam if x[0] == chatconfig[1]]
            curlRequest = await BuildCurlRequest(curlRequest=chatconfig[8],dynamicProperty=dynamicParam_dict)
            
            chatbotConfig = ChatbotConfiguration(SkillStoreId=chatconfig[0],
                                                Id=chatconfig[1],
                                                IsDefault=chatconfig[2],
                                                InputType=chatconfig[3],
                                                OutputType=chatconfig[4],
                                                FileType=chatconfig[5],
                                                ChatbotUIView=chatconfig[6],
                                                LastMessagesCount=chatconfig[7],
                                                ChatGPTVersion=chatconfig[9],
                                                IsChatbotTestable=chatconfig[10],
                                                UserMessageFormat=chatconfig[11],
                                                AssistantMessageFormat=chatconfig[11].replace("user","assistant").replace("$Message","$replyMsg") if chatconfig[11] else None,
                                                SecurityGroupId=chatconfig[12],
                                                ShowCitation=chatconfig[13],
                                                ShowFollowUpQuestions=chatconfig[14],
                                                DisableFollowUpQuestions=chatconfig[15],
                                                CitationURL=chatconfig[16],
                                                CitationParams=chatconfig[17],
                                                ImageURL=chatconfig[18],
                                                ImageParams=chatconfig[19],
                                                CurlRequestString=curlRequest
                                                ).dict()
            chatbotConfig_List.append(chatbotConfig)       
       
        promptUserInput_List=[]
        for ssl in promptUserInput:
            promptuserinput = None
            skillTag_dict = [x for x in skillTag if x[0] == ssl[0]]
            skillfunction_dict = [x for x in skillFunction if x[0] == ssl[0]]
            skillsubfunction_dict = [x for x in skillSubFunction if x[0] == ssl[0]]
            promptSystemGeneratedInput_dict = [x for x in promptSystemGeneratedInput if x[0] == ssl[0]]
            comments_dict = [x for x in Comments if x[0] == ssl[0]]
            users_dict = [x for x in users if x[0] == ssl[0]]
            chatbotConfig_dict = [x for x in chatbotConfig_List if x["SkillStoreId"] == ssl[1]]
            if len(chatbotConfig_dict) == 0:
                chatbotConfig_dict = [x for x in chatbotConfig_List if x["IsDefault"] == True]
            skillTag_List = []
            skillFunction_List = []
            skillSubFunction_List = []
            promptSystemGeneratedInput_List = []
            comments_List = []
            users_List = []
            for sa in skillTag_dict:
                skillTag_List.append(Filter(
                    Id=sa[1],
                    Name=sa[2]
                    ).dict())
            
            for sa in skillfunction_dict:
                skillFunction_List.append(Filter(
                    Id=sa[1],
                    Name=sa[2]
                    ).dict())
                
            for sa in skillsubfunction_dict:
                skillSubFunction_List.append(Filter(
                    Id=sa[1],
                    Name=sa[2]
                    ).dict())
            
            for sa in promptSystemGeneratedInput_dict:
                promptSystemGeneratedInput_List.append(PromptSystemGeneratedInputList(
                    Id=sa[1],
                    ModelAPIURL=sa[2],
                    PromptStyle=sa[3],
                    WordCount=sa[4],
                    PromptGenerated=sa[5],
                    PromptText=sa[6],
                    Status=sa[7],
                    ).dict())
            
            for sa in comments_dict:
                comments_List.append(PromptUserInputComments(
                                    Id=sa[1],
                                    Comment=sa[2],
                                    CommentDate=stringify_dt(sa[3]),
                                    FirstName=sa[4],
                                    LastName=sa[5],
                                    ParentCommentId=sa[6],
                                    userImage=sa[7],
                                    userImageMimeType=sa[8]
                                ).dict())
            
            for sa in users_dict:
                users_List.append(sa[1])
            
            promptuserinput = PromptUserInputList(
                Id=ssl[0],
                SkillStoreId=ssl[1],
                SkillStoreName=ssl[2],
                SecurityGroupId=chatbotConfig_dict[0].get("SecurityGroupId"),
                IsDisclaimerAccepted=ssl[3],
                DisclaimerText=ssl[4],
                Title=ssl[5],
                ShortDescription=ssl[6],
                PromptBackground=ssl[7],
                DesiredPromptOutput=ssl[8],
                SourceOnInputOutput=ssl[9],
                IsConfidentialAccepted=ssl[10],
                ConfidentialText=ssl[11],
                LookupDepartmentId=ssl[12],
                DepartmentName=ssl[13],
                IsPublic=ssl[14],
                CardImage_Base64=ssl[15],
                ImageName=ssl[16],
                MimeType=ssl[17],
                IsViewed=ssl[18],
                IsCommented=ssl[19],
                IsStared=ssl[20],
                ViewCount=ssl[21],
                CommentCount=ssl[22],
                CreatedByFirstName=ssl[23],
                CreatedByLastName=ssl[24],
                WordCount=ssl[25],
                CreativityName=ssl[26],
                LookupCreativityId=ssl[27],
                IsReadonlyAccess=ssl[28],
                CreatedById=ssl[29],
                LikeCount=ssl[30],
                IsLiked=ssl[31],
                IsMyPrompt=ssl[32],
                IsSharedPrompt=ssl[33],
                IsImportedPrompt=ssl[34],
                CreatedOn=stringify_dt(ssl[35]),
                LastUpdatedOn=stringify_dt(ssl[36]),
				SkillStoreShortDescription=ssl[37],
                Result=ssl[38],
                userImage=ssl[39],
                userImageMimeType=ssl[40],
                IsUsingWrapperAPIURL=ssl[41],
                WrapperAPIURL=ssl[42],
                tags=skillTag_List,
                functions=skillFunction_List,
                subFunctions=skillSubFunction_List,
                PromptSystemGeneratedInputs=promptSystemGeneratedInput_List,
                comments=comments_List,
                Users=users_List,
                ChatbotConfiguration=chatbotConfig_dict[0]
                ).dict()
            logger.debug(f'{promptuserinput}')
            promptUserInput_List.append(promptuserinput)
            
        return promptUserInput_List
    except Exception as ex:
        raise

    
async def GetChatPromptUserInputHelper(SkillStoreId:Optional[int],user_id:str):
    try:
        if SkillStoreId == None:
            SkillStoreId = 0
        promptUserInput,skillFunction,promptSystemGeneratedInput,chatbotBaseConfig,dynamicParam = await exec_stored_procedure_multiple_sets(sp_name="GetChatPromptUserInputs",
                                            param_names=["UserId","SkillStoreId"], 
                                            param_values=[user_id,SkillStoreId],
                                            conStr=SkillStoreDBCon, 
                                            fetch_data=True) 
        
        
        chatbotConfig_List = []
        for chatconfig in chatbotBaseConfig:
            dynamicParam_dict = [x for x in dynamicParam if x[0] == chatconfig[1]]
            curlRequest = await BuildCurlRequest(curlRequest=chatconfig[8],dynamicProperty=dynamicParam_dict)
            
            chatbotConfig = ChatbotConfiguration(SkillStoreId=chatconfig[0],
                                                Id=chatconfig[1],
                                                IsDefault=chatconfig[2],
                                                InputType=chatconfig[3],
                                                OutputType=chatconfig[4],
                                                FileType=chatconfig[5],
                                                ChatbotUIView=chatconfig[6],
                                                LastMessagesCount=chatconfig[7],
                                                ChatGPTVersion=chatconfig[9],
                                                IsChatbotTestable=chatconfig[10],
                                                UserMessageFormat=chatconfig[11],
                                                AssistantMessageFormat=chatconfig[11].replace("user","assistant").replace("$Message","$replyMsg") if chatconfig[11] else None,
                                                SecurityGroupId=chatconfig[12],
                                                ShowCitation=chatconfig[13],
                                                ShowFollowUpQuestions=chatconfig[14],
                                                DisableFollowUpQuestions=chatconfig[15],
                                                CitationURL=chatconfig[16],
                                                CitationParams=chatconfig[17],
                                                ImageURL=chatconfig[18],
                                                ImageParams=chatconfig[19],
                                                CurlRequestString=curlRequest
                                                ).dict()
            chatbotConfig_List.append(chatbotConfig)       
       
        promptUserInput_List=[]
        for ssl in promptUserInput:
            promptuserinput = None
            skillfunction_dict = [x for x in skillFunction if x[0] == ssl[0]]
            promptSystemGeneratedInput_dict = [x for x in promptSystemGeneratedInput if x[0] == ssl[0]]
            chatbotConfig_dict = [x for x in chatbotConfig_List if x["SkillStoreId"] == ssl[1]]
            if len(chatbotConfig_dict) == 0:
                chatbotConfig_dict = [x for x in chatbotConfig_List if x["IsDefault"] == True]
            skillFunction_List = []
            promptSystemGeneratedInput_List = []
            
            for sa in skillfunction_dict:
                skillFunction_List.append(Filter(
                    Id=sa[1],
                    Name=sa[2]
                    ).dict())
                
            for sa in promptSystemGeneratedInput_dict:
                promptSystemGeneratedInput_List.append(PromptSystemGeneratedInputList(
                    Id=sa[1],
                    ModelAPIURL=sa[2],
                    PromptStyle=sa[3],
                    WordCount=sa[4],
                    PromptGenerated=sa[5],
                    PromptText=sa[6],
                    Status=sa[7],
                    ).dict())
            
            promptuserinput = PromptUserInputList(
                Id=ssl[0],
                SkillStoreId=ssl[1],
                SkillStoreName=ssl[2],
                SecurityGroupId=chatbotConfig_dict[0].get("SecurityGroupId"),
                IsDisclaimerAccepted=ssl[3],
                DisclaimerText=ssl[4],
                Title=ssl[5],
                ShortDescription=ssl[6],
                PromptBackground=ssl[7],
                DesiredPromptOutput=ssl[8],
                SourceOnInputOutput=ssl[9],
                IsConfidentialAccepted=ssl[10],
                ConfidentialText=ssl[11],
                LookupDepartmentId=ssl[12],
                DepartmentName=ssl[13],
                IsPublic=ssl[14],
                IsViewed=ssl[15],
                IsCommented=ssl[16],
                IsStared=ssl[17],
                ViewCount=ssl[18],
                CommentCount=ssl[19],
                CreatedByFirstName=ssl[20],
                CreatedByLastName=ssl[21],
                WordCount=ssl[22],
                CreativityName=ssl[23],
                LookupCreativityId=ssl[24],
                IsReadonlyAccess=ssl[25],
                CreatedById=ssl[26],
                LikeCount=ssl[27],
                IsLiked=ssl[28],
                IsMyPrompt=ssl[29],
                IsSharedPrompt=ssl[30],
                IsImportedPrompt=ssl[31],
                CreatedOn=stringify_dt(ssl[32]),
                LastUpdatedOn=stringify_dt(ssl[33]),
                SkillStoreShortDescription=ssl[34],
                userImage=ssl[35],
                userImageMimeType=ssl[36], 
                IsUsingWrapperAPIURL=ssl[37],
                WrapperAPIURL=ssl[38],             
                tags=[],
                functions=skillFunction_List,
                subFunctions=[],
                PromptSystemGeneratedInputs=promptSystemGeneratedInput_List,
                Users=[],
                ChatbotConfiguration=chatbotConfig_dict[0]
                ).dict()
            logger.debug(f'{promptuserinput}')
            promptUserInput_List.append(promptuserinput)
            
        return promptUserInput_List
    except Exception as ex:
        raise

async def GetPromptUserInputByIdHelper(PromptUserInputId:int,user_id:str):
    try:
        promptUserInput,skillTag,skillFunction,skillSubFunction,promptSystemGeneratedInput,Comments,users,chatbotBaseConfig,dynamicParam = await exec_stored_procedure_multiple_sets(sp_name="GetPromptUserInputById",
                                            param_names=["UserId","PromptUserInputId"], 
                                            param_values=[user_id,PromptUserInputId],
                                            conStr=SkillStoreDBCon, 
                                            fetch_data=True)
        
        dynamicParam_dict = [x for x in dynamicParam if x[0] == chatbotBaseConfig[0][1]]
        curlRequest = await BuildCurlRequest(curlRequest=chatbotBaseConfig[0][8],dynamicProperty=dynamicParam_dict)
        
        chatbotConfig = ChatbotConfiguration(SkillStoreId=chatbotBaseConfig[0][0],
                                            Id=chatbotBaseConfig[0][1],
                                            IsDefault=chatbotBaseConfig[0][2],
                                            InputType=chatbotBaseConfig[0][3],
                                            OutputType=chatbotBaseConfig[0][4],
                                            FileType=chatbotBaseConfig[0][5],
                                            ChatbotUIView=chatbotBaseConfig[0][6],
                                            LastMessagesCount=chatbotBaseConfig[0][7],
                                            ChatGPTVersion=chatbotBaseConfig[0][9],
                                            IsChatbotTestable=chatbotBaseConfig[0][10],
                                            UserMessageFormat=chatbotBaseConfig[0][11],
                                            AssistantMessageFormat=chatbotBaseConfig[0][11].replace("user","assistant").replace("$Message","$replyMsg") if chatbotBaseConfig[0][11] else None,
                                            SecurityGroupId=chatbotBaseConfig[0][12],
                                            ShowCitation=chatbotBaseConfig[0][13],
                                            ShowFollowUpQuestions=chatbotBaseConfig[0][14],
                                            DisableFollowUpQuestions=chatbotBaseConfig[0][15],
                                            CitationURL=chatbotBaseConfig[0][16],
                                            CitationParams=chatbotBaseConfig[0][17],
                                            ImageURL=chatbotBaseConfig[0][18],
                                            ImageParams=chatbotBaseConfig[0][19],
                                            CurlRequestString=curlRequest
                                            ).dict()
              
        if promptUserInput == None or len(promptUserInput) == 0:
            return None
       
        promptuserinput = None
        skillTag_List = []
        skillFunction_List = []
        skillSubFunction_List = []
        promptSystemGeneratedInput_List = []
        comments_List = []
        users_List = []
        for sa in skillTag:
            skillTag_List.append(Filter(
                Id=sa[1],
                Name=sa[2]
                ).dict())
        
        for sa in skillFunction:
            skillFunction_List.append(Filter(
                Id=sa[1],
                Name=sa[2]
                ).dict())
            
        for sa in skillSubFunction:
            skillSubFunction_List.append(Filter(
                Id=sa[1],
                Name=sa[2]
                ).dict())
        
        for sa in promptSystemGeneratedInput:
            promptSystemGeneratedInput_List.append(PromptSystemGeneratedInputList(
                Id=sa[1],
                ModelAPIURL=sa[2],
                PromptStyle=sa[3],
                WordCount=sa[4],
                PromptGenerated=sa[5],
                PromptText=sa[6],
                Status=sa[7],
                ).dict())
            
        for sa in Comments:
            comments_List.append(PromptUserInputComments(
                Id=sa[1],
                Comment=sa[2],
                CommentDate=stringify_dt(sa[3]),
                FirstName=sa[4],
                LastName=sa[5],
                ParentCommentId=sa[6],
                userImage=sa[7],
                userImageMimeType=sa[8]
                ).dict())
        
        for sa in users:
            users_List.append(sa[1])
        
        promptuserinput = PromptUserInputList(
            Id=promptUserInput[0][0],
            SkillStoreId=promptUserInput[0][1],
            SkillStoreName=promptUserInput[0][2],
            SecurityGroupId=chatbotConfig.get("SecurityGroupId"),
            IsDisclaimerAccepted=promptUserInput[0][3],
            DisclaimerText=promptUserInput[0][4],
            Title=promptUserInput[0][5],
            ShortDescription=promptUserInput[0][6],
            PromptBackground=promptUserInput[0][7],
            DesiredPromptOutput=promptUserInput[0][8],
            SourceOnInputOutput=promptUserInput[0][9],
            IsConfidentialAccepted=promptUserInput[0][10],
            ConfidentialText=promptUserInput[0][11],
            LookupDepartmentId=promptUserInput[0][12],
            DepartmentName=promptUserInput[0][13],
            IsPublic=promptUserInput[0][14],
            CardImage_Base64=promptUserInput[0][15],
            ImageName=promptUserInput[0][16],
            MimeType=promptUserInput[0][17],
            IsViewed=promptUserInput[0][18],
            IsCommented=promptUserInput[0][19],
            IsStared=promptUserInput[0][20],
            ViewCount=promptUserInput[0][21],
            CommentCount=promptUserInput[0][22],
            CreatedByFirstName=promptUserInput[0][23],
            CreatedByLastName=promptUserInput[0][24],
            WordCount=promptUserInput[0][25],
            CreativityName=promptUserInput[0][26],
            LookupCreativityId=promptUserInput[0][27],
            IsReadonlyAccess=promptUserInput[0][28],
            CreatedById=promptUserInput[0][29],
            LikeCount=promptUserInput[0][30],
            IsLiked=promptUserInput[0][31],
            IsMyPrompt=promptUserInput[0][32],
            IsSharedPrompt=promptUserInput[0][33],
            IsImportedPrompt=promptUserInput[0][34],
            CreatedOn=stringify_dt(promptUserInput[0][35]),
            LastUpdatedOn=stringify_dt(promptUserInput[0][36]),
            SkillStoreShortDescription=promptUserInput[0][37],
            Result=promptUserInput[0][38],
            userImage=promptUserInput[0][39],
            userImageMimeType=promptUserInput[0][40],
            IsUsingWrapperAPIURL=promptUserInput[0][41],
            WrapperAPIURL=promptUserInput[0][42],
            tags=skillTag_List,
            functions=skillFunction_List,
            subFunctions=skillSubFunction_List,
            PromptSystemGeneratedInputs=promptSystemGeneratedInput_List,
            comments=comments_List,
            Users=users_List,
            ChatbotConfiguration=chatbotConfig
            ).dict()
        
        return promptuserinput
    except Exception as ex:
        raise
    
async def GetCreativityHelper():
    try:
        creativity = await exec_store_proc(sp_name="GetCreativity",
                                            param_names=[], 
                                            param_values=[],
                                            conStr=SkillStoreDBCon, 
                                            fetch_data=True)
        logger.debug(f'{creativity}')
        creativity_list=[]
        for sl in creativity:
            creativity_list.append(Filter(
                Id=sl[0],
                Name=sl[1]
            ).dict())
        return creativity_list
    except Exception as ex:
        raise
    
async def SharePromptWithUsersHelper(user_ids:List[str],PromptUserInputId:int,user_id:str):
    try:
        userIds = []        
        for text in user_ids:
            userIds.append((text,))            
        
        await exec_store_proc(sp_name="InsertUpdatePromptUserInputUserMapping",
                                param_names=["UserId","PromptUserInputId","UserIds"], 
                                param_values=[user_id,PromptUserInputId,userIds],
                                conStr=SkillStoreDBCon, 
                                fetch_data=False)
    except Exception as ex:
        raise

async def InsertUpdatePromptUserInputLikeStatusHelper(status:UpdateStatus,user_id:str):
    try:
        await exec_store_proc(sp_name="InsertUpdatePromptUserInputLikeStatus",
                                param_names=["IsLiked","LikedBy","PromptUserInputId"], 
                                param_values=[status.Status,user_id,status.PromptUserInputId],
                                conStr=SkillStoreDBCon, 
                                fetch_data=False)
    except Exception as ex:
        raise
    
async def BulkImportPromptHelper(prompts:List[BulkImportPrompts],user_id:str):
    try:     
        prompt_lst =[]
        for prompt in prompts:
            prompt_lst.append((prompt.Title,prompt.ShortDescription))  
        await exec_store_proc(sp_name="BulkImportPrompts",
                                param_names=["UserId","Prompts"], 
                                param_values=[user_id,prompt_lst],
                                conStr=SkillStoreDBCon, 
                                fetch_data=False)
    except Exception as ex:
        raise

async def BulkImportPromptHelperV2(prompts:List[BulkImportPromptsV2],user_id:str):
    try:     
        prompt_lst =[]
        for prompt in prompts:
            prompt_lst.append((prompt.Title,prompt.ShortDescription,prompt.SkillStoreId))  
        await exec_store_proc(sp_name="BulkImportPromptsV2",
                                param_names=["UserId","Prompts"], 
                                param_values=[user_id,prompt_lst],
                                conStr=SkillStoreDBCon, 
                                fetch_data=False)
    except Exception as ex:
        raise


async def DeletePromptHelper(PromptUserInputId:int,user_id:str):
    try:
        await exec_stored_procedure_multiple_sets(sp_name="DeletePromptUserInput",
                                            param_names=["UserId","PromptUserInputId"], 
                                            param_values=[user_id,PromptUserInputId],
                                            conStr=SkillStoreDBCon, 
                                            fetch_data=False)
    except Exception as ex:
        raise

async def BuildCurlRequest(curlRequest:str,dynamicProperty:List):
    try:
        for dp in dynamicProperty:
            curlRequest = curlRequest.replace(dp[1],dp[2])
        return curlRequest
    except Exception as ex:
        raise