import time

def calc(func):
    def wrapper(*args):
        init_time = time.time()
        
        if len(args) < 2:
            fun = func(args[1], args[2], args[3], args[4])
        else:
            fun = func(args[1], args[2])
            
        final_time = time.time()
        time_result =  final_time - init_time
            
        print(f"Done in {time_result} seconds!")
        
        return fun
    return wrapper