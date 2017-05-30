from factor import Factor

def main():
    # f = Factor(['A', 'B', 'C'], \
    # [['t', 'f'], ['t', 'f'] ,['t', 'f']], \
    # [0.63, 0.27, 0.08, 0.02, 0.28, 0.12, 0.48, 0.12])
    # f.out_prob()
    # print f.pTable
    # Factor.restrict(f, 'A', 't')
    # f.out_prob()
    # print f.pTable

    # f1 = Factor(['A', 'B'], \
    # [['t', 'f'], ['t', 'f']], \
    # [0.9, 0.1, 0.4, 0.6])
    # f1.out_prob()

    f1 = Factor(['A', 'B', 'C'], \
    [['t', 'f'], ['t', 'f'], ['t', 'f']], \
    [0.63, 0.27, 0.08, 0.02, 0.28, 0.12, 0.48, 0.12])
    f1.out_prob()

    f2 = Factor(['C', 'D'], \
    [['t', 'f'], ['t', 'f']], \
    [0.7, 0.3, 0.8, 0.2])
    f2.out_prob()
    
    # f2 = Factor(['C', 'D', 'E'], \
    # [['t', 'f'], ['t', 'f'], ['t', 'f']], \
    # [0.63, 0.27, 0.08, 0.02, 0.28, 0.12, 0.48, 0.12])
    # f2.out_prob()

    ff = Factor.multiply(f1, f2)
    f3 = Factor.normalize(ff)
    f3.out_prob()

main()