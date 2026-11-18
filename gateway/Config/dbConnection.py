from sqlmodel import SQLModel,Field,create_engine
import uuid
from Config.envConfig import Settings,get_settings


class BlackListTokens(SQLModel,table=True):
    Token:str = Field(default=None,primary_key=True)
    reason:str


env:Settings = get_settings()

mysql_url = f"mysql+pymysql://{env.mysql_user}:{env.mysql_pass}@{env.mysql_host}/{env.mysql_table}"
engine = create_engine(mysql_url)

with engine.connect() as connection:
    print("Connection successful")