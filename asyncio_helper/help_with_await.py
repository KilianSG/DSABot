import asyncio


def cancel_tasks(tasks):
    for task in tasks:
        if task.cancelled():
            continue
        else:
            task.cancel()
