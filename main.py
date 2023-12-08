import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import math
from helpers import *

st.set_page_config(layout='wide')

# Window settings
with st.sidebar:
    MODE = st.radio(label='Mode', options=['Cartesian', 'Polar'],
                    help='The default option is Cartesian Square, and it is safe to leave it there. ' +
                    'Cartesian Circle shaves off points around the edges so it looks more circular.')
    
    # Window tab; sets the desired window for the drawing
    if (MODE == 'Cartesian'):
        SHAPE = st.radio(label='Shape', options=['Square', 'Circle'], help='Square is recommended for Cartesian mode.', index=0)
        st.header('Window')
        X_MIN = st.number_input(label='Left X Bound', value=-10.0, step=1.0)
        X_MAX = st.number_input(label='Right X Bound', value=10.0, step=1.0)
        X_STEP = st.number_input(label='X Step', value=1.0, step=1.0)
        I_MIN = st.number_input(label='Left I Bound', value=-10.0, step=1.0)
        I_MAX = st.number_input(label='Right I Bound', value=10.0, step=1.0)
        I_STEP = st.number_input(label='I Step', value=1.0, step=1.0)
        WINDOW_SETTINGS = [MODE, SHAPE, X_MIN, X_MAX, X_STEP, I_MIN, I_MAX, I_STEP]
    elif (MODE == 'Polar'):
        SHAPE = st.radio(label='Shape', options=['Circle', 'Square', 'Mix of Both'], help='Circle is recommended for Polar mode.', index=0)
        st.header('Window')
        THETA_STEP = st.number_input(label='Theta Step (Degrees)', value=9, step=1, min_value=1)
        DOT_COUNT = st.number_input(label='Number of Dots per Theta Step', value=10, step=1, min_value=1)
        DOT_INCREMENT = st.number_input(label='Gap between Dots', value=1.0, step=1.0, min_value=0.1)
        WINDOW_SETTINGS = [MODE, SHAPE, THETA_STEP, DOT_COUNT, DOT_INCREMENT]
    
    DOT_SIZE = st.number_input(label='Dot Size', value=3, min_value=1, max_value=10, step=1)
    GRAPH_COUNT = st.number_input(label='Number of Graphs', value=1, min_value=1, max_value=3)
    OVERLAP_GRAPHS = st.checkbox(label='Overlap real and imaginary graphs when showing complex?', value=False)
    WINDOW_SETTINGS.append(OVERLAP_GRAPHS)
    
def input_polynomial(column):
    # Polynomial Tab; sets the polynomial to be drawn by the program
    st.header(f'Polynomial {column + 1}' if GRAPH_COUNT != 1 else 'Polynomial')
    degree = st.number_input(label='Select the degree of the polynomial:', key=f'degree{column}', value=3, min_value=1, step=1)
    polynomial_real = []
    polynomial_imag = []
    
    enter1, enter2 = st.columns(2)
    with enter1:
        for i in range(degree + 1):
            polynomial_real.append(st.number_input(f'Enter real coefficient for x^{degree - i}', key=f'real_coeff_{i}_{column}', value=1.0, step=1.0))
    with enter2:
        for i in range(degree + 1):
            polynomial_imag.append(st.number_input(f'Enter imaginary coefficient for x^{degree - i}', key=f'imag_coeff_{i}_{column}', value=0.0, step=1.0) * 1j)

    real_imag = st.radio(label='What do you want to show?', options=['Real', 'Imaginary', 'Complex'], key=f'radio{column}', index=column)
    
    fig = calculate_polynomial(polynomial_real, polynomial_imag, degree, real_imag, WINDOW_SETTINGS)

    columns = st.columns(1 + (0 if fig[1] == '' else 1))
    for i, col in enumerate(columns):
        with col:
            fig[i].update_traces(marker=dict(size=DOT_SIZE))
            st.plotly_chart(fig[i], use_container_width=True, sharing='streamlit')

