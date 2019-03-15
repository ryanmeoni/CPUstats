import matplotlib
matplotlib.use("TkAgg")
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import sys

# Function to get CPU frequency
def getfreq():

    with open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq', 'r') as f:

        line = f.readline().strip()
        lineValue = float(line)
        return lineValue


# Data fields needed for plotting live data
time = 0
pause_start = 0
Freqxs = []
Freqys = []
CstateS0xs = []
CstateS0ys = []

for i in range(0,3):
    newS0 = []
    CstateS0ys.append(newS0)

CstateS1xs = []
CstateS1ys = []

for i in range(0,3):
    newS1 = []
    CstateS1ys.append(newS1)

PowerS0xs = []
PowerS0ys = []
PowerS1xs = []
PowerS1ys = []

# Set up our plots
fig = plt.figure(figsize=(6, 4))
fig.suptitle("CPU Statistics", fontsize = 16)
sub1 = plt.subplot(2, 2, 1)
sub2 = plt.subplot(2, 2, 2)
sub3 = plt.subplot(2, 2, 3)
sub4 = plt.subplot(2, 2, 4)
sub1.set_title("Freq vs. Time")
sub1.set_ylabel("Freq (Hz)")
sub2.set_title("Power vs. Time")
sub2.set_ylabel("Power (Watts)")
sub3.set_title("Socket 1 C-States")
sub3.set_xlabel("Time (Seconds)")
sub3.set_ylabel("C-State (/8)")
sub4.set_title("Socket 0 C-States")
sub4.set_xlabel("Time (Seconds)")
sub4.set_ylabel("C-State (/8)")


