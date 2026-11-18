from pydantic import BaseModel,EmailStr
from sqlmodel import Session
from Config.dbConnection import engine,EmailLogs
from datetime import datetime


class EmailCred(BaseModel):
    email: EmailStr
    html: str
    subject: str
    type: str


def InsertToDB(EmailCred:EmailCred,clientip:str,in_retry:bool):

    Insert = EmailLogs(emailTo=EmailCred["email"],type=EmailCred["type"],clientIp=clientip,createAt=datetime.now(),in_retry=in_retry)

    with Session(engine) as session:
        session.add(Insert)
        session.commit()
        session.close()

    print("Inserted Into DB")

