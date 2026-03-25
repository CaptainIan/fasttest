import time
from xffasttest.common.log import Logger, Fore

def action(func, *args, **kwds):
    def wrapper(*args, **kwds):
        result = None
        try:
            Logger().log_info(f'{func.__name__} --> {list(args)}', Fore.GREEN, end='')
            start_time = time.time()
            if args or kwds:
                result = func(*args, **kwds)
            else:
                result = func()
            end_time = time.time()
            time_difference = round(end_time - start_time, 2)
            Logger().log_print(f' --> {time_difference}s\n', Fore.RED)
            if result:
                Logger().log_info(f'{func.__name__} <-- {result}\n', Fore.BLUE)
        except Exception as e:
            raise e

        return result
    return wrapper