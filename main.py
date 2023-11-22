import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def calculate_y(polynomial, x):
    y_val = 0
    for j in range(degree + 1):
        y_val = y_val + (x ** (degree - j) * polynomial[j])
    return y_val

# Window settings
with st.sidebar:
    col1, col2 = st.columns(2)

    with col1: # Polynomial Tab; sets the polynomial to be drawn by the program
        st.header('Polynomial')
        degree = st.number_input(label='Select the degree of the polynomial:', value=3, min_value=1, step=1)
        polynomial = []
        for i in range(degree + 1):
            polynomial.append(st.number_input(f"Enter coefficient for x^{degree - i}", key=f"coeff_{i}", value=1))

    with col2: # Window tab; sets the desired window for the drawing
        st.header('Window')
        X_MIN = st.number_input(label='Left X Bound', value=-10.0, step=0.1)
        X_MAX = st.number_input(label='Right X Bound', value=10.0, step=0.1)
        X_STEP = st.number_input(label='X Step', value=1.0, step=0.1)
        I_MIN = st.number_input(label='Left I Bound', value=-10.0, step=0.1)
        I_MAX = st.number_input(label='Right I Bound', value=10.0, step=0.1)
        I_STEP = st.number_input(label='I Step', value=1.0, step=0.1)
        DOT_SIZE = st.number_input(label='Dot Size', value=5, min_value=1, max_value=10, step=1)

# this part displays the polynomial being drawn onto the screen
poly = ''
for i in range(len(polynomial)):
    if (polynomial[i] != 0):
        if (len(polynomial) != i and i != 0):
            if (polynomial[i] < 0):
                poly = poly + ' - '
            else:
                poly = poly + ' + '
        poly = poly + str(abs(polynomial[i]) if abs(polynomial[i]) != 1 else '') + 'x^' + str(len(polynomial) - i - 1)
st.write('Polynomial Shown: ' + poly)

# calculates dot locations
points = pd.DataFrame(columns=['x', 'i', 'y'])
for x in np.arange(X_MIN, X_MAX + 1, X_STEP):
    for i in np.arange(I_MIN, I_MAX + 1, I_STEP):
        points.loc[len(points)] = {'x': x, 'i': i, 'y': calculate_y(polynomial, complex(x, i))}
points['y_real'] = points['y'].apply(lambda z: z.real)
points['y_imag'] = points['y'].apply(lambda z: z.imag)

# graphing stuff
points['color'] = 'red'
points.loc[points['y_real'] == 0, 'color'] = 'green'
points.loc[points['i'] == 0, 'color'] = 'blue'

fig = go.Figure(data=[go.Scatter3d(x=points['x'], y=points['i'], z=points['y_real'], mode='markers',
                                  marker=dict(color=points['color'], size=DOT_SIZE))])

fig.update_layout(scene=dict(aspectratio=dict(x=1, y=1, z=1), 
                             xaxis=dict(title='Real'),
                             yaxis=dict(title='Imaginary'),
                             zaxis=dict(title='Y Real')))

st.plotly_chart(fig, use_container_width=True, sharing='streamlit')

fig = go.Figure(data=[go.Scatter3d(x=points['x'], y=points['i'], z=points['y_imag'], mode='markers',
                                  marker=dict(color=points['color'], size=DOT_SIZE))])

fig.update_layout(scene=dict(aspectratio=dict(x=1, y=1, z=1), 
                             xaxis=dict(title='Real'),
                             yaxis=dict(title='Imaginary'),
                             zaxis=dict(title='Y Imaginary')))

st.plotly_chart(fig, use_container_width=True, sharing='streamlit')