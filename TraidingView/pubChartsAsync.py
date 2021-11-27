#import requests
import asyncio
import aiohttp
import random
import string
from datetime import datetime 



def logger(msg, source):
    print(datetime.now(), "| msg from", source, ":", msg)  

    
def logger_worker(msg, worker_id):
    logger(msg, "worker №"+str(worker_id)) 


def save_url(url):
    f = open("URLs.txt", "a");
    f.write(str(datetime.now()) + ": "+ url + "\n")
    f.close()


def get_random_string():
    return  ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=8))


metrics = 0


async def measure_runtime():
    global metrics
    while True:
        await asyncio.sleep(10)
        logger("avrg requests per second: "+ str(metrics/10), "runtime measurer")
        metrics = 0
    
    

async def worker(id):
    logger_worker("ready", id)
    global metrics
    async with aiohttp.ClientSession() as session:

        while True:

            val = get_random_string()
            
            async with session.get('https://www.tradingview.com/chart/' + val) as resp:
                if resp.status == 200:
                    logger_worker("found valid url at /"+ val, id)
                    save_url(val)
                metrics+=1
                   
            
    logger_worker("done", id)

async def main(number_of_workers):


    tasks = []
    tasks.append(asyncio.create_task(measure_runtime()))
    
    for w in range(number_of_workers):
        tasks.append(asyncio.create_task(worker(w)))
    
        
    for t in tasks:
        await t

asyncio.run(main(15))



