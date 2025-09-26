import pyodbc

async def getSQLCursor(conStr):
        conn = pyodbc.connect(conStr)
        cursor = conn.cursor()
        return cursor, conn