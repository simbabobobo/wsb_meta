from func_timeout import func_set_timeout, FunctionTimedOut
import time


def mytest():
    start_time = time.time()
    print("Start")
    for i in range(1, 10):
        print("%d seconds have passed" % i)
        time.sleep(1)
        end_time = time.time()
        if end_time - start_time > 4:
            yield i,i+1
    return i


a=list(mytest())
print(a[0])