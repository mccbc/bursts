import sys, os
sys.path.append('/home/bcm2vn/research/wind/vis/python/')
cwd = os.getcwd()
from plot_1d import *
import athena_read
from glob import glob
sys.path.append(cwd)
import argparse
import pdb

G = 6.67e-8
Rgas = 8.314e7
arad = 7.7657e-15
msun = 1.99e33
Rns = 1e6
M = 1.4e-3
temp = 1e7
vir = G * msun * M / Rns / Rgas / temp
rho_0 = 0.03324127
kappaes = 0.2 * Rns * rho_0
Prat = 2.8112786

GM = G*M*msun/Rns/Rgas/temp


parser = argparse.ArgumentParser()
parser.add_argument('step', type=int, nargs='*', help='Step or steps at which to plot the variables')
parser.add_argument('-o', '--output', action='store_true')
args = parser.parse_args()

athfiles = glob('eddingtonwind.block0.out2.*')
steps = args.step

for step in steps:
    data = athena_read.tab(athfiles[step])
    print(athfiles[step])
    x1v = data[0, 0, :, 0]
    Fcom = data[0, 0, :, 11]

    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(17, 11))
    plt.tight_layout()
    fig.subplots_adjust(hspace=0, top=0.95, bottom=0.05)


    ax1.plot(x1v, Prat*kappaes*Fcom - GM/x1v**2, 'c-', label="Rad - Grav accel")
    ax1.plot(x1v, np.abs(Prat*kappaes*Fcom - GM/x1v**2), 'c--')
    ax1.set_ylim((1e-3, 1e2))

    #ax1.plot(x1v, np.zeros(len(x1v)), 'k--')

    ax3.plot(x1v, data[0, 0, :, 3], 'm-', label="Velocity")
    ax3.plot(x1v, np.abs(data[0, 0, :, 3]), 'm--')

    ax2.plot(x1v, data[0, 0, :, 8], label="Eulerian Frame Flux")
    ax2.plot(x1v, data[0, 0, :, 6], label="Energy Density")
    ax2.plot(x1v, data[0, 0, :, 11], label="Comoving Frame Flux")
    ax2.set_ylim((1e-5, 1.5))

    ax3.plot(x1v, data[0, 0, :, 8] - data[0, 0, :, 11], 'r-', label="Advective Flux")
    ax3.plot(x1v, np.abs(data[0, 0, :, 8] - data[0, 0, :, 11]), 'r--')
    ax3.set_ylim((1e-20, 10))

    for ax in (ax1, ax2, ax3):
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.legend()

    plt.xlabel('x1v')
    #plt.ylim((1e-15, 1e2))
    #plt.xlim((0.95, 40))

    plt.suptitle('Diagnostic plot      t={}'.format(1e-4*step))
    #plt.tight_layout()

    #box = ax.get_position()
    #ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height*0.85])
    #ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.09), ncol=3)


    if args.output == True:
        plt.savefig('diagnostic_step{:05d}.png'.format(step))
    else:
        plt.show()
