# -- coding: utf-8 --
"""
Created on Fri Apr 26 09:32:45 2024

@author: Sten
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
w=np.sqrt(32/0.001476)
dt=float(6*10**-7)
v1=[0]
v2=[0]
x1=[0]
x2=[0]
a1=[]
a2=[]

df = pd.read_excel(r'C:\Users\Sten\OneDrive\School\Hva\Jaar_1\Project\Blok 4\data memo 1.xlsx')
df['a1']= np.gradient(np.gradient(df['s1']))
df['a2']= np.gradient(np.gradient(df['s2']))
df['v1'] = np.gradient(df['s1'])
df['v2'] = np.gradient(df['s2'])
b=0.034363
m= 0.001476
k=32
for i in range(len(df)-1):
    a1.append(df['a1'][i]-b/m*df['v1'][i]-k/m*df['s1'][i])
    v1.append(v1[i-1]+a1[i]*dt)
    x1.append(x1[i-1]+v1[i]*dt)
    a2.append(df['a2'][i]-b/m*df['v2'][i]-k/m*df['s2'][i])
    v2.append(v2[i-1]+a2[i]*dt)
    x2.append(x2[i-1]+v2[i]*dt)

fig, ax = plt.subplots()
ax2 = ax.twinx()
ax.plot(df['t1'],x2, label='Tweede dataset', color='green')
ax2.plot(df['t1'],x1 , label='Eerste dataset', color = "red")
plt.title("De afgelegde afstand van de massa en twee experimenten")
plt.xlabel('tijd (s)')
plt.ylabel('afgelegde astand(m)')
plt.grid()
plt.legend()
plt.show()