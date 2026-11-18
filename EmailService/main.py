from fastapi import FastAPI,HTTPException, BackgroundTasks,Request,Depends
from starlette import status
import json
from pydantic import BaseModel,EmailStr
from Config.redisConnection import redisConnect
from Config.envConfig import Settings,get_settings 
from utils.EmailFunction import EmailFunction,EmailFunctionForQueue
from Config.dbConnection import engine
from sqlmodel import SQLModel
from Config.QueueConfig import queue
from bullmq import Worker


class EmailCred(BaseModel):
    email: EmailStr
    html: str
    subject: str
    type: str


async def VerifyInternalToken(request:Request):
    env:Settings = get_settings()
    internalToken = request.headers.get("x-internal-secret")
    actualToken = env.internal_token

    if internalToken is None or actualToken != internalToken:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail={"message":"Access forbidden: Invalid token"})


app = FastAPI()

SQLModel.metadata.create_all(engine)



@app.get("/",dependencies=[Depends(VerifyInternalToken)])
def mainRoute():
    raise HTTPException(status_code=status.HTTP_200_OK,detail="Working Email service")







@app.post("/api/email",dependencies=[Depends(VerifyInternalToken)])
async def SendEmail(EmailCred:EmailCred,Req:Request,background_tasks:BackgroundTasks):
    new_obj = {
        "email": EmailCred.model_dump(),
        "clientIp": Req.client.host
    }
    redisConnect.rpush("email",json.dumps(new_obj))
    background_tasks.add_task(EmailFunction)
    return "The email queued And will be sent shortly."


