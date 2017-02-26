import matplotlib.pyplot as plt
from matplotlib import dates
from matplotlib.dates import HourLocator
import matplotlib.pylab as plb


def make_plot(x, y, label, ylabel, title=None, format_string='-o'):
    plt.plot(x, y, format_string, label=label, markersize=4, linewidth=1.5)
    # generate a formatter
    fmtr = dates.DateFormatter("%H:%M")
    # need a handle to the current axes to manipulate it
    ax = plt.gca()
    # set this formatter to the axis
    ax.xaxis.set_major_formatter(fmtr)
    ax.xaxis.set_major_locator(HourLocator())
    # configure plt
    plt.xticks(rotation=90, fontsize='small')
    plt.yticks(fontsize='small')
    plt.xlabel('Hour', fontsize='medium')
    plt.ylabel(ylabel, fontsize='medium')
    plt.legend(loc='upper right', fontsize='small')
    plt.title(title, fontsize='medium')
    plt.grid(True, which='both', linestyle='-')


def save_as_png(loc):
    plb.savefig(loc, bbox_inches='tight')
    # since plt.show() is not being called, need to "flush" previous plots
    plt.close('all')
