from sqlalchemy import create_engine
from sqlalchemy import text
import secret

engine = create_engine(f"mysql+pymysql://{secret.username}:{secret.password}@{secret.hostname}:{secret.port}/final_project")


def exec(query):
    with engine.connect() as conn:
        try:
            result = conn.execute(text(query))
            print(f"exec : {query}")
            print(f"exec : {result.rowcount} rows affected")
            return result
        except BaseException as err:
            print(f"Unexpected {err=}, {type(err)=}")


def count(table):
    result = exec(f"SELECT count(1) as count from {table};")
    for row in result:
        return row["count"]


def truncate(table):
    result = exec(f"TRUNCATE TABLE {table};")
    return result.rowcount
