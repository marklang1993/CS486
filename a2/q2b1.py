from factor import Factor

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

q2b1()