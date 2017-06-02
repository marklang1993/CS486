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
    # f1 = Factor(['A'], \
    # [['t', 'f']], \
    # [0.6, 0.4])
    # # f1.print_table()

    # f2 = Factor(['A', 'B'], \
    # [['t', 'f'], ['t', 'f']], \
    # [0.2, 0.8, 0.75, 0.25])
    # # f2.print_table()

    f3 = Factor(['A', 'C'], \
    [['t', 'f'], ['t', 'f']], \
    [0.8, 0.2, 0.1, 0.9])

    f4 = Factor(['D', 'B', 'C'], \
    [['t', 'f'], ['t', 'f'], ['t', 'f']], \
    [0.95, 0.05, 0.9, 0.1, 0.8, 0.2, 0.0, 1.0])

    f5 = Factor(['C', 'E'], \
    [['t', 'f'], ['t', 'f']], \
    [0.7, 0.3, 0.0, 1.0])

    # res1 = Factor.multiply(f3, f5)
    # res1.print_table()
    # res2 = Factor.multiply(f5, res1)
    # res2.print_table()

    # fRes = Factor.multiply(f1, f3)
    # fRes.print_table()
    # fRes = Factor.sumout(fRes, 'A')
    # fRes.print_table()

    # fL = [f1, f2]
    # qL = ['B']
    # hL = ['A']
    # eL = dict()
    # f6 = Factor.inference(fL, qL, hL, eL)
    # f6.print_table()

    # fL = [f1, f3]
    # qL = ['C']
    # hL = ['A']
    # eL = dict()
    # f7 = Factor.inference(fL, qL, hL, eL)
    # f7.print_table()

    # fL = [f6, f7, f4]
    # qL = ['D']
    # hL = ['B', 'C']
    # eL = dict()
    # f8 = Factor.inference(fL, qL, hL, eL)
    # f8.print_table()

def q2b1():
    f1 = Factor(['Trav'], \
    [['t', 'f']], \
    [0.05, 0.95])

    f2 = Factor(['Fraud', 'Trav'], \
    [['t', 'f'], ['t', 'f']], \
    [0.01, 0.004, 0.99, 0.996])

    fL = [f1, f2]
    qL = ['Fraud']
    hL = ['Trav']
    eL = dict()
    fRes = Factor.inference(fL, qL, hL, eL)
    fRes.print_table()

def q2b2():
    f1 = Factor(['Trav'], \
    [['t', 'f']], \
    [0.05, 0.95])

    f2 = Factor(['Fraud', 'Trav'], \
    [['t', 'f'], ['t', 'f']], \
    [0.01, 0.004, 0.99, 0.996])

    f3 = Factor(['FP', 'Fraud', 'Trav'], \
    [['t', 'f'], ['t', 'f'], ['t', 'f']], \
    [0.9, 0.1, 0.9, 0.01, 0.1, 0.9, 0.1, 0.99])

    f4 = Factor(['IP', 'Fraud', 'OC'], \
    [['t', 'f'], ['t', 'f'], ['t', 'f']], \
    [0.15, 0.051, 0.1, 0.001, 0.85, 0.949, 0.9, 0.999])

    f5 = Factor(['CRP', 'OC'], \
    [['t', 'f'], ['t', 'f']], \
    [0.1, 0.01, 0.9, 0.99])

    f6 = Factor(['OC'], \
    [['t', 'f']], \
    [0.8, 0.2])

    fL = [f1, f2, f3, f4, f5, f6]
    qL = ['Fraud']
    hL = ['Trav', 'OC']
    eL = dict(FP = 't', IP = 'f', CRP = 't')
    fRes = Factor.inference(fL, qL, hL, eL)
    fRes.print_table()

def q2c():
    f1 = Factor(['Trav'], \
    [['t', 'f']], \
    [0.05, 0.95])

    f2 = Factor(['Fraud', 'Trav'], \
    [['t', 'f'], ['t', 'f']], \
    [0.01, 0.004, 0.99, 0.996])

    f3 = Factor(['FP', 'Fraud', 'Trav'], \
    [['t', 'f'], ['t', 'f'], ['t', 'f']], \
    [0.9, 0.1, 0.9, 0.01, 0.1, 0.9, 0.1, 0.99])

    f4 = Factor(['IP', 'Fraud', 'OC'], \
    [['t', 'f'], ['t', 'f'], ['t', 'f']], \
    [0.15, 0.051, 0.1, 0.001, 0.85, 0.949, 0.9, 0.999])

    f5 = Factor(['CRP', 'OC'], \
    [['t', 'f'], ['t', 'f']], \
    [0.1, 0.01, 0.9, 0.99])

    f6 = Factor(['OC'], \
    [['t', 'f']], \
    [0.8, 0.2])

    fL = [f1, f2, f3, f4, f5, f6]
    qL = ['Fraud']
    hL = ['OC']
    eL = dict(FP = 't', IP = 'f', CRP = 't', Trav = 't')
    fRes = Factor.inference(fL, qL, hL, eL)
    fRes.print_table()

def q2d():
    f1 = Factor(['Trav'], \
    [['t', 'f']], \
    [0.05, 0.95])

    f2 = Factor(['Fraud', 'Trav'], \
    [['t', 'f'], ['t', 'f']], \
    [0.01, 0.004, 0.99, 0.996])

    f3 = Factor(['FP', 'Fraud', 'Trav'], \
    [['t', 'f'], ['t', 'f'], ['t', 'f']], \
    [0.9, 0.1, 0.9, 0.01, 0.1, 0.9, 0.1, 0.99])

    f4 = Factor(['IP', 'Fraud', 'OC'], \
    [['t', 'f'], ['t', 'f'], ['t', 'f']], \
    [0.15, 0.051, 0.1, 0.001, 0.85, 0.949, 0.9, 0.999])

    f5 = Factor(['CRP', 'OC'], \
    [['t', 'f'], ['t', 'f']], \
    [0.1, 0.01, 0.9, 0.99])

    f6 = Factor(['OC'], \
    [['t', 'f']], \
    [0.8, 0.2])
    
    fL = [f1, f2, f3, f4, f5, f6]
    qL = ['Fraud']
    hL = ['Trav', 'FP', 'OC', 'CRP']
    eL = dict(IP = 't')
    fRes = Factor.inference(fL, qL, hL, eL)
    fRes.print_table()

    print('=========================================')

    fL = [f1, f2, f3, f4, f5, f6]
    qL = ['Fraud']
    hL = ['Trav', 'FP', 'OC']
    eL = dict(IP = 't', CRP = 't')
    fRes = Factor.inference(fL, qL, hL, eL)
    fRes.print_table()

def main():
    q2b1()
    q2b2()
    q2c()
    q2d()


main()