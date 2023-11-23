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

def calculate_y(polynomial, x, degree):
    y_val = 0
    for j in range(degree + 1):
        y_val = y_val + (x ** (degree - j) * polynomial[j])
    return y_val

# Window settings
with st.sidebar:

    # Window tab; sets the desired window for the drawing
    st.header('Window')
    X_MIN = st.number_input(label='Left X Bound', value=-10.0, step=0.1)
    X_MAX = st.number_input(label='Right X Bound', value=10.0, step=0.1)
    X_STEP = st.number_input(label='X Step', value=1.0, step=0.1)
    I_MIN = st.number_input(label='Left I Bound', value=-10.0, step=0.1)
    I_MAX = st.number_input(label='Right I Bound', value=10.0, step=0.1)
    I_STEP = st.number_input(label='I Step', value=1.0, step=0.1)
    DOT_SIZE = st.number_input(label='Dot Size', value=3, min_value=1, max_value=10, step=1)
    GRAPH_COUNT = st.number_input(label='Number of Graphs', value=1, min_value=1, max_value=3)

def graph_polynomial(column):
    # Polynomial Tab; sets the polynomial to be drawn by the program
    st.header(f'Polynomial {column + 1}' if GRAPH_COUNT != 1 else 'Polynomial')
    degree = st.number_input(label='Select the degree of the polynomial:', key=f'degree{column}', value=3, min_value=1, step=1)
    polynomial = []
    for i in range(degree + 1):
        polynomial.append(st.number_input(f'Enter coefficient for x^{degree - i}', key=f'coeff_{i}_{column}', value=1.0, step=1.0))
    st.write('Polynomial Shown: ' + write_polynomial(polynomial))

    real_imag = st.radio(label='What do you want to show?', options=['Real', 'Imaginary', 'Complex'], key=f'radio{column}', index=column)
    real = real_imag == 'Real' or real_imag == 'Complex'
    imag = real_imag == 'Imaginary' or real_imag == 'Complex'

    # calculates dot locations
    points = pd.DataFrame(columns=['x', 'i', 'y', 'type'])
    for x in np.arange(X_MIN, X_MAX + 1, X_STEP):
        for i in np.arange(I_MIN, I_MAX + 1, I_STEP):
            if (real): points.loc[len(points)] = {'x': x, 'i': i, 'y': calculate_y(polynomial, complex(x, i), degree).real, 'type': 'real'}
            if (imag): points.loc[len(points)] = {'x': x, 'i': i, 'y': calculate_y(polynomial, complex(x, i), degree).imag, 'type': 'imag'}

    # dot colors
    points.loc[(points['type'] == 'real'), 'color'] = '#FF4031'
    points.loc[(points['type'] == 'imag'), 'color'] = '#0541FF'
    points.loc[(points['type'] == 'real') & (points['y'] == 0), 'color'] = '#9E0000'
    points.loc[(points['type'] == 'imag') & (points['y'] == 0), 'color'] = '#00009E'
    points.loc[(points['type'] == 'real') & (points['i'] == 0), 'color'] = '#85FF7D'
    points.loc[(points['type'] == 'imag') & (points['i'] == 0), 'color'] = '#00FF00'

    # graph
    fig = go.Figure(data=[go.Scatter3d(x=points['x'], y=points['i'], z=points['y'], mode='markers',
                                    marker=dict(color=points['color'], size=DOT_SIZE))])

    fig.update_layout(scene=dict(aspectratio=dict(x=1, y=1, z=1), 
                                xaxis=dict(title='Real'),
                                yaxis=dict(title='Imaginary'),
                                zaxis=dict(title='Y Real')))

    st.plotly_chart(fig, use_container_width=True, sharing='streamlit')

columns = st.columns(GRAPH_COUNT)
for i, col in enumerate(columns):
    with col:
        graph_polynomial(i)

# explains what each color is
st.header('Explanation of Colors')
st.write('Red represents the real part of y, and blue is the imaginary part. You can show/hide them at your convenience with the radio buttons above.')
st.write('Green is when i is zero, aka what you see when you plug it into your graphing calculator.')
st.write('When y is equal to zero, the red/blue is a bit darker. Green stays the same when y equals zero.')

st.header('Limitations')
st.write('Only supports real integer exponents greater than or equal to zero.')
st.write('Currently does not work with imaginary coefficients. This is something I plan to change in the future, but I haven\'t gotten to it yet.')
st.write('For irrational numbers (pie, radicals, etc.) use a decimal approximation. There isn\'t a way to add them currently and allowing imaginary coefficients is higher on my to-do list, so don\'t expect it soon. Sorry for the inconvenience :(')
st.write('It can\'t find any irrational zeros and will almost certainly miss decimal ones (depending on what you have "step" set to) so stick to other tools for finding zeros.')

st.header('A few Notes')
st.write('Since computers don\'t have infinite processing power, I can\'t graph every dot in this graph, which is why the "step" inputs exist. To minimize this, make step very small (which has a high impact on performance).')
st.write('A point is a "zero" of the polynomial when both the real and imaginary parts equal zero. In other words, a zero is where both the red and blue dots overlap at y=0.')
st.write('If anyone is good at Python, Plotly, or Streamlit and has an idea of how to make this better, implement a feature, or help in some way, feel free to help! https://github.com/Survivalist83/graphing-polynomials')