@st.cache_data(hash_funcs={complex: hash_complex})
def calculate_polynomial(polynomial_real, polynomial_imag, degree, real_imag, WINDOW_SETTINGS):
    real = real_imag == 'Real' or real_imag == 'Complex'
    imag = real_imag == 'Imaginary' or real_imag == 'Complex'

    # calculates dot locations
    if (MODE == 'Cartesian'): # Cartesian Mode
        points = pd.DataFrame(columns=['x', 'i', 'y', 'type'])
        for x in np.arange(X_MIN, X_MAX + 1, X_STEP):
            for i in np.arange(I_MIN, I_MAX + 1, I_STEP):
                if (SHAPE != 'Circle' or check_circle(x, i, X_MIN, X_MAX, I_MIN, I_MAX)):
                    y = calculate_y(polynomial_real, polynomial_imag, complex(x, i), degree)
                    if (real): points.loc[len(points)] = {'x': x, 'i': i, 'y': y.real, 'type': 'real'}
                    if (imag): points.loc[len(points)] = {'x': x, 'i': i, 'y': y.imag, 'type': 'imag'}
    
    elif (MODE == 'Polar'): # Polar Mode
        points = pd.DataFrame(columns=['x', 'i', 'y', 'type'])
        for theta in range(int(360 / THETA_STEP)):
            radians = math.radians(theta * THETA_STEP)
            for increment in range(int(DOT_COUNT * offset_polar(radians, 'Mix of Both', SHAPE))):
                radius = increment * DOT_INCREMENT * offset_polar(radians, 'Square', SHAPE)
                x = radius * math.cos(math.radians(theta * THETA_STEP))
                i = radius * math.sin(math.radians(theta * THETA_STEP))
                y = calculate_y(polynomial_real, polynomial_imag, complex(x, i), degree)
                if (real): points.loc[len(points)] = {'x': x, 'i': i, 'y': y.real, 'type': 'real'}
                if (imag): points.loc[len(points)] = {'x': x, 'i': i, 'y': y.imag, 'type': 'imag'}
    
    # dot colors
    points.loc[(points['type'] == 'real'), 'color'] = '#FF4031'
    points.loc[(points['type'] == 'imag'), 'color'] = '#0541FF'
    points.loc[(points['type'] == 'real') & (points['y'] == 0), 'color'] = '#9E0000'
    points.loc[(points['type'] == 'imag') & (points['y'] == 0), 'color'] = '#00009E'
    points.loc[(points['type'] == 'real') & (points['i'] == 0), 'color'] = '#85FF7D'
    points.loc[(points['type'] == 'imag') & (points['i'] == 0), 'color'] = '#00FF00'

    # graph

    fig = ''
    if (real_imag == 'Real' or real_imag == 'Imaginary' or OVERLAP_GRAPHS):
        fig = go.Figure(data=[go.Scatter3d(x=points['x'], y=points['i'], z=points['y'], mode='markers',
                                        marker=dict(color=points['color']),
                                        hovertemplate='Real: %{x}, Imaginary: %{y}, Output: %{z}<extra></extra>')])
        fig.update_layout(scene=dict(aspectratio=dict(x=1, y=1, z=1),
                                    xaxis=dict(title='Real'),
                                    yaxis=dict(title='Imaginary'),
                                    zaxis=dict(title='Y')),
                                    title=write_polynomial(polynomial_real, polynomial_imag))
        return fig, ''
    else:
        points_real = points[points['type'] == 'real']
        fig_real = go.Figure(data=[go.Scatter3d(x=points_real['x'], y=points_real['i'], z=points_real['y'], mode='markers',
                                        marker=dict(color=points_real['color']),
                                        hovertemplate='Real: %{x}, Imaginary: %{y}, Output: %{z}<extra></extra>')])
        fig_real.update_layout(scene=dict(aspectratio=dict(x=1, y=1, z=1),
                                    xaxis=dict(title='Real'),
                                    yaxis=dict(title='Imaginary'),
                                    zaxis=dict(title='Y')),
                                    title=write_polynomial(polynomial_real, polynomial_imag))
        points_imag = points[points['type'] == 'imag']
        fig_imag = go.Figure(data=[go.Scatter3d(x=points_imag['x'], y=points_imag['i'], z=points_imag['y'], mode='markers',
                                        marker=dict(color=points_imag['color']),
                                        hovertemplate='Real: %{x}, Imaginary: %{y}, Output: %{z}<extra></extra>')])
        fig_imag.update_layout(scene=dict(aspectratio=dict(x=1, y=1, z=1),
                                    xaxis=dict(title='Real'),
                                    yaxis=dict(title='Imaginary'),
                                    zaxis=dict(title='Y')))
        return fig_real, fig_imag

columns = st.columns(GRAPH_COUNT)
for i, col in enumerate(columns):
    with col:
        input_polynomial(i)

# explains what each color is
st.header('Explanation of Colors')
st.write('Red represents the real part of y, and blue is the imaginary part. You can show/hide them at your convenience with the radio buttons above.')
st.write('Green is when i is zero, aka what you see when you plug it into your graphing calculator.')
st.write('When y is equal to zero, the red/blue is a bit darker. Green stays the same when y equals zero.')

st.header('Limitations')
st.write('Only supports real integer exponents greater than or equal to zero.')
st.write('For irrational numbers (pie, radicals, etc.) use a decimal approximation.')
st.write('It can\'t find any irrational zeros and will almost certainly miss decimal ones (depending on what you have "step" set to) so stick to other tools for finding zeros.')

st.header('A few Notes')
st.write('Since computers don\'t have infinite processing power, I can\'t graph every dot in this graph, which is why the "step" inputs exist. To minimize this, make step very small (which has a high impact on performance).')
st.write('A point is a "zero" of the polynomial when both the real and imaginary parts equal zero. In other words, a zero is where both the red and blue dots overlap at y=0.')
st.write('This has been designed with dark mode in mind. Click the three dots (upper right hand corner), click settings, and under "Choose app theme, colors and fonts" select "Dark" for best viewing experience.')
st.write('If anyone is good at Python, Plotly, or Streamlit and has an idea of how to make this better, implement a feature, or help in some way, feel free to help! https://github.com/Survivalist83/graphing-polynomials')