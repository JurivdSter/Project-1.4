# Importeer de benodigde bibliotheken
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Definieer je constanten
b = 0.034363  # Dempingscoëfficiënt
m = 0.001476  # Massa
k = 32        # Veerconstante

# Laad gegevens in of definieer een functie d(t)
df = pd.read_excel(r'C:\Users\Sten\OneDrive\School\Hva\Jaar_1\Project\Blok 4\data memo 1.xlsx')  # Laad gegevens in van Excel-bestand
df['a1'] = np.gradient(np.gradient(df['s1'], df['t1']), df['t1'])  # Bereken versnelling a1
df['a2'] = np.gradient(np.gradient(df['s2'], df['t2']), df['t2'])  # Bereken versnelling a2

# Definieer de functie die de differentiaalvergelijkingen opstelt
def dsdx(t, S, w):
    x, v = S
    d_interp = ainterp(t, df['t2'], w)  # Interpoleer de versnelling op tijdstip t
    return [
        v,
        (d_interp - b * v - k * x) / m
    ]

# Definieer een hulppuntfunctie voor lineaire interpolatie
def ainterp(t, t1, a1):
    return np.interp(t, t1, a1)

S_0 = [0, 0]  # Begincondities voor verplaatsing en snelheid
t = df['t1']  # Tijdreeks vanuit de gegevens

# Los de differentiaalvergelijkingen op voor de eerste set van versnellingen
sol1 = odeint(dsdx, y0=S_0, t=t, tfirst=True, args=(df['a1'],))
x_sol1 = sol1.T[0]

# Los de differentiaalvergelijkingen op voor de tweede set van versnellingen
sol2 = odeint(dsdx, y0=S_0, t=t, tfirst=True, args=(df['a2'],))
x_sol2 = sol2.T[0]

# Manipuleer de gegevens om de tijdstappen voor het plotten te definiëren
df['tscatter'] = df['t1'] - 0.002
df2 = df[df['tscatter'] >= 0]
n = 800 

# Plot de werkelijke en ideale respons van het systeem
plt.plot(t, x_sol1, label='Werkelijke respons')
plt.scatter(df['tscatter'][::n], x_sol1[::n], s=10, color='red', label='Ideale respons')  

plt.xlim(0, 0.030)  # X-as limieten

plt.grid()  # Toon een grid
plt.legend()  # Toon de legende
plt.xlabel('Tijd (s)')  # X-as label
plt.ylabel('Afstand (m)')  # Y-as label
plt.title('Ideale response en werkelijke respons')  # Plot titel
plt.show()  # Toon de plot
