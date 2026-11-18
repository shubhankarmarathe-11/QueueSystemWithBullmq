from sqlmodel import Field,SQLModel, create_engine
import uuid
from Config.envConfig import get_settings,Settings

class EmailLogs(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4,primary_key=True)
    emailTo: str
    type: str
    clientIp: str | None = None
    in_retry: bool
    createAt: str



env:Settings = get_settings()

mysql_url = f"mysql+pymysql://{env.mysql_user}:{env.mysql_pass}@{env.mysql_host}/{env.mysql_table}"
engine = create_engine(mysql_url)

with engine.connect() as connection:
    print("Connection successful")


