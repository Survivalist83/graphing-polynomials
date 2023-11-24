import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(layout='wide')

def write_polynomial(polynomial_real, polynomial_imag):
    if (len(polynomial_real) != len(polynomial_imag)): return('There has been an error calculating the polynomial.') # this should never throw, ever
    leng = len(polynomial_real)

    poly = ''
    for i in range(leng):
        real = int(polynomial_real[i]) if (polynomial_real[i].is_integer()) else polynomial_real[i]
        imag = int(polynomial_imag[i].imag) if (polynomial_imag[i].imag.is_integer()) else polynomial_imag[i]
        
        # handles the plus or minus at the beginning of each term
        if (poly != '' and (polynomial_real[i] != 0 or polynomial_imag[i] != 0)):
            if (real != 0 and imag != 0): # handles compex coefficients
                poly = poly + ' + ' if (i != 0) else '' # always a plus since complex coefficients will always be in parenthesis
            elif (real != 0): # handles real coefficients
                poly = poly + (' +' if (real > 0) else ' -')
            elif (imag != 0): # handles imag coefficients
                poly = poly + (' +' if (imag > 0) else ' -')
            else: st.write ('if you see this there is a catastrophic error (it\'s probably not that bad lol)')
        
        x = 'x' if (leng - i > 1) else ''
        e = f'^{leng - i - 1}' if (leng - i > 2) else ''
        # writes the actual coefficient
        if (real != 0 and imag != 0): # handles complex coefficients
            if (imag == 1): a = ' '
            elif (imag == -1): a = ' '
            else: a = ' ' + str(abs(imag))
            poly = poly + f'({real} {"+" if (imag > 0) else "-"}{a}i){x}{e}'
        
        elif (real != 0): # handles real coefficients
            if (real == 1 and i + 1 != leng): a = ' '
            elif (real == -1 and i + 1 != leng): a = ' '
            else: a = ' ' + str(abs(real))
            poly = poly + a + x + e
        
        elif (imag != 0): # handles imaginary (but specifically not complex) coefficients
            if (imag == 1): a = ' '
            elif (imag == -1): a = ' '
            else: a = ' ' + str(abs(imag))
            poly = poly + a + 'i' + x + e

    return poly

def calculate_y(polynomial_real, polynomial_imag, x, degree):
    y_val = 0
    for j in range(degree + 1):
        y_val = y_val + (x ** (degree - j) * (polynomial_real[j] + polynomial_imag[j]))
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
    polynomial_real = []
    polynomial_imag = []
    
    enter1, enter2 = st.columns(2)
    with enter1:
        for i in range(degree + 1):
            polynomial_real.append(st.number_input(f'Enter real coefficient for x^{degree - i}', key=f'real_coeff_{i}_{column}', value=1.0, step=1.0))
    with enter2:
        for i in range(degree + 1):
            polynomial_imag.append(st.number_input(f'Enter imaginary coefficient for x^{degree - i}', key=f'imag_coeff_{i}_{column}', value=0.0, step=1.0) * 1j)
    
    # st.write('Polynomial Shown: ' + write_polynomial(polynomial_real, polynomial_imag))

    real_imag = st.radio(label='What do you want to show?', options=['Real', 'Imaginary', 'Complex'], key=f'radio{column}', index=column)
    real = real_imag == 'Real' or real_imag == 'Complex'
    imag = real_imag == 'Imaginary' or real_imag == 'Complex'

    # calculates dot locations
    points = pd.DataFrame(columns=['x', 'i', 'y', 'type'])
    for x in np.arange(X_MIN, X_MAX + 1, X_STEP):
        for i in np.arange(I_MIN, I_MAX + 1, I_STEP):
            if (real): points.loc[len(points)] = {'x': x, 'i': i, 'y': calculate_y(polynomial_real, polynomial_imag, complex(x, i), degree).real, 'type': 'real'}
            if (imag): points.loc[len(points)] = {'x': x, 'i': i, 'y': calculate_y(polynomial_real, polynomial_imag, complex(x, i), degree).imag, 'type': 'imag'}

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
                                zaxis=dict(title='Y Real')),
                                title=write_polynomial(polynomial_real, polynomial_imag))

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
st.write('For irrational numbers (pie, radicals, etc.) use a decimal approximation.')
st.write('It can\'t find any irrational zeros and will almost certainly miss decimal ones (depending on what you have "step" set to) so stick to other tools for finding zeros.')

st.header('A few Notes')
st.write('Since computers don\'t have infinite processing power, I can\'t graph every dot in this graph, which is why the "step" inputs exist. To minimize this, make step very small (which has a high impact on performance).')
st.write('A point is a "zero" of the polynomial when both the real and imaginary parts equal zero. In other words, a zero is where both the red and blue dots overlap at y=0.')
st.write('If anyone is good at Python, Plotly, or Streamlit and has an idea of how to make this better, implement a feature, or help in some way, feel free to help! https://github.com/Survivalist83/graphing-polynomials')