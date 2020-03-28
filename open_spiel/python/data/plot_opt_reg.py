import numpy as np
import os
import json
import matplotlib
from matplotlib import pyplot as plt

def load_data(m, f, regret):
    iters = 101
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

def plot(game, methods, path, regret=True):
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
        plt.savefig(path + game + '_regret.png')
    else:
        plt.savefig(path + game + '_expl.png')
    plt.show()
    plt.clf()

def plot_both(game, methods, path):
    colors = ['b', 'g', 'y', 'r']

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
    plt.savefig(path + game + '_regret_and_expl.png')
    plt.show()
    plt.clf()
    
if __name__ == '__main__':
    game = 'leduc_poker'
    # game = 'kuhn_poker'
    methods = ['cfr', 'cfr_opt_reg_mc_10', 'cfr_opt_reg_mc_20', 'cfr_opt_reg_mc_50']
    path_name = './opt_reg/'
    if not os.path.exists(path_name):
        os.mkdir(path_name)

    plot(game, methods, path_name, regret=False)
    # plot_both(game, methods, path_name)
        
        
        
