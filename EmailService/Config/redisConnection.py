from redis import Redis

redisConnect = Redis(host='127.0.0.1',port=6379)

if redisConnect.ping():
    print("Redis Connected")
else:
    print("Redis Not Connected")
