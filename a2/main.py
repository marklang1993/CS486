from factor import Factor

def main():
    f = Factor(['A', 'B', 'C'], \
    [['t', 'f'], ['t', 'f'] ,['t', 'f']], \
    [0.63, 0.27, 0.08, 0.02, 0.28, 0.12, 0.48, 0.12])
    f.out_prob()
    f.restrict('B', 't')
    f.out_prob()
    
main()