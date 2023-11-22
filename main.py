import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def calculate_y(polynomial, x):
    y_val = 0
    for j in range(degree + 1):
        y_val = y_val + (x ** (degree - j) * polynomial[j])
    return y_val

polynomial = [2, -1, 3, 6, -4]
degree = len(polynomial) - 1

X_MIN = -10
X_MAX = 10
X_STEP = 0.5

I_MIN = -10
I_MAX = 10
I_STEP = 0.5

points = pd.DataFrame(columns=['x', 'i', 'y'])

for x in np.arange(X_MIN, X_MAX + 1, X_STEP):
    for i in np.arange(I_MIN, I_MAX + 1, I_STEP):
        points.loc[len(points)] = {'x': x, 'i': i, 'y': calculate_y(polynomial, complex(x, i))}

points['y_real'] = points['y'].apply(lambda z: z.real)
points['y_imag'] = points['y'].apply(lambda z: z.imag)

points['color'] = 'red'
points.loc[points['i'] == 0, 'color'] = 'blue'
points.loc[points['y_real'] == 0, 'color'] = 'green'

fig = go.Figure(data=[go.Scatter3d(x=points['x'], y=points['i'], z=points['y_real'], mode='markers',
                                  marker=dict(color=points['color']))])

fig.update_layout(scene=dict(aspectratio=dict(x=1, y=1, z=1), 
                             xaxis=dict(title='Real'),
                             yaxis=dict(title='Imaginary'),
                             zaxis=dict(title='Y')))

st.plotly_chart(fig, use_container_width=True, sharing='streamlit')