# Animation function to update plot
def animate(i):
    global pause_start
    global time
    c0stateS1 = None
    c3stateS1 = None
    c6stateS1 = None
    c0stateS0 = None
    c3stateS0 = None
    c6stateS0 = None
    powerS1 = None
    powerS0 = None

    if (pause_start == 0):


        # Parse data from PCM and graph if we are not paused
        while (powerS1 is None) or (powerS0 is None) or (c0stateS1 is None) or (c3stateS1 is None) or (c6stateS1 is None) or (c0stateS0 is None) or (c3stateS0 is None) or (c6stateS0 is None):

            line = sys.stdin.readline()
            line = line.split()
            if (len(line) > 1) and line[0] == "S1;" and line[1] == "PCUClocks:":
                c0stateS1 = line[6]
                c3stateS1 = line[7]
                c6stateS1 = line[8]
                c0stateS1 = (c0stateS1.rstrip(';'))
                c3stateS1 = (c3stateS1.rstrip(';'))
                c6stateS1 = (c6stateS1)
            if (len(line) > 1) and line[0] == "S0;" and line[1] == "PCUClocks:":
                c0stateS0 = line[6]
                c3stateS0 = line[7]
                c6stateS0 = line[8]
                c0stateS0 = (c0stateS0.rstrip(';'))
                c3stateS0 = (c3stateS0.rstrip(';'))
                c6stateS0 = (c6stateS0)
            if (len(line) > 1) and line[0] == "S0;" and line[8] == "Watts:":
                powerS0 = line[9]
                powerS0 = (powerS0.rstrip(';'))
            if (len(line) > 1) and line[0] == "S1;" and line[8] == "Watts:":
                powerS1 = line[9]
                powerS1 = (powerS1.rstrip(';'))

        # Print data to console to log/check
        print("Socket 1 C0 State is {}".format(c0stateS1))
        print("Socket 1 C3 State is {}".format(c3stateS1))
        print("Socket 1 C6 State is {}".format(c6stateS1))
        print("Socket 0 C0 State is {}".format(c0stateS0))
        print("Socket 0 C3 State is {}".format(c3stateS0))
        print("Socket 0 C6 State is {}".format(c6stateS0))
        print("Socket 1 Power Consumption is {}".format(powerS1))
        print("Socket 0 Power Consumption is {}".format(powerS0))

        # Frequency plot handling
        frequency = getfreq()
        Freqxs.append(int(time))
        Freqys.append(frequency)
        if (len(Freqxs) < 2):
            sub1.plot(Freqxs, Freqys, color = 'blue', label='Frequency')
            sub1.legend(loc='upper right')
            sub1.set_xlim(left=max(0, time - 50), right=time+25)
        else:
            sub1.plot(Freqxs, Freqys, color = 'blue')
            sub1.set_xlim(left=max(0, time - 50), right=time+25)
        # Power plot handling
        PowerS1xs.append(int(time))
        PowerS1ys.append(float(powerS1))
        PowerS0xs.append(float(time))
        PowerS0ys.append(float(powerS0))
        if (len(PowerS1xs) < 2):
            sub2.plot(PowerS1xs, PowerS1ys, color = 'blue', label='S1 Power')
            sub2.plot(PowerS0xs, PowerS0ys, color = 'red', label='S0 Power')
            sub2.legend(loc='upper right')
            sub2.set_xlim(left=max(0, time - 50), right=time+25)
        else:
            sub2.plot(PowerS1xs, PowerS1ys, color = 'blue')
            sub2.plot(PowerS0xs, PowerS0ys, color = 'red')
            sub2.set_xlim(left=max(0, time - 50), right=time+25)
        # S0states plot handling
        CstateS0xs.append(int(time))
        CstateS0ys[0].append(float(c0stateS0))
        CstateS0ys[1].append(float(c3stateS0))
        CstateS0ys[2].append(float(c6stateS0))
        if (len(CstateS0xs) < 2):
            sub3.plot(CstateS0xs, CstateS0ys[0], color = 'green', label='C0 State')
            sub3.plot(CstateS0xs, CstateS0ys[1], color = 'purple', label='C3 State')
            sub3.plot(CstateS0xs, CstateS0ys[2], color = 'blue', label='C6 State')
            sub3.legend(loc='upper right')
            sub3.set_xlim(left=max(0, time - 50), right=time+25)
        else:
            sub3.plot(CstateS0xs, CstateS0ys[0], color = 'green')
            sub3.plot(CstateS0xs, CstateS0ys[1], color = 'purple')
            sub3.plot(CstateS0xs, CstateS0ys[2], color = 'blue')
            sub3.set_xlim(left=max(0, time - 50), right=time+25)
        # S1states plot handling
        CstateS1xs.append(int(time))
        CstateS1ys[0].append(float(c0stateS1))
        CstateS1ys[1].append(float(c3stateS1))
        CstateS1ys[2].append(float(c6stateS1))
        if (len(CstateS1xs) < 2):
            sub4.plot(CstateS1xs, CstateS1ys[0], color = 'green', label='C0 State')
            sub4.plot(CstateS1xs, CstateS1ys[1], color = 'purple', label='C3 State')
            sub4.plot(CstateS1xs, CstateS1ys[2], color = 'blue', label='C6 State')
            sub4.legend(loc='upper right')
            sub4.set_xlim(left=max(0, time - 50), right=time+25)
        else:
            sub4.plot(CstateS1xs, CstateS1ys[0], color = 'green')
            sub4.plot(CstateS1xs, CstateS1ys[1], color = 'purple')
            sub4.plot(CstateS1xs, CstateS1ys[2], color = 'blue')
            sub4.set_xlim(left=max(0, time - 50), right=time+25)

        # Set next second for time
        time = time + 1

    # Else, grab data but don't use it (only happens during pause, because when we resume we want to still get the live data)
    else:
        while (powerS1 is None) or (powerS0 is None) or (c0stateS1 is None) or (c3stateS1 is None) or (c6stateS1 is None) or (c0stateS0 is None) or (c3stateS0 is None) or (c6stateS0 is None):

            line = sys.stdin.readline()
            line = line.split()
            if (len(line) > 1) and line[0] == "S1;" and line[1] == "PCUClocks:":
                c0stateS1 = line[6]
                c3stateS1 = line[7]
                c6stateS1 = line[8]
                c0stateS1 = (c0stateS1.rstrip(';'))
                c3stateS1 = (c3stateS1.rstrip(';'))
                c6stateS1 = (c6stateS1)
            if (len(line) > 1) and line[0] == "S0;" and line[1] == "PCUClocks:":
                c0stateS0 = line[6]
                c3stateS0 = line[7]
                c6stateS0 = line[8]
                c0stateS0 = (c0stateS0.rstrip(';'))
                c3stateS0 = (c3stateS0.rstrip(';'))
                c6stateS0 = (c6stateS0)
            if (len(line) > 1) and line[0] == "S0;" and line[8] == "Watts:":
                powerS0 = line[9]
                powerS0 = (powerS0.rstrip(';'))
            if (len(line) > 1) and line[0] == "S1;" and line[8] == "Watts:":
                powerS1 = line[9]
                powerS1 = (powerS1.rstrip(';'))


        print("Socket 1 C0 State is {}".format(c0stateS1))
        print("Socket 1 C3 State is {}".format(c3stateS1))
        print("Socket 1 C6 State is {}".format(c6stateS1))
        print("Socket 0 C0 State is {}".format(c0stateS0))
        print("Socket 0 C3 State is {}".format(c3stateS0))
        print("Socket 0 C6 State is {}".format(c6stateS0))
        print("Socket 1 Power Consumption is {}".format(powerS1))
        print("Socket 0 Power Consumption is {}".format(powerS0))


