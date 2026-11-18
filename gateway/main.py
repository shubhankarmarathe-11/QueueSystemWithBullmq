

from fastapi import FastAPI,Request,HTTPException
from starlette import status
from sqlmodel import SQLModel
from Config.dbConnection import engine
from pydantic import BaseModel,EmailStr
from Config.envConfig import get_settings,Settings
from bullmq import Queue

app = FastAPI()

SQLModel.metadata.create_all(engine)

class EmailCred(BaseModel):
    email: EmailStr
    html: str
    subject: str
    type: str


email_queue = Queue("Emails")


@app.get("/")
def SlashRoot():
    return "Hello World"


@app.post("/api/email")
async def emailService(emailCred:EmailCred,request:Request):
    env:Settings = get_settings()
    try:
        job = await email_queue.add(
            "emails",
            {
                "email": str(emailCred.email),
                "html": emailCred.html,
                "subject": emailCred.subject,
                "type": emailCred.type
            },
            {
                "attempts": 3,
                "backoff": {
                    "type": "exponential",
                    "delay": 2000
                },
                "removeOnComplete": True,
                "removeOnFail":False
            }
        )

        return {
            "message": "Email queued successfully",
            "jobId": job.id
        }

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Unable to queue email"
        )