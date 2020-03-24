import numpy as np
import os
import json
import matplotlib
from matplotlib import pyplot as plt

def load_data(m, f):
    iters = 1001
    freq = 5
    data = np.load(f + "iter_{}_freq_{}_info_regs.npy".format(iters, freq))
    x = range(0, iters, freq)
    return x, data

def plot(game):
    methods = ['cfr', 'cfr_full_rp_cur', 'cfr_full_rp_ave']
    # methods = ['cfr_full_rp_ave']

    for m in methods:
        plt.title(m)
        plt.ylabel('Regret')
        plt.xlabel('Iterations')
        plt.xscale('log')
        plt.yscale('log')
        f = m + '_' + game + '/'
        x, y = load_data(m, f)
        for i in range(y.shape[1]):
            plt.plot(x, y[:,i], label=str(i), linewidth=1.)
        plt.legend()
        plt.savefig('./full_rp/' + game + '_' + m + '_info_reg.png')
        # plt.show()
        plt.clf()
    
if __name__ == '__main__':
    # game = 'leduc_poker'
    game = 'kuhn_poker'

    plot(game)
        
        
        
