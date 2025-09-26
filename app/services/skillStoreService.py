from typing import List
from app.models.skillStore import Filter,SkillStore,UpdateStatus,SkillTag,\
    SkillStoreDetail,SkillStoreLikes,SkillStoreUsed,SkillStoreVersion,\
        SkillStoreDetailVersion,SkillFunction,SkillSubFunction,DefaultChatbotConfiguration,\
            ChatbotConfiguration,Additive,SkillStoreStatus,DisableFollowupQuestions,\
                CreateUpdateSkillStore,KeyValuePair
from app.commons.sp_helper import exec_store_proc,exec_stored_procedure_multiple_sets
import logging
import os
from app.commons.utils import stringify_dt

logger = logging.getLogger()

SkillStoreDBCon = os.environ["SkillStoreDB"]

async def GetFunctionHelper(LookupDepartmentId:int):
    try:
        function = await exec_store_proc(sp_name="GetFunction",
                                            param_names=["LookupDepartmentId"], 
                                            param_values=[LookupDepartmentId],
                                            conStr=SkillStoreDBCon, 
                                            fetch_data=True)
        logger.debug(f'{function}')
        function_list=[]
        for sl in function:
            function_list.append(Filter(
                Id=sl[0],
                Name=sl[1]
            ).dict())
        return function_list
    except Exception as ex:
        raise

async def GetSubFunctionHelper(FunctionIds:List[int]):
    try:
        Ids = []
        for id in FunctionIds:
            Ids.append((id,))
        subFunction = await exec_store_proc(sp_name="GetSubFunction",
                                            param_names=["FunctionIds"], 
                                            param_values=[Ids],
                                            conStr=SkillStoreDBCon, 
                                            fetch_data=True)
        logger.debug(f'{subFunction}')
        subFunction_list=[]
        for sl in subFunction:
            subFunction_list.append(Filter(
                Id=sl[0],
                Name=sl[1]
            ).dict())
        return subFunction_list
    except Exception as ex:
        raise

async def GetSkillTagsHelper():
    try:
        skillTag = await exec_store_proc(sp_name="GetSkillTags",
                                            param_names=[], 
                                            param_values=[],
                                            conStr=SkillStoreDBCon, 
                                            fetch_data=True)
        logger.debug(f'{skillTag}')
        skillTag_list=[]
        for sl in skillTag:
            skillTag_list.append(Filter(
                Id=sl[0],
                Name=sl[1]
            ).dict())
        return skillTag_list
    except Exception as ex:
        raise

async def GetDepartmentHelper():
    try:
        Departments = await exec_store_proc(sp_name="GetDepartments",
                                            param_names=[], 
                                            param_values=[],
                                            conStr=SkillStoreDBCon, 
                                            fetch_data=True)
        logger.debug(f'{Departments}')
        Departments_list=[]
        for sl in Departments:
            Departments_list.append(Filter(
                Id=sl[0],
                Name=sl[1]
            ).dict())
        return Departments_list
    except Exception as ex:
        raise

async def GetSkillScopeHelper():
    try:
        skillScope = await exec_store_proc(sp_name="GetSkillScope",
                                            param_names=[], 
                                            param_values=[],
                                            conStr=SkillStoreDBCon, 
                                            fetch_data=True)
        logger.debug(f'{skillScope}')
        skillScope_list=[]
        for sl in skillScope:
            skillScope_list.append(Filter(
                Id=sl[0],
                Name=sl[1]
            ).dict())
        return skillScope_list
    except Exception as ex:
        raise

async def InsertUpdateLikeStatusHelper(status:UpdateStatus,user_id:str):
    try:
        await exec_store_proc(sp_name="InsertUpdateLikeStatus",
                                param_names=["IsLiked","LikedBy","SkillStoreId"], 
                                param_values=[status.Status,user_id,status.SkillStoreId],
                                conStr=SkillStoreDBCon, 
                                fetch_data=False)
    except Exception as ex:
        raise

async def AddUpdateUsersSkillShowFollowupQuestionStateHelper(status:DisableFollowupQuestions,user_id:str):
    try:
        await exec_store_proc(sp_name="AddUpdateUsersSkillShowFollowupQuestionState",
                                param_names=["UserId","SkillStoreId","ShowStatus"], 
                                param_values=[user_id,status.SkillStoreId,status.Status],
                                conStr=SkillStoreDBCon, 
                                fetch_data=False)
    except Exception as ex:
        raise

