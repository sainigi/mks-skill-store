from pydantic import BaseModel
from typing import Optional, List

class Filter(BaseModel):
    Id: int
    Name: str
    

class Additive(BaseModel):
    Id: int
    Name: str
    Value:str

class SkillTag(BaseModel):
    Id: int
    Name: str
    
class SkillFunction(BaseModel):
    Id: int
    Name: str

class SkillSubFunction(BaseModel):
    Id: int
    Name: str

class KeyValuePair(BaseModel):
    key: str
    Value: str
    
class SkillResource(BaseModel):
    Id: int
    ResourceId:str
    ResourceName:str

class ChatbotConfiguration(BaseModel):
    SkillStoreId:Optional[int]
    Id:int
    IsDefault:bool
    InputType:str
    OutputType:str
    FileType:Optional[str]
    ChatbotUIView:Optional[str]
    LastMessagesCount:Optional[int]
    CurlRequestString:str
    ChatGPTVersion:str
    IsChatbotTestable:bool
    UserMessageFormat:Optional[str]
    AssistantMessageFormat:Optional[str]
    SecurityGroupId:Optional[str]
    ShowCitation:bool
    ShowFollowUpQuestions:bool
    DisableFollowUpQuestions:bool
    CitationURL:Optional[str]
    CitationParams:Optional[str]
    ImageURL:Optional[str]
    ImageParams:Optional[str]
    
class DefaultChatbotConfiguration(BaseModel):
    Id:int
    IsDefault:bool
    InputType:str
    OutputType:str
    FileType:Optional[str]
    ChatbotUIView:Optional[str]
    LastMessagesCount:Optional[int]
    CurlRequestString:str
    ChatGPTVersion:str
    IsChatbotTestable:bool
    UserMessageFormat:Optional[str]
    AssistantMessageFormat:Optional[str]
    SecurityGroupId:Optional[str]
    ShowCitation:bool
    IsActive:bool
    ShowFollowUpQuestions:bool
    DisableFollowUpQuestions:bool
    IsUsingWrapperAPIURL:Optional[bool]
    WrapperAPIURL:Optional[str]
    CitationURL:Optional[str]
    CitationParams:Optional[str]
    ImageURL:Optional[str]
    ImageParams:Optional[str]
    
class DisableFollowupQuestions(BaseModel):
    SkillStoreId:int
    Status:bool

class SkillStore(BaseModel):
    Id:int
    Name:str
    Description:str
    SkillScope:str
    DepartmentName:str
    Acurracy:float
    AvgExecutionTime:int
    VersionName:str
    IsLiked:bool
    IsUsed:bool
    LikeCount:int
    UsedCount:int
    IsChatbotTestable:bool
    ModifiedOn:Optional[str]
    ShortDescription:Optional[str]
    SecurityGroupId:Optional[str]
    IsThirdPartyAITool:bool
    ChatBotURL:Optional[str]
    IsUsingWrapperAPIURL:Optional[bool]
    WrapperAPIURL:Optional[str]
    ChatbotConfiguration:Optional[ChatbotConfiguration]
    skillTags:List[SkillTag]
    functions:List[SkillFunction]
    subFunctions:List[SkillSubFunction]
    SkillResources:Optional[List[SkillResource]]
    Owner:Optional[List[str]]
    Contact:Optional[List[str]]

class UpdateStatus(BaseModel):
    SkillStoreId:int
    Status:bool
    
class SkillStoreStatus(BaseModel):
    Id:int
    Name:str
    ISDefault:bool
    IsActive:bool

class SkillStoreLikes(BaseModel):
    Id:int
    firstName:str
    lastName:Optional[str]
    likedBy:str
    isLiked:bool

class SkillStoreUsed(BaseModel):
    Id:int
    firstName:str
    lastName:Optional[str]
    UsedBy:str

