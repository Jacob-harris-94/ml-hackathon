# tail recursion with defualt args
def recurse_n_times(n=0):
    if n > 0:
        recurse_n_times(n-1)
    print(f'recursed {n} times')

if __name__ == '__main__':
    recurse_n_times()