# Reset Graph Data
def reset_graphs():
    global time
    global Freqxs
    global Freqys
    global CstateS0xs
    global CstateS0ys
    global CstateS1xs
    global CstateS1ys
    global PowerS0xs
    global PowerS0ys
    global PowerS1xs
    global PowerS1ys
    global sub1
    global sub2
    global sub3
    global sub4

    time = 0
    Freqxs = []
    Freqys = []
    CstateS0xs = []
    CstateS0ys = []
    # Reset 2-D S0states array
    for i in range(0,3):
        newS0 = []
        CstateS0ys.append(newS0)
    CstateS1xs = []
    CstateS1ys = []
    # Reset 2-D S1states array
    for i in range(0,3):
        newS1 = []
        CstateS1ys.append(newS1)
    PowerS0xs = []
    PowerS0ys = []
    PowerS1xs = []
    PowerS1ys = []
    sub1.clear()
    sub2.clear()
    sub3.clear()
    sub4.clear()
    sub1.set_title("Freq vs. Time")
    sub1.set_ylabel("Freq (Hz)")
    sub2.set_title("Power vs. Time")
    sub2.set_ylabel("Power (Watts)")
    sub3.set_title("Socket 1 C-States")
    sub3.set_xlabel("Time (Seconds)")
    sub3.set_ylabel("C-State (/8)")
    sub4.set_title("Socket 0 C-States")
    sub4.set_xlabel("Time (Seconds)")
    sub4.set_ylabel("C-State (/8)")

# Simple change of pause_start value that is checked in animate function
def pause_start_graphs():
    global pause_start
    if (pause_start == 1):
        pause_start = 0
    elif (pause_start == 0):
        pause_start = 1


class graphApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        # Initialize Tkinter

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "CPU Frequency and Power Plot")

        container = tk.Frame(self)

        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure( 0, weight = 5)
        container.grid_columnconfigure(0, weight = 5)

        self.frames = {}

        frame = StartPage(container, self)

        self.frames[StartPage] = frame

        frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame(StartPage)


    def show_frame(self, cont):

        frame = self.frames[cont]

        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        button1 = ttk.Button(self, text="Reset Graphs", command=reset_graphs)

        button1.pack()

        button2 = ttk.Button(self, text="Pause/Start Graphs", command=pause_start_graphs)

        button2.pack()

        canvas = FigureCanvasTkAgg(fig, self)

        canvas.draw()

        canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)

        toolbar = NavigationToolbar2Tk(canvas, self)

        toolbar.update()

        canvas._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = True)


app = graphApp()

app.minsize(1000, 800)

ani = animation.FuncAnimation(fig, animate, interval = 1000)

app.mainloop()

