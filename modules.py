import time

def calc(func):
    def wrapper(ip, **kargs):
        init_time = time.time()
        
        fun = func(ip, kargs)
            
        final_time = time.time()
        time_result =  final_time - init_time
            
        print(f"Done in {time_result} seconds!")
        
        return fun
    return wrapper