class SkillStoreDetailVersion(BaseModel):
    Id:int
    Name:str
    Description:str
    SkillScope:str
    DepartmentName:str
    Acurracy:float
    AvgExecutionTime:int
    VersionName:str
    Owner:str
    CreatedBy:str
    CreatedOn:str
    PublishedOn:str
    ContactName:str
    ContactEmailId:str
    IsLiked:bool
    IsUsed:bool
    LikeCount:int
    UsedCount:int
    skillTags:List[SkillTag]
    functions:List[SkillFunction]
    subFunctions:List[SkillSubFunction]
    OwnerUserImage:Optional[str]
    OwnerUserImageMimeType:Optional[str]
    CreatorUserImage:Optional[str]
    CreatorUserImageMimeType:Optional[str]    
    IsThirdPartyAITool:bool
    ChatBotURL:Optional[str]
    IsUsingWrapperAPIURL:Optional[bool]
    WrapperAPIURL:Optional[str]

class SkillStoreVersion(BaseModel):
    versionName:str
    VersionId:int
    versionDetail:SkillStoreDetailVersion
  
class SkillStoreDetail(BaseModel):
    Id:int
    Name:str
    Description:str
    SkillScope:str
    DepartmentName:str
    Acurracy:float
    AvgExecutionTime:int
    VersionName:str
    Owner:str
    CreatedBy:str
    CreatedOn:str
    PublishedOn:str
    ContactName:str
    ContactEmailId:str
    IsLiked:bool
    IsUsed:bool
    LikeCount:int
    UsedCount:int
    ModifiedOn:Optional[str]
    ShortDescription:Optional[str]
    IsChatbotTestable:bool
    SecurityGroupId:Optional[str]
    OwnerUserImage:Optional[str]
    OwnerUserImageMimeType:Optional[str]
    CreatorUserImage:Optional[str]
    CreatorUserImageMimeType:Optional[str]    
    IsThirdPartyAITool:bool
    ChatBotURL:Optional[str]
    IsUsingWrapperAPIURL:Optional[bool]
    WrapperAPIURL:Optional[str]
    ChatbotConfiguration:Optional[ChatbotConfiguration]
    skillTags:List[SkillTag]
    functions:List[SkillFunction]
    subFunctions:List[SkillSubFunction]
    SkillResources:Optional[List[SkillResource]]
    likes:Optional[List[SkillStoreLikes]]
    used:Optional[List[SkillStoreUsed]]
    versions:Optional[List[SkillStoreVersion]]

class CreateUpdateSkillStore(BaseModel):
    Name:str
    ShortDescription:Optional[str]
    Description:str    
    DepartmentNameId:int
    LookupSkillScopeId:int
    PublishOn:str
    Acurracy:float
    AvgExecutionTime:float
    IsThirdPartyAITool:bool
    functions:Optional[List[int]]
    subFunctions:Optional[List[int]]
    tags:Optional[List[str]]
    Owner:Optional[List[str]]
    Contact:Optional[List[str]]
    DynamicProperties:Optional[List[KeyValuePair]]
    SkillResources:Optional[List[SkillResource]]
    InputType:Optional[str]
    OutputType:Optional[str]
    LastMessagesCount:Optional[int]
    ChatGPTVersion:Optional[str]
    IsChatbotTestable:Optional[bool]
    ShowCitation:Optional[bool]
    ShowFollowUpQuestions:Optional[bool]
    CurlRequestString:Optional[str]
    UserAssistantMessageFormat:Optional[str]
    ChatbotUIView:Optional[str]    
    ChatBotURL:Optional[str]
    FileType:Optional[str]
    SecurityGroupId:Optional[str]
    IsUsingWrapperAPIURL:Optional[bool]
    WrapperAPIURL:Optional[str]
    CitationURL:Optional[str]
    CitationParams:Optional[str]
    ImageURL:Optional[str]
    ImageParams:Optional[str]
    
class SkillResourceCost(BaseModel):
    SkillId:int
    DaysBack:int 