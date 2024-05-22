# -*- coding: utf-8 -*-
"""
Created on Sat May 18 15:22:55 2024

@author: Sten
"""

import numpy as np
import matplotlib.pyplot as plt


def limiet_bereken(w):
    def position_oscillator(a, t, parameters, initial_state=np.array([0, 0])):
        state = np.empty((len(a), 2), dtype=float)
        state[0] = initial_state
        for i, acc in enumerate(a[:-1]):
            state[i + 1, 1] = state[i, 1] + (acc - parameters[0]**2 * state[i, 0] - 2 * parameters[1] * state[i, 1]) * (t[i + 1] - t[i])
            state[i + 1, 0] = state[i, 0] + state[i, 1] * (t[i + 1] - t[i])
        return state

    # Constants
    k = 0.3820  # Spring constant (N/m)
    m = 4.3e-6  # Mass (kg)
    b = 8.1053e-5  # Damping factor (kg/s)
    Fmax = 600e-9  # Maximum force (N)

    # Calculate natural frequency
    w_0 = np.sqrt(k / m)


    # Time parameters
    t_start = 0.5  # Start time (s)
    t_end = 3# End time (s)
    t_step = 1e-4  # Time step (s)


    # Arrays for force and time
    t = np.arange(t_start, t_end + t_step, t_step)
    F = Fmax * np.cos(w * t)

    # Parameters for the function
    params = np.array([w_0, b / (2 * m)])

    # Simulate mass movement
    state = position_oscillator(F / m, t, params)

    # Calculate the maximum values for every 600 frames
    num_max_frames = 600
    num_max_chunks = len(t) // num_max_frames  # Number of complete chunks of 600 frames

    # Reshape the displacement data to chunks of 600 frames
    data_chunks = state[:num_max_chunks * num_max_frames, 0].reshape(num_max_chunks, num_max_frames)

    # Calculate the maximum absolute value for each chunk
    max_values = np.max(np.abs(data_chunks), axis=1)
    min_values = np.min(data_chunks, axis=1)
    # Time points corresponding to the maximum values
    t_max_values = t[:num_max_chunks * num_max_frames:num_max_frames]

    # Calculate the gradient (dydx) of max_values
    dydt = np.gradient(max_values, t_max_values)

    # Find the index where dydx is closest to 0.00001
    target_dydt = 1e-9
    i=0
    while True:
        if i>=len(dydt)-1:
            index=i 
            break
        elif abs(dydt[i])<target_dydt:
            index=i
            break
        else:
            i+=1

    evenwichtsstand=(max_values+min_values)/2
    evenwichtsstand=np.mean(evenwichtsstand)
    amplitude=max_values[index]-evenwichtsstand
    # Get the corresponding displacement value at that index

    #Plot the displacement over time with max values and their gradient
    


    return [amplitude]

w=np.linspace(200,400,500)
frequentie=w/(2*np.pi)
amplide=[]
for i in range(len(w)):
    amplide.append(limiet_bereken(w[i]))
plt.plot(frequentie,amplide, label='Amplitude tegen frequentie', color='orange')
plt.grid()
plt.xlabel('frequentie (Hz)')
plt.ylabel('Amplitude (m)')
maxium=np.max(amplide)

X_values=frequentie
amplide = [item for sublist in amplide for item in sublist]
frequentie_max= frequentie[np.argmax(amplide)]
amplide=np.array(amplide)

print(frequentie_max)
Y_values= amplide
y_threshold=maxium/2
frequentie_hoger=[]
plt.fill_between(X_values, Y_values, y_threshold, where=(Y_values >= y_threshold), color='blue', alpha=1, label='Groter dan half maxium')
for i in range(len(amplide)):
    if amplide[i]>=y_threshold:
        frequentie_hoger.append(frequentie[i])
FWHM= round(frequentie_hoger[-1]-frequentie_hoger[0],5)
print(f'De FWHM is voor deze parameters gelijk aan {FWHM} Hz ')
        