async def InsertUpdateUsedStatusHelper(SkillStoreId:int,user_id:str):
    try:
        await exec_store_proc(sp_name="InsertUpdateUsedStatus",
                                param_names=["UsedBy","SkillStoreId"], 
                                param_values=[user_id,SkillStoreId],
                                conStr=SkillStoreDBCon, 
                                fetch_data=False)
    except Exception as ex:
        raise

async def GetSkillStoreHelper(user_id:str):
    try:
        skillStore,skillTag,skillFunction,skillSubFunction,chatbotBaseConfig,dynamicParam = await exec_stored_procedure_multiple_sets(sp_name="GetSkillStores",
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
        
        skillStore_List=[]
        for ssl in skillStore:
            skillstore = None
            skillTag_dict = [x for x in skillTag if x[0] == ssl[0]]
            skillfunction_dict = [x for x in skillFunction if x[0] == ssl[0]]
            skillsubfunction_dict = [x for x in skillSubFunction if x[0] == ssl[0]]
            chatbotConfig_dict = [x for x in chatbotConfig_List if x["SkillStoreId"] == ssl[0]]
            if len(chatbotConfig_dict) == 0:
                chatbotConfig_dict = [x for x in chatbotConfig_List if x["IsDefault"] == True]
            skillTag_List = []
            skillFunction_List = []
            skillSubFunction_List = []
            for sa in skillTag_dict:
                skillTag_List.append(SkillTag(
                    Id=sa[1],
                    Name=sa[2]
                    ).dict())
            
            for sa in skillfunction_dict:
                skillFunction_List.append(SkillFunction(
                    Id=sa[1],
                    Name=sa[2]
                    ).dict())
                
            for sa in skillsubfunction_dict:
                skillSubFunction_List.append(SkillSubFunction(
                    Id=sa[1],
                    Name=sa[2]
                    ).dict())
            
            skillstore = SkillStore(
                Id=ssl[0],
                Name=ssl[1],
                Description=ssl[2],
                SkillScope=ssl[3],
                DepartmentName=ssl[4],
                Acurracy=ssl[5],
                AvgExecutionTime=ssl[6],
                VersionName=ssl[7],
                IsLiked=ssl[8],
                IsUsed=ssl[9],
                LikeCount=ssl[10],
                UsedCount=ssl[11],
                ModifiedOn=stringify_dt(ssl[12]) if ssl[12] else ssl[12],
                ShortDescription=ssl[13],
                IsThirdPartyAITool=ssl[14],
                ChatBotURL=ssl[15],
                IsUsingWrapperAPIURL=ssl[16],
                WrapperAPIURL=ssl[17],
                IsChatbotTestable=chatbotConfig_dict[0].get("IsChatbotTestable"),
                SecurityGroupId=chatbotConfig_dict[0].get("SecurityGroupId"),
                ChatbotConfiguration=chatbotConfig_dict[0] if ssl[14] == False else None,
                skillTags=skillTag_List,
                functions=skillFunction_List,
                subFunctions=skillSubFunction_List
                ).dict()
            skillStore_List.append(skillstore)
            
        return skillStore_List
    except Exception as ex:
        raise

async def GetSkillStoreByIdHelper(SkillStoreId:int,user_id:str):
    try:
        skillStore,skillTag,skillFunction,skillSubFunction,skillLikes,skillUsed,SkillVersions,VersionDetails,skillTagVersions,SkillFunctionVersions,SkillSubFunctionsVersions,chatbotBaseConfig,dynamicParam = await exec_stored_procedure_multiple_sets(sp_name="GetSkillStoreById",
                                            param_names=["UserId","SkillStoreId"], 
                                            param_values=[user_id,SkillStoreId],
                                            conStr=SkillStoreDBCon, 
                                            fetch_data=True)
        
        if skillStore == None or len(skillStore) == 0:
            return None
        
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
        
        skillstore = None        
        
        skillTag_List = []
        skillFunction_List = []
        skillSubFunction_List = []
        skillLike_List = []
        skillUsed_List = []
        version_List = []
        for sa in skillTag:
            skillTag_List.append(SkillTag(
                Id=sa[1],
                Name=sa[2]
                ).dict())
        
        for sa in skillFunction:
            skillFunction_List.append(SkillFunction(
                Id=sa[1],
                Name=sa[2]
                ).dict())
            
        for sa in skillSubFunction:
            skillSubFunction_List.append(SkillSubFunction(
                Id=sa[1],
                Name=sa[2]
                ).dict())
        
        for sa in skillLikes:
            skillLike_List.append(SkillStoreLikes(
                Id=sa[1],
                firstName=sa[2],
                lastName=sa[3],
                likedBy=sa[4],
                isLiked=sa[5]
                ).dict())
            
        for sa in skillUsed:
            skillUsed_List.append(SkillStoreUsed(
                Id=sa[1],
                firstName=sa[2],
                lastName=sa[3],
                UsedBy=sa[4]
                ).dict())
                
        for sv in SkillVersions:
            versionDetail = None
            versionDetails_dict = [x for x in VersionDetails if x[0] == sv[2]]
            skillTag_version_Dict = [x for x in skillTagVersions if x[0] == sv[2]]
            skillFunction_version_Dict = [x for x in SkillFunctionVersions if x[0] == sv[2]]
            skillSubFunction_version_Dict = [x for x in SkillSubFunctionsVersions if x[0] == sv[2]]
            skillTag_version_List = []
            skillFunction_version_List = []
            skillSubFunction_version_List = []
            
            for sa in skillTag_version_Dict:
                skillTag_version_List.append(SkillTag(
                    Id=sa[2],
                    Name=sa[3]
                    ).dict())
            
            for sa in skillFunction_version_Dict:
                skillFunction_version_List.append(SkillFunction(
                    Id=sa[2],
                    Name=sa[3]
                    ).dict())
            
            for sa in skillSubFunction_version_Dict:
                skillSubFunction_version_List.append(SkillSubFunction(
                    Id=sa[2],
                    Name=sa[3]
                    ).dict())
            
            if len(versionDetails_dict) > 0:
                versionDetail = SkillStoreDetailVersion(
                Id=versionDetails_dict[0][1],
                Name=versionDetails_dict[0][2],
                Description=versionDetails_dict[0][3],
                SkillScope=versionDetails_dict[0][4],
                DepartmentName=versionDetails_dict[0][5],
                Acurracy=versionDetails_dict[0][6],
                AvgExecutionTime=versionDetails_dict[0][7],
                VersionName=versionDetails_dict[0][8],
                Owner=versionDetails_dict[0][9],
                CreatedBy=versionDetails_dict[0][10],
                CreatedOn=stringify_dt(versionDetails_dict[0][11]),
                PublishedOn=stringify_dt(versionDetails_dict[0][12]),
                ContactName=versionDetails_dict[0][13],
                ContactEmailId=versionDetails_dict[0][14],
                IsLiked=versionDetails_dict[0][15],
                IsUsed=versionDetails_dict[0][16],
                LikeCount=versionDetails_dict[0][17],
                UsedCount=versionDetails_dict[0][18],
                ownerUserImage=versionDetails_dict[0][19],
                ownerUserImageMimeType=versionDetails_dict[0][20],
                creatorUserImage=versionDetails_dict[0][21],
                creatorUserImageMimeType=versionDetails_dict[0][22],
                IsThirdPartyAITool=versionDetails_dict[0][23],
                ChatBotURL=versionDetails_dict[0][24],
                IsUsingWrapperAPIURL=versionDetails_dict[0][25],
                WrapperAPIURL=versionDetails_dict[0][26],
                skillTags=skillTag_version_List,
                functions=skillFunction_version_List,
                subFunctions=skillSubFunction_version_List,
                ).dict()
                
                version_List.append(SkillStoreVersion(
                    versionName=sv[1],
                    VersionId=sv[2],
                    versionDetail=versionDetail
                ).dict())
        logger.debug(f'{skillStore}') 
        skillstore = SkillStoreDetail(
            Id=skillStore[0][0],
            Name=skillStore[0][1],
            Description=skillStore[0][2],
            SkillScope=skillStore[0][3],
            DepartmentName=skillStore[0][4],
            Acurracy=skillStore[0][5],
            AvgExecutionTime=skillStore[0][6],
            VersionName=skillStore[0][7],
            Owner=skillStore[0][8],
            CreatedBy=skillStore[0][9],
            CreatedOn=stringify_dt(skillStore[0][10]),
            PublishedOn=stringify_dt(skillStore[0][11]),
            ContactName=skillStore[0][12],
            ContactEmailId=skillStore[0][13],
            IsLiked=skillStore[0][14],
            IsUsed=skillStore[0][15],
            LikeCount=skillStore[0][16],
            UsedCount=skillStore[0][17],
            ModifiedOn=stringify_dt(skillStore[0][18]) if skillStore[0][18] else skillStore[0][18],
                ShortDescription=skillStore[0][19],
            IsChatbotTestable=chatbotConfig.get("IsChatbotTestable"),
            SecurityGroupId=chatbotConfig.get("SecurityGroupId"),
            OwnerUserImage=skillStore[0][20],
            OwnerUserImageMimeType=skillStore[0][21],
            CreatorUserImage=skillStore[0][22],
            CreatorUserImageMimeType=skillStore[0][23],
            IsThirdPartyAITool=skillStore[0][24],
            ChatBotURL=skillStore[0][25],
            IsUsingWrapperAPIURL=skillStore[0][26],
            WrapperAPIURL=skillStore[0][27],
            ChatbotConfiguration=chatbotConfig if skillStore[0][24] == False else None,
            skillTags=skillTag_List,
            functions=skillFunction_List,
            subFunctions=skillSubFunction_List,
            likes=skillLike_List,
            used=skillUsed_List,
            versions=version_List
            ).dict()
        logger.debug(f'{skillstore}')            
        return skillstore
    except Exception as ex:
        raise

async def BuildCurlRequest(curlRequest:str,dynamicProperty:List):
    try:
        for dp in dynamicProperty:
            curlRequest = curlRequest.replace(dp[1],dp[2])
        return curlRequest
    except Exception as ex:
        raise

async def GetDefaultChatbotConfigHelper():
    try:
        chatbotBaseConfig,dynamicParam = await exec_stored_procedure_multiple_sets(sp_name="GetDefaultChatbotConfig",
                                            param_names=[], 
                                            param_values=[],
                                            conStr=SkillStoreDBCon, 
                                            fetch_data=True)
        
        dynamicParam_dict = [x for x in dynamicParam if x[0] == chatbotBaseConfig[0][0]]
        curlRequest = await BuildCurlRequest(curlRequest=chatbotBaseConfig[0][7],dynamicProperty=dynamicParam_dict)
        
        chatbotConfig = DefaultChatbotConfiguration(Id=chatbotBaseConfig[0][0],
                                            IsDefault=chatbotBaseConfig[0][1],
                                            InputType=chatbotBaseConfig[0][2],
                                            OutputType=chatbotBaseConfig[0][3],
                                            FileType=chatbotBaseConfig[0][4],
                                            ChatbotUIView=chatbotBaseConfig[0][5],
                                            LastMessagesCount=chatbotBaseConfig[0][6],
                                            ChatGPTVersion=chatbotBaseConfig[0][8],
                                            IsChatbotTestable=chatbotBaseConfig[0][9],
                                            UserMessageFormat=chatbotBaseConfig[0][10],
                                            AssistantMessageFormat=chatbotBaseConfig[0][10].replace("user","assistant").replace("$Message","$replyMsg") if chatbotBaseConfig[0][10] else None,
                                            SecurityGroupId=chatbotBaseConfig[0][11],                                            
                                            ShowCitation=chatbotBaseConfig[0][12],
                                            IsActive=chatbotBaseConfig[0][13],
                                            ShowFollowUpQuestions=chatbotBaseConfig[0][14], 
                                            DisableFollowUpQuestions=chatbotBaseConfig[0][15],                        
                                            IsUsingWrapperAPIURL=chatbotBaseConfig[0][16],                        
                                            WrapperAPIURL=chatbotBaseConfig[0][17],                        
                                            CitationURL=chatbotBaseConfig[0][18],                        
                                            CitationParams=chatbotBaseConfig[0][19], 
                                            ImageURL=chatbotBaseConfig[0][20],                        
                                            ImageParams=chatbotBaseConfig[0][21],                        
                                            CurlRequestString=curlRequest
                                            ).dict()
        return chatbotConfig
    except Exception as ex:
        raise

async def GetAdditivesHelper():
    try:
        additive = await exec_store_proc(sp_name="GetAdditives",
                                            param_names=[], 
                                            param_values=[],
                                            conStr=SkillStoreDBCon, 
                                            fetch_data=True)
        logger.debug(f'{additive}')
        additive_list=[]
        for sl in additive:
            additive_list.append(Additive(
                Id=sl[0],
                Name=sl[1],
                Value=sl[2]
            ).dict())
        return additive_list
    except Exception as ex:
        raise

async def CheckSkillsAvailabilityHelper():
    try:
        skills = await exec_store_proc(sp_name="CheckSkillsAvailability",
                                            param_names=[], 
                                            param_values=[],
                                            conStr=SkillStoreDBCon, 
                                            fetch_data=True)
        skills_List = []
        logger.debug(f'{skills}')
        for skill in skills:        
            skills_List.append(SkillStoreStatus(Id=skill[0],
                                                Name=skill[1],
                                                ISDefault=skill[2],
                                                IsActive=skill[3]
                                                ).dict())
        return skills_List
    except Exception as ex:
        raise

async def CreateSkillHelper(data:CreateUpdateSkillStore,user_id:str):
    try:
        functions = []
        subFunctions = []
        tags = []
        owners = []
        contacts = []
        dynamicProperties = []
        
        for id in data.functions:
            functions.append((id,))
        
        for id in data.subFunctions:
            subFunctions.append((id,))
        
        for text in data.tags:
            tags.append((text,))
            
        for text in data.Owner:
            owners.append((text,))
        
        for text in data.Contact:
            contacts.append((text,))
        
        for text in data.DynamicProperties:
            dynamicProperties.append((text.key,text.Value))
            
        await exec_store_proc(sp_name="InsertSkillStore",
                                param_names=["UserId","Name","ShortDescription",
                                             "Description","LookupDepartmentId","LookupSkillScopeId",
                                             "PublishOn","Acurracy","AvgExecutionTime",
                                             "IsThirdPartyAITool","LookupFunction","LookupSubFunction","Tags",
                                             "Owner","Contact","DynamicProperties","InputType","OutputType","LastMessagesCount",
                                             "ChatGPTVersion","IsChatbotTestable","ShowCitation",
                                             "ShowFollowUpQuestions","CurlRequestString","UserAssistantMessageFormat",
                                             "ChatbotUIView","ChatBotURL","FileType","SecurityGroupId",
                                             "IsUsingWrapperAPIURL","WrapperAPIURL","CitationURL",
                                             "CitationParams","ImageURL","ImageParams"], 
                                param_values=[user_id,data.Name,data.ShortDescription,data.Description,
                                              data.DepartmentNameId,data.LookupSkillScopeId,data.PublishOn,data.Acurracy,
                                              data.AvgExecutionTime,data.IsThirdPartyAITool,functions,
                                              subFunctions,tags,owners,contacts,dynamicProperties,data.InputType,data.OutputType,
                                              data.LastMessagesCount,data.ChatGPTVersion,data.IsChatbotTestable,data.ShowCitation,
                                              data.ShowFollowUpQuestions,data.CurlRequestString,data.UserAssistantMessageFormat,
                                              data.ChatbotUIView,data.ChatBotURL,data.FileType,data.SecurityGroupId,
                                              data.IsUsingWrapperAPIURL,data.WrapperAPIURL,data.CitationURL,data.CitationParams,
                                              data.ImageURL,data.ImageParams],
                                conStr=SkillStoreDBCon, 
                                fetch_data=False)
    except Exception as ex:
        raise

async def UpdateSkillHelper(data:CreateUpdateSkillStore,SkillStoreId:int,user_id:str):
    try:
        functions = []
        subFunctions = []
        tags = []
        owners = []
        contacts = []
        dynamicProperties = []
        for id in data.functions:
            functions.append((id,))
        
        for id in data.subFunctions:
            subFunctions.append((id,))
        
        for text in data.tags:
            tags.append((text,))
        
        for text in data.Owner:
            owners.append((text,))
        
        for text in data.Contact:
            contacts.append((text,))
        
        for text in data.DynamicProperties:
            dynamicProperties.append((text.key,text.Value))
            
        await exec_store_proc(sp_name="UpdateSkillStore",
                                param_names=["SkillStoreId","UserId","Name","ShortDescription",
                                             "Description","LookupDepartmentId","LookupSkillScopeId",
                                             "PublishOn","Acurracy","AvgExecutionTime",
                                             "IsThirdPartyAITool","LookupFunction","LookupSubFunction","Tags",
                                             "Owner","Contact","DynamicProperties","InputType","OutputType","LastMessagesCount",
                                             "ChatGPTVersion","IsChatbotTestable","ShowCitation",
                                             "ShowFollowUpQuestions","CurlRequestString","UserAssistantMessageFormat",
                                             "ChatbotUIView","ChatBotURL","FileType","SecurityGroupId",
                                             "IsUsingWrapperAPIURL","WrapperAPIURL","CitationURL","CitationParams"
                                             ,"ImageURL","ImageParams"], 
                                param_values=[SkillStoreId,user_id,data.Name,data.ShortDescription,data.Description,
                                              data.DepartmentNameId,data.LookupSkillScopeId,data.PublishOn,data.Acurracy,
                                              data.AvgExecutionTime,data.IsThirdPartyAITool,functions,
                                              subFunctions,tags,owners,contacts,dynamicProperties,data.InputType,data.OutputType,
                                              data.LastMessagesCount,data.ChatGPTVersion,data.IsChatbotTestable,data.ShowCitation,
                                              data.ShowFollowUpQuestions,data.CurlRequestString,data.UserAssistantMessageFormat,
                                              data.ChatbotUIView,data.ChatBotURL,data.FileType,data.SecurityGroupId,
                                              data.IsUsingWrapperAPIURL,data.WrapperAPIURL,data.CitationURL,data.CitationParams
                                              ,data.ImageURL,data.ImageParams],
                                conStr=SkillStoreDBCon, 
                                fetch_data=False)
    except Exception as ex:
        raise

async def DeleteSkillHelper(SkillStoreId:int,user_id:str):
    try:
        await exec_store_proc(sp_name="DeleteSkill",
                                            param_names=["SkillStoreId","UserId"], 
                                            param_values=[SkillStoreId,user_id],
                                            conStr=SkillStoreDBCon, 
                                            fetch_data=False)
    except Exception as ex:
        raise

async def GetSkillDetailsHelper(SkillStoreId:int):
    try:
        skills,LookupFunction,LookupSubFunction,LookupSkillTag,Contact,Owner,DynamicProperties = await exec_stored_procedure_multiple_sets(sp_name="GetSkillDetails",
                                            param_names=["SkillStoreId"], 
                                            param_values=[SkillStoreId],
                                            conStr=SkillStoreDBCon, 
                                            fetch_data=True)
        Skill = None
        lf_List = []
        lsf_List = []
        lst_List = []
        c_List = []
        o_List = []
        dp_List = []
        logger.debug(f'{skills}')  
        
        for lf in LookupFunction:
            lf_List.append(lf[0])
        
        for lsf in LookupSubFunction:
            lsf_List.append(lsf[0])

        for lst in LookupSkillTag:
            lst_List.append(lst[0])
            
        for c in Contact:
            c_List.append(c[0])
            
        for o in Owner:
            o_List.append(o[0])

        for dp in DynamicProperties:
            dp_List.append(KeyValuePair(key=dp[0],
                                        Value=dp[1]).dict())
            
        Skill = CreateUpdateSkillStore(Name=skills[0][0],
                                            Description=skills[0][1],
                                            LookupSkillScopeId=skills[0][2],
                                            PublishOn=stringify_dt(skills[0][3]) if skills[0][3] else skills[0][3],
                                            Acurracy=skills[0][4],
                                            AvgExecutionTime=skills[0][5],
                                            DepartmentNameId=skills[0][6],
                                            ShortDescription=skills[0][7],
                                            IsThirdPartyAITool=skills[0][8],
                                            ChatBotURL=skills[0][9],
                                            InputType=skills[0][10],
                                            OutputType=skills[0][11],
                                            FileType=skills[0][12],
                                            ChatbotUIView=skills[0][13],
                                            LastMessagesCount=skills[0][14],
                                            ChatGPTVersion=skills[0][15],
                                            IsChatbotTestable=skills[0][16],
                                            ShowCitation=skills[0][17],
                                            ShowFollowUpQuestions=skills[0][18],
                                            CurlRequestString=skills[0][19],
                                            UserAssistantMessageFormat=skills[0][20],
                                            SecurityGroupId=skills[0][21],
                                            IsUsingWrapperAPIURL=skills[0][22],
                                            WrapperAPIURL=skills[0][23],
                                            CitationURL=skills[0][24],
                                            CitationParams=skills[0][25],
                                            ImageURL=skills[0][26],
                                            ImageParams=skills[0][27],
                                            functions=lf_List,
                                            subFunctions=lsf_List,
                                            tags=lst_List,
                                            Owner=o_List,
                                            Contact=c_List,
                                            DynamicProperties=dp_List 
                                            ).dict()
        return Skill
    except Exception as ex:
        raise