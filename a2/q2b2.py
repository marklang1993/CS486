from factor import Factor

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

q2b2()