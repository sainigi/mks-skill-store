from pydantic import BaseModel
from typing import Optional, List

class Notification(BaseModel):
    Id:int
    NotificationMessage:str
    FromFirstName:str
    ToFirstName:str
    FromLastName:str
    ToLastName:str
    FromUserName:str
    ToUserName:str
    SharedOn:str
    IsRead:bool
    ReadOn:Optional[str]
    NavigationURL:str
    DataId:str
    NotificationType:str
    Title:str
    Description:str
    FromUserImage:Optional[str]
    ToUserImage:Optional[str]
    FromUserImageImageType:Optional[str]
    ToUserImageImageType:Optional[str]