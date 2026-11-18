import asyncio
from bullmq import Worker

from utils.EmailFunction import EmailFunctionForQueue



async def Process(job,token):
    try:
        print(f"Processing Job: {job.id}")
        print(f"Attempt: {job.attemptsMade}")
        if job.name == "emails":
            result = EmailFunctionForQueue(job.data["subject"],job.data["html"],job.data["email"],job.data["type"])
            print("result--",result)
            print(f"Job {job.id} completed")

            return result
    except Exception as e:

        print(f"Job {job.id} failed: {str(e)}")

        raise

async def runQueueWorker():
    worker = Worker("Emails",Process,{"concurrency":100})

    try:
        await asyncio.Event().wait()
    finally:
        await worker.close();


if __name__ == "__main__":
    asyncio.run(runQueueWorker())