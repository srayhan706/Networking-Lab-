import matplotlib.pyplot as plt

def plot_graph(data_file, title):
    with open(data_file, 'r') as file:
        data = file.readlines()
        data = [float(d.strip()) for d in data]

    time = [i for i in range(len(data))]

    plt.plot(time, data)
    plt.xlabel('Time')
    plt.ylabel(title)
    plt.title(f'{title} vs. Time')
    plt.grid(True)
    plt.show()

# Plot SampleRTT vs. time
plot_graph('sample_rtt.txt', 'SampleRTT')

# Plot Estimated RTT vs. time
plot_graph('timeout.txt', 'Estimated RTT')
