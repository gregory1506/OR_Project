''' Naive implementation of Fibonacci sequence '''
past = {}
def fib(N):
    if N < 2:
        return 1
    if N in past:
        return past[N]
    else:
        past[N] = fib(N -1) + fib(N - 2)
    return past[N] 

print("Fibonnaci of {} is {}".format(40,fib(40)))