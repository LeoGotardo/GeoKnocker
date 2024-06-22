import time

def calc(func):
    def wrapper():
        init_time = time.time()
        func()
        final_time = time.time()
        time_result = init_time - final_time
        print(f"Done in {time_result} seconds!")
    return wrapper

@calc
def soma():
    x = 1000000000000000
    y = 2000000000000
    time.sleep(1)
    return x + y