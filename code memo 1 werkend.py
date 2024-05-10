from scipy.integrate import odeint
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Define your constants
b = 0.034363
m = 0.001476
k = 32

# Load your data or define your function d(t)
df = pd.read_excel(r'C:\Users\Sten\OneDrive\School\Hva\Jaar_1\Project\Blok 4\data memo 1.xlsx')
df['a1'] = np.gradient(np.gradient(df['s1'], df['t1']), df['t1'])
df['a2'] = np.gradient(np.gradient(df['s2'], df['t2']), df['t2'])

def dsdx(t, S, w):
    x, v = S
    d_interp = ainterp(t,df['t2'], w)
    return [
        v,
        (d_interp - b * v - k * x) / m
    ]
def ainterp(t,t1, a1):
    return np.interp(t,t1,a1)
S_0 = [0, 0]
t = df['t1']

# Solve the ODE system
sol1 = odeint(dsdx, y0=S_0, t=t, tfirst=True, args=(df['a1'],))
x_sol1 = sol1.T[0]
sol2 = odeint(dsdx, y0=S_0, t=t, tfirst=True, args=(df['a2'],))
x_sol2 = sol2.T[0]
df['tscatter']= df['t1']-0.002
df2= df[df['tscatter'] >= 0]
n = 800 
plt.plot(t, x_sol1, label='Werkelijke respons')
plt.scatter(df['tscatter'][::n], x_sol1[::n], s=10, color='red', label= 'ideale respons')  

plt.xlim(0,0.030)



plt.grid()
plt.legend()
plt.xlabel('Tijd (s)')
plt.ylabel('Afstand (m)')
plt.title('Ideale response en werkelijke respons')
plt.show()

