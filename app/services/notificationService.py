from app.models.notification import Notification
from app.commons.sp_helper import exec_store_proc
import logging
import os
from app.commons.utils import stringify_dt

logger = logging.getLogger()

SkillStoreDBCon = os.environ["SkillStoreDB"]

async def GetNotificationListByUserHelper(user_id:str):
    try:
        notifications = await exec_store_proc(sp_name="GetNotificationListByUser",
                                            param_names=["UserId"], 
                                            param_values=[user_id],
                                            conStr=SkillStoreDBCon, 
                                            fetch_data=True) 
        
        notification_List = []
        for notif in notifications:
            notification_List.append(Notification(Id=notif[0],
                                                NotificationMessage=notif[1],
                                                FromFirstName=notif[2],
                                                ToFirstName=notif[3],
                                                FromLastName=notif[4],
                                                ToLastName=notif[5],
                                                FromUserName=notif[6],
                                                ToUserName=notif[7],
                                                SharedOn=stringify_dt(notif[8]) if notif[8] else notif[8],                                                
                                                IsRead=notif[9],
                                                ReadOn=stringify_dt(notif[10]) if notif[10] else notif[10],
                                                NavigationURL=notif[11],
                                                DataId=notif[12],
                                                NotificationType=notif[13],
                                                Title=notif[14],
                                                Description=notif[15],
                                                FromUserImage=notif[18],
                                                ToUserImage=notif[16],
                                                FromUserImageImageType=notif[19],
                                                ToUserImageImageType=notif[17]
                                                  ).dict())        
        
        return notification_List
    except Exception as ex:
        raise

async def UpdateNotificationReadStatusHelper(notificationId:int, user_id:str):
    try:
        await exec_store_proc(sp_name="UpdateNotificationReadStatus",
                                param_names=["UserId","NotificationId"], 
                                param_values=[user_id,notificationId],
                                conStr=SkillStoreDBCon, 
                                fetch_data=False)
    except Exception as ex:
        raise