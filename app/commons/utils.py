from datetime import datetime, timedelta, timezone
from dateutil import parser, tz
from typing import Dict, List
from uuid import UUID
import pytz

def format_date(dt: str):
    try:
        return dt[:-3]+'Z'
    except:
        raise


def get_now_date_time():
    try:
        now = datetime.now()
        date_str = now.strftime('%Y-%m-%dT%H:%M:%S.%f')
        return format_date(date_str)
    except:
        raise

def sub_dict(dictionary: Dict, columns: List):
    try:
        return {key: dictionary[key] for key in columns}
    except:
        raise

def stringify_dt(dt: datetime):
    return dt.strftime('%m/%d/%Y %H:%M:%S %p')

def get_latest_date(date_list):
    try:
        parse_dt_list = []
        for dt in date_list:
            parse_dt= parser.parse(dt)
            if parse_dt.tzinfo is None:
                parse_dt = parse_dt.replace(tzinfo=tz.tzutc())
            parse_dt_list.append(parse_dt)

        latest_date = max(parse_dt_list)
        return format_date(latest_date.strftime("%Y-%m-%dT%H:%M:%S.%f"))
    except:
        raise

def isValidUUID(id_):
    try:
        UUID(id_, version=4)
        return True
    except ValueError:
        return False

def get_now_date():
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    return date_str


def get_now_date_time_by_timezone(time_zone):
    now_in_tz = datetime.now(pytz.timezone(time_zone))
    return now_in_tz


def get_execute_at(time_zone):
    now_in_tz = get_now_date_time_by_timezone(time_zone)
    # logger.debug(f"Current Local Time in {time_zone} : {now_in_tz.strftime('%m/%d/%Y %H:%M:%S %p')}")
    today12am_in_tz = pytz.timezone(time_zone).localize(datetime.combine(now_in_tz.date(), datetime.min.time()))
    today12_01am_in_tz = today12am_in_tz + timedelta(minutes=1)
    next12_01am_in_tz = today12_01am_in_tz if now_in_tz < today12_01am_in_tz else today12_01am_in_tz + timedelta(days=1)
    # logger.debug(f"Next 12:01 a.m. in {time_zone} : {next12_01am_in_tz.strftime('%m/%d/%Y %H:%M:%S %p')}")
    next12_01am_in_utc = next12_01am_in_tz.astimezone(timezone.utc)
    # logger.debug(f"Next 12:01 a.m. in UTC : {next12_01am_in_utc.strftime('%m/%d/%Y %H:%M:%S %p')}")
    return next12_01am_in_utc.strftime('%m/%d/%Y %H:%M:%S %p')