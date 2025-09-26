from pydantic import BaseModel
from typing import Optional, List
from app.models.skillStore import Filter

class PromptSystemGeneratedInput(BaseModel):
    ModelAPIURL:str
    PromptStyle:str
    WordCount:Optional[int]
    PromptGenerated:bool
    PromptText:str
    Status:str

class PromptUserInput(BaseModel):
    SkillStoreId:Optional[int]
    IsDisclaimerAccepted:Optional[bool]
    DisclaimerText:Optional[str]
    Title:str
    ShortDescription:str
    PromptBackground:Optional[str]
    DesiredPromptOutput:Optional[str]
    SourceOnInputOutput:Optional[str]
    IsConfidentialAccepted:Optional[bool]
    ConfidentialText:Optional[str]
    LookupDepartmentId:Optional[int]    
    IsPublic:bool
    CardImage_Base64:Optional[str]
    ImageName:Optional[str]
    MimeType:Optional[str]
    WordCount:Optional[int]
    LookupCreativityId:Optional[int]
    Result:Optional[str]
    functions:Optional[List[int]]
    subFunctions:Optional[List[int]]
    tags:Optional[List[str]]
    PromptSystemGeneratedInputs:Optional[List[PromptSystemGeneratedInput]]

class Comments(BaseModel):
    ParentCommentId:Optional[int]
    PromptUserInputId:int
    Comment:str
    
class UpdateStatus(BaseModel):
    PromptUserInputId:int
    Status:bool

class BulkImportPrompts(BaseModel):
    Title:str
    ShortDescription:str

class BulkImportPromptsV2(BaseModel):
    Title:str
    ShortDescription:str
    SkillStoreId:int

class PromptSystemGeneratedInputList(BaseModel):
    Id:int
    ModelAPIURL:str
    PromptStyle:str
    WordCount:Optional[int]
    PromptGenerated:bool
    PromptText:str
    Status:str
    
class PromptUserInputComments(BaseModel):
    Id:int    
    Comment:str   
    CommentDate:str
    FirstName:str
    LastName:str
    ParentCommentId:Optional[int]
    userImage:Optional[str]
    userImageMimeType:Optional[str]

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

class PromptUserInputList(BaseModel):
    Id:int
    SkillStoreId:Optional[int]
    SkillStoreName:Optional[str]
    SecurityGroupId:Optional[str]
    SkillStoreShortDescription:Optional[str]
    IsDisclaimerAccepted:bool
    DisclaimerText:Optional[str]
    Title:str
    ShortDescription:str
    PromptBackground:Optional[str]
    DesiredPromptOutput:Optional[str]
    SourceOnInputOutput:Optional[str]
    IsConfidentialAccepted:bool
    ConfidentialText:Optional[str]
    LookupDepartmentId:Optional[int]  
    DepartmentName:Optional[str]
    IsPublic:bool
    CardImage_Base64:Optional[str]
    ImageName:Optional[str]
    MimeType:Optional[str]
    IsViewed:bool
    IsCommented:bool
    IsStared:bool
    ViewCount:int
    CommentCount:int
    CreatedByFirstName:str
    CreatedByLastName:str
    CreatedById:str
    WordCount:Optional[int]
    CreativityName:Optional[str]
    LookupCreativityId:Optional[int]
    IsReadonlyAccess:bool
    IsLiked:bool
    LikeCount:int
    IsMyPrompt:bool
    IsSharedPrompt:bool
    IsImportedPrompt:bool
    CreatedOn:str
    LastUpdatedOn:str
    Result:Optional[str]
    userImage:Optional[str]
    userImageMimeType:Optional[str]
    IsUsingWrapperAPIURL:Optional[bool]
    WrapperAPIURL:Optional[str]
    functions:Optional[List[Filter]]
    subFunctions:Optional[List[Filter]]
    tags:Optional[List[Filter]]    
    ChatbotConfiguration:Optional[ChatbotConfiguration]
    PromptSystemGeneratedInputs:Optional[List[PromptSystemGeneratedInputList]]
    comments:Optional[List[PromptUserInputComments]]
    Users:Optional[List[str]]

class Skills(BaseModel):
    Id: int
    Name: str
    SecurityGroupId:Optional[str]
    ChatbotConfiguration:Optional[ChatbotConfiguration]