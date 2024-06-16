import time

def calc(func):
    def wrapper():
        init_time = time.time()
        func()
        final_time = time.time()
        time_result = init_time - final_time
        print(f"Done in {time_result} seconds!")
    return wrapper