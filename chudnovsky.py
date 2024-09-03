#Note: For extreme calculations, other code can be used to run on a GPU, which is much faster than this.
# The code for the algorithm taken as-is from Wikipedia https://en.wikipedia.org/wiki/Chudnovsky_algorithm
# precision of  2700 decimal places achieved at n=191  calc time:  5506264 ns (5.5ms)
# Processor	Intel(R) Xeon(R) E-2176M  CPU @ 2.70GHz, 2712 Mhz, 6 Core(s), 12 Logical Processor(s)

import decimal
import time

def binary_split(a, b):
    if b == a + 1:
        Pab = -(6*a - 5)*(2*a - 1)*(6*a - 1)
        Qab = 10939058860032000 * a**3
        Rab = Pab * (545140134*a + 13591409)
    else:
        m = (a + b) // 2 # floor division: divide and round down
        Pam, Qam, Ram = binary_split(a, m)
        Pmb, Qmb, Rmb = binary_split(m, b)
        
        Pab = Pam * Pmb
        Qab = Qam * Qmb
        Rab = Qmb * Ram + Pam * Rmb
    return Pab, Qab, Rab


def chudnovsky(n):
    if n <= 1:
        print('n MUST be greater than 1')
        return -1
    """Chudnovsky algorithm."""
    P1n, Q1n, R1n = binary_split(1, n)
    return (426880 * decimal.Decimal(10005).sqrt() * Q1n) / (13591409*Q1n + R1n)


#print(f"(standard precision)\n02 = {chudnovsky(2)}")  # 3.141592653589793238462643384
max_n = 200
print(f'Calculating pi using the Chudnovsky algorithm up to n={max_n}')
decimal.getcontext().prec = 100 # number of digits of decimal precision
prev_run=0
for n in range(2,max_n):
    start_ns = time.perf_counter_ns()
    this_run = chudnovsky(n)
    stop_ns = time.perf_counter_ns()
    if this_run == prev_run:
        print(f'precision of {decimal.getcontext().prec:>5} decimal places achieved at n={n-1:>3}', end='')
        print(f"  calc time: {prev_time:>8} ns")
        decimal.getcontext().prec+=100
        
    #print(f"{n:02d} = {this_run}",end='')  # 3.14159265358979323846264338...
    #print(f"{n:02d} ",end='')  # 3.14159265358979323846264338...
    prev_time = stop_ns - start_ns
    prev_run = this_run
