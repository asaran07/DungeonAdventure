import sqlite3


def __init__():
    pass


def getSkeletonInfo(name):
    try:
        sqliteConnection = sqlite3.connect("monster_factory_new.db")
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """select * from monster_factory_new where name = ?"""
        cursor.execute(sqlite_select_query, (name,))
        records = cursor.fetchall()
        print("Monster ID ", name)
        for i, row in records:
            print(row[i])

    except sqlite3.Error as error:
        print("Failed to read data from sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("SQLite connection is closed")


getSkeletonInfo("Skeleton")
