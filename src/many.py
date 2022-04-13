# -*- coding: UTF-8 -*-

import asyncio
import time


async def worker(id):
    print("woker%s 开始工作" % (id))
    await asyncio.sleep(1)
    print("woker%s 工作结束" % (id))
    return id


async def main():
    taskList=[]
    for num in range(1,8):
        task = asyncio.create_task(worker(num))
        print("%s任务已经分发"%(num))
        taskList.append(task)

    print(f"started at {time.strftime('%X')}")

    for task in taskList:
        await task
        print("await")

    print(f"finished at {time.strftime('%X')}")


print("START")
asyncio.run(main())
print("END")
