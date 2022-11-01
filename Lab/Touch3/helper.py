import matplotlib.pyplot as plt
from scipy import signal
from scipy.integrate import cumtrapz
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.widgets import Button
from pylab import rcParams

def test_cap_IV(cap_IV):
    i_test = np.array([0.002,0.002,0.002,0.002,0.002])
    c_test = 1e-9
    t_test = 3e-6
    V_correct = [0.0, 6.0, 12.0, 18.0, 24.0]
    V_check = np.array(cap_IV(i_test, c_test, t_test))
    
    i_test_2 = np.array([0.002,0.002,0.002,0.002,0.002])
    c_test_2 = 10e-9
    t_test_2 = 3e-6
    V_correct_2 = [0.0, 0.6, 1.2, 1.8, 2.4]
    V_check_2 = np.array(cap_IV(i_test_2, c_test_2, t_test_2))
    
    rtol = 1e-4
    if (np.linalg.norm(V_check - V_correct) / np.linalg.norm(V_correct) > rtol) or (np.linalg.norm(V_check_2 - V_correct_2) / np.linalg.norm(V_correct_2) > rtol):
        print("Incorrect! Fix your cap_IV before moving on")
    else:
        print("cap_IV test passed!")

def square_wave_zerod():
    return np.concatenate((np.array(200*[0]), (0.01 * signal.square(2 * np.pi * 3 * np.linspace(0, 1, 1200)))))

def integrate(function, dt, c=0):
    return cumtrapz(function, dx=dt, initial=c);

def check_cap(C, C_t):
    if (1e-9 < C or 1e-12 > C):
        raise ValueError('C has the wrong units. Make sure you use the right units')
    elif (1e-9 < C_t or 1e-12 > C_t):
        raise ValueError('C_t has the wrong units. Make sure you use the right units')
    return

class Index1(object):
    touch = False
    def __init__(self, l, vo, vot):
        self.l = l
        self.vo = vo
        self.vot = vot
    def a_touch(self, event):
        ydata = self.vot
        self.l.set_ydata(ydata)
        plt.show()
    def a_notouch(self, event):
        self.touch = False
        ydata = self.vo
        self.l.set_ydata(ydata)
        plt.show()

def cap_plot(cap_IV, C, C_t):
    rcParams['figure.figsize'] = 7,5
    t = .2e-9 
    i_in = (10 * signal.square(2 * np.pi * 3 * np.linspace(0, 1, 1300)))[100:1200:]  

    vo = cap_IV(0.001 * i_in, C, t)
    if (C_t != 0):
        vot = cap_IV(0.001 * i_in, C_t, t)
    else:
        vot = vo
    time = [t * x / t for x in range(0, len(i_in))]

    fig, ax1 = plt.subplots()
    plt.title("Voltage and Current vs Time on a Capacitor")
    plt.subplots_adjust(bottom=0.2)
    plt.grid(False)

    l, = plt.plot(time, vo, lw=2)
    plt.ylim(-(max(vo)*4),max(vo)*4)
    ax1.set_xlabel('time')
    ax1.set_ylabel('Voltage (V)', color='b')
    ax2 = ax1.twinx()
    ax2.plot(time, i_in, 'r')
    ax2.set_ylabel('Current (mA)', color='r')
    
    #set up buttons
    axtouch   = plt.axes([0.7, 0.05, 0.1, 0.075])
    axnotouch = plt.axes([0.81, 0.05, 0.1, 0.075])
    btouch = Button(axtouch, 'Touch')
    bnotouch = Button(axnotouch, 'No Touch')
    callback = Index1(l,vo,vot)
    btouch.on_clicked(callback.a_touch)
    bnotouch.on_clicked(callback.a_notouch)
    return (vo, vot), (btouch, bnotouch, callback) # need return so graph updates in notebook

class Index2(object):
    touch = False
    def __init__(self, l, vo, vot, p, cot, co):
        self.l = l
        self.vo = vo
        self.vot = vot
        self.p = p
        self.cot = cot
        self.co = co
    def a_touch(self, event):
        self.touch = True
        ydata1 = self.vot
        self.l.set_ydata(ydata1)
        ydata2 = self.cot
        self.p.set_ydata(ydata2)
        plt.show()
    def a_notouch(self, event):
        self.touch = False
        ydata1 = self.vo
        self.l.set_ydata(ydata1)
        ydata2 = self.co
        self.p.set_ydata(ydata2)
        plt.show()

def cap_plot_wcomp(comparator, v_ref, cap_IV, C, C_t):
    rcParams['figure.figsize'] = 7,5
    t = .2e-9 
    i_in = (10 * signal.square(2 * np.pi * 3 * np.linspace(0, 1, 1300)))[100:1200:]  

    vo = cap_IV(0.001 * i_in, C, t)
    co = [comparator(x, v_ref) for x in vo]
    if (C_t != 0):
        vot = cap_IV(0.001 * i_in, C_t, t)
        cot = [comparator(x, v_ref) for x in vot]
    else:
        vot = vo
        cot = co

    time = [t * x / t for x in range(0, len(i_in))]

    fig, ax1 = plt.subplots()
    plt.title("Voltage on a Capacitor and Comparator Output")
    plt.subplots_adjust(bottom=0.2)
    plt.grid(False)

    l, = plt.plot(time, vo, lw=2)
    l.set_color('b')
    p, = plt.plot(time, co, lw=2)
    p.set_color('g')

    plt.ylim(-(max(vo)*4),max(vo)*4)
    
    ax1.set_xlabel('time')
    ax1.set_ylabel('Voltage (V)', color='b')
    ax1.plot(time, len(time)*[v_ref], color='r')
    m_ref = mpatches.Patch(color='red', label='V_Ref')
    m_cap  = mpatches.Patch(color='blue', label='Capacitor Voltage')
    m_comp  = mpatches.Patch(color='green', label='Comparator')
    plt.legend(handles=[m_ref, m_cap, m_comp], loc='upper right', bbox_to_anchor=(.7, 11))

    # set up buttons
    axtouch   = plt.axes([0.7, 0.05, 0.1, 0.075])
    axnotouch = plt.axes([0.81, 0.05, 0.1, 0.075])
    btouch = Button(axtouch, 'Touch')
    bnotouch = Button(axnotouch, 'No Touch')
    callback = Index2(l, vo, vot, p, cot, co)
    btouch.on_clicked(callback.a_touch)
    bnotouch.on_clicked(callback.a_notouch)

    return btouch, bnotouch, callback # need return so graph updates in notebook
