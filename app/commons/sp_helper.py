import os
from app.commons.db_helper import getSQLCursor
import logging
from typing import List

logger = logging.getLogger()

async def exec_store_proc(sp_name: str, param_names: List, param_values: List, conStr: str, fetch_data: bool= True):
        try:
            print(f'Begin exec_store_proc_survey sp_name {sp_name} param {str(param_names)} param value {str(param_values)}.')
            stored_proc = f"EXEC [{sp_name}] {', '.join([f'@{name} = ?' for name in param_names])}"
            params = tuple(param_values)
            cursor, conn = await getSQLCursor(conStr)
            cursor.execute(stored_proc, params)
            data = None
            if fetch_data:
                data = cursor.fetchall()
            conn.commit()
            conn.close()
            return data
        except Exception as ex:
            print(f'exec_store_proc_survey Failed {str(ex)}.')
            raise
    
async def exec_stored_procedure_multiple_sets(sp_name: str, param_names: List, param_values: List, conStr: str, fetch_data: bool= True):
    try:
        stored_proc = f"EXEC [{sp_name}] {', '.join([f'@{name} = ?' for name in param_names])}"
        params = tuple(param_values)
        cursor, conn = await getSQLCursor(conStr)
        cursor.execute(stored_proc, params)
        data = []
        if fetch_data:
            while True:
                rows = cursor.fetchall()
                data.append(rows)
                if not cursor.nextset():
                    break

        conn.commit()
        conn.close()
        return data

    except Exception as ex:
        raise