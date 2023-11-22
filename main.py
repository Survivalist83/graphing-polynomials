import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def write_polynomial(polynomial):
    poly = ''
    for i in range(len(polynomial)):
        if (polynomial[i] != 0):
            if (len(polynomial) != i and i != 0):
                if (polynomial[i] < 0):
                    poly = poly + ' - '
                else:
                    poly = poly + ' + '
            poly = poly + str(abs(polynomial[i]) if abs(polynomial[i]) != 1 else '') + 'x^' + str(len(polynomial) - i - 1)
    return poly

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
            polynomial.append(st.number_input(f"Enter coefficient for x^{degree - i}", key=f"coeff_{i}", value=1.0, step=1.0))
        st.write('Polynomial Shown: ' + write_polynomial(polynomial))

    with col2: # Window tab; sets the desired window for the drawing
        st.header('Window')
        X_MIN = st.number_input(label='Left X Bound', value=-10.0, step=0.1)
        X_MAX = st.number_input(label='Right X Bound', value=10.0, step=0.1)
        X_STEP = st.number_input(label='X Step', value=1.0, step=0.1)
        I_MIN = st.number_input(label='Left I Bound', value=-10.0, step=0.1)
        I_MAX = st.number_input(label='Right I Bound', value=10.0, step=0.1)
        I_STEP = st.number_input(label='I Step', value=1.0, step=0.1)
        DOT_SIZE = st.number_input(label='Dot Size', value=3, min_value=1, max_value=10, step=1)

# calculates dot locations
points = pd.DataFrame(columns=['x', 'i', 'y', 'type'])
for x in np.arange(X_MIN, X_MAX + 1, X_STEP):
    for i in np.arange(I_MIN, I_MAX + 1, I_STEP):
        points.loc[len(points)] = {'x': x, 'i': i, 'y': calculate_y(polynomial, complex(x, i)).real - 1, 'type': 'real'}
        points.loc[len(points)] = {'x': x, 'i': i, 'y': calculate_y(polynomial, complex(x, i)).imag, 'type': 'imag'}

# dot colors
points.loc[(points['type'] == 'real'), 'color'] = '#FF4031'
points.loc[(points['type'] == 'imag'), 'color'] = '#0541FF'
points.loc[(points['type'] == 'real') & (points['y'] == 0), 'color'] = '#9E0000'
points.loc[(points['type'] == 'imag') & (points['y'] == 0), 'color'] = '#00009E'
points.loc[(points['type'] == 'real') & (points['i'] == 0), 'color'] = '#85FF7D'
points.loc[(points['type'] == 'imag') & (points['i'] == 0), 'color'] = '#00FF00'

# graph

real = st.checkbox(label='Show real part of y', value=True)
imag = st.checkbox(label='Show imaginary part of y when y is complex', value=False)

if (not real):
    points = points[points['type'] != 'real']
if (not imag):
    points = points[points['type'] != 'imag']

fig = go.Figure(data=[go.Scatter3d(x=points['x'], y=points['i'], z=points['y'], mode='markers',
                                  marker=dict(color=points['color'], size=DOT_SIZE))])

fig.update_layout(scene=dict(aspectratio=dict(x=1, y=1, z=1), 
                             xaxis=dict(title='Real'),
                             yaxis=dict(title='Imaginary'),
                             zaxis=dict(title='Y Real')))

st.plotly_chart(fig, use_container_width=True, sharing='streamlit')

# explains what each color is
st.write('Red represents the real part of y, and blue is the imaginary part. You can show/hide them at your convenience with the checkboxes above.')
st.write('Green is when i is zero, aka what you see when you plug it into your graphing calculator.')
st.write('When y is equal to zero, the red/blue is a bit darker. Green stays the same when y equals zero.')
st.write('Note: since computers don\'t have infinite processing power, I can\'t graph every dot in this graph, which is why the "step" inputs exist. To minimize this, make step very small (which has a high impact on performance).')