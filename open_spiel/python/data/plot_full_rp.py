import numpy as np
import os
import json
import matplotlib
from matplotlib import pyplot as plt

def load_data(m, f, regret):
    iters = 1001
    freq = 5
    data = np.load(f + "iter_{}_freq_{}.npz".format(iters, freq))
    x = data['cfr_nodes']
    # print(m)
    if regret:
        y = data['regs']
        return x, y
    else:
        y = data['convs']
        return x, y

def plot(game, regret=True):
    methods = ['cfr', 'cfr_full_rp_cur', 'cfr_full_rp_ave']

    if regret:
        plt.ylabel('Average Regret') 
    else:
        plt.ylabel('Exploitability')
    plt.xlabel('CFR nodes')
    plt.xscale('log')
    plt.yscale('log')
    for m in methods:
        f = m + '_' + game + '/'
        x, y = load_data(m, f, regret)
        plt.plot(x, y, label=m, linewidth=2.5)
        # # plt.errorbar(nx, y_mean[::1000], yerr=y_std[::1000], fmt='o', capsize=4, elinewidth=1)
        # print("with variance", with_variance)
        # if with_variance:
        #     plt.fill_between(x, y_mean-y_std, y_mean+y_std, alpha=0.2)
        plt.legend()
    if regret:
        plt.savefig('./full_rp/' + game + '_regret.png')
    else:
        plt.savefig('./full_rp/' + game + '_expl.png')
    plt.show()
    plt.clf()

def plot_both(game):
    methods = ['cfr', 'cfr_full_rp_cur', 'cfr_full_rp_ave']
    colors = ['b', 'g', 'y']

    plt.ylabel('Average Regret and Exploitability')
    plt.xlabel('CFR nodes')
    plt.xscale('log')
    plt.yscale('log')
    for i in range(len(methods)):
        m = methods[i]
        color = colors[i]
        f = m + '_' + game + '/'
        x, y = load_data(m, f, regret=True)
        plt.plot(x, y[:,0], label=m + '_regret_p0', linewidth=2., color=color, linestyle='-.')
        plt.plot(x, y[:,1], label=m + '_regret_p1', linewidth=2., color=color, linestyle='--')
        x, y = load_data(m, f, regret=False)
        plt.plot(x, y, label=m + '_expl', linewidth=2., color=color, linestyle='-')
        # # plt.errorbar(nx, y_mean[::1000], yerr=y_std[::1000], fmt='o', capsize=4, elinewidth=1)
        # print("with variance", with_variance)
        # if with_variance:
        #     plt.fill_between(x, y_mean-y_std, y_mean+y_std, alpha=0.2)
        plt.legend()
    plt.savefig('./full_rp/' + game + '_regret_and_expl.png')
    plt.show()
    plt.clf()
    
if __name__ == '__main__':
    # game = 'leduc_poker'
    game = 'kuhn_poker'

    # plot(game, regret=False)
    plot_both(game)
        
        
        
