import time
from Config.redisConnection import redisConnect
import json
import emails
from utils.Email_DB_Functions import InsertToDB
from Config.envConfig import Settings,get_settings


def EmailFunction():

    env:Settings = get_settings()

    new_obj = json.loads(redisConnect.rpop("email"))
    EmailCred = new_obj["email"]
    time.sleep(3)
    message = emails.html(
        subject=EmailCred["subject"],
        html=EmailCred["html"],
        mail_from=("fastAPi",env.email_user)
    )
    try:
        response = message.send(
            to=EmailCred["email"],
            smtp={
                "host": "smtp.gmail.com",
                "port": 587,
                "tls": True,
                "user": env.email_user,
                "password":env.email_pass
            }
        )

        if response.status_code == 250:
            InsertToDB(new_obj["email"],new_obj['clientIp'],False)
    except Exception as e:
        print(f"error - {e}")
        InsertToDB(new_obj["email"],new_obj['clientIp'],True)





def EmailFunctionForQueue(subject:str,html:str,email:str,type:str):

    env:Settings = get_settings()

    new_obj = {
        "subject":subject,
        "html":html,
        "type":type,
        "email":email
    }

    message = emails.html(
        subject=subject,
        html=html,
        mail_from=("fastAPi",env.email_user)
    )
    try:
        response = message.send(
            to=email,
            smtp={
                "host": "smtp.gmail.com",
                "port": 587,
                "tls": True,
                "user": env.email_user,
                "password":env.email_pass
            }
        )

        if response.status_code == 250:
            InsertToDB(new_obj,"",False)
            return "done"
    except Exception as e:
        print(f"error - {e}")
        InsertToDB(new_obj,"",True)
        return "error"
