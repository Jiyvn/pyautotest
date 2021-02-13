import platform
import multiprocessing as mp
import os
import time

import psutil

from app.core.exceptions import ArgsError


def run(method, args, amount=1):
    pool = None
    try:
        if len(args) <= 1:
            method(*args[0])
        else:
            if platform.system().lower() != "windows":
                mp.set_start_method('spawn', force=True)
            cores = mp.cpu_count()
            perc = psutil.cpu_percent()
            used = int(perc*cores/100) + 1
            left = cores - used - 1
            if left <= 0:
                raise ResourceWarning(f"Not enough core for test: {used} used, {cores} in total")
            amount = amount if amount < left else left
            pool = mp.Pool(amount)
            for a in args:
                # print(f"a: {a}")
                if not isinstance(a, (list, tuple)):
                    raise ArgsError("invalid args, expected list or tuple")
                pool.apply_async(method, a)  # 固定并发限制amount，异步进入, 须len(args) >= amount
                time.sleep(0.5)
            # pool.map(method, args)  # 固定并发，需要结合partial
            pool.close()
            pool.join()
    except KeyboardInterrupt:
        if pool:
            pool.close()
            pool.join()
        else:
            os._exit(1)
