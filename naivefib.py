''' Naive implementation of Fibonacci sequence '''

def fib(N):
    if N < 2:
        return 1
    else:
        return fib(N -1) + fib(N - 2)

print("Fibonnaci of {} is {}".format(40,fib(40)))