from factor import Factor

def ex1():
    # example 1
    f1 = Factor(['A'], \
    [['t', 'f']], \
    [0.9, 0.1])
    f1.print_table()

    f2 = Factor(['A', 'B'], \
    [['t', 'f'], ['t', 'f']], \
    [0.9, 0.1, 0.4, 0.6])
    f2.print_table()

    f3 = Factor(['B', 'C'], \
    [['t', 'f'], ['t', 'f']], \
    [0.7, 0.3, 0.2, 0.8])
    f3.print_table()

    fL = [f1, f2, f3]
    qL = ['C']
    hL = ['A', 'B']
    eL = dict()
    fRes = Factor.inference(fL, qL, hL, eL)
    fRes.print_table()

def ex2():
    f1 = Factor(['A'], \
    [['t', 'f']], \
    [0.6, 0.4])
    # f1.print_table()

    f2 = Factor(['A', 'B'], \
    [['t', 'f'], ['t', 'f']], \
    [0.2, 0.8, 0.75, 0.25])
    # f2.print_table()

    f3 = Factor(['A', 'C'], \
    [['t', 'f'], ['t', 'f']], \
    [0.8, 0.2, 0.1, 0.9])
    # f3.print_table()

    f4 = Factor(['B', 'C', 'D'], \
    [['t', 'f'], ['t', 'f'], ['t', 'f']], \
    [0.95, 0.05, 0.9, 0.1, 0.8, 0.2, 0.0, 1.0])
    # f4.print_table()

    f5 = Factor(['C', 'E'], \
    [['t', 'f'], ['t', 'f']], \
    [0.7, 0.3, 0.0, 1.0])

    # fRes = Factor.multiply(f1, f3)
    # fRes.print_table()
    # fRes = Factor.sumout(fRes, 'A')
    # fRes.print_table()

    fL = [f1, f2]
    qL = ['B']
    hL = ['A']
    eL = dict()
    f6 = Factor.inference(fL, qL, hL, eL)
    f6.print_table()

    fL = [f1, f3]
    qL = ['C']
    hL = ['A']
    eL = dict()
    f7 = Factor.inference(fL, qL, hL, eL)
    f7.print_table()

    fL = [f6, f7, f4]
    qL = ['D']
    hL = ['B', 'C']
    eL = dict()
    f8 = Factor.inference(fL, qL, hL, eL)
    f8.print_table()

def main():
    ex1()

main()