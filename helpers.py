import streamlit as st
import math

def hash_list(list):
    return hash(tuple(list))

def hash_complex(complex_number):
    return hash((complex_number.real, complex_number.imag))

def calculate_y(polynomial_real, polynomial_imag, x, degree):
    y_val = 0
    for j in range(degree + 1):
        y_val = y_val + (x ** (degree - j) * (polynomial_real[j] + polynomial_imag[j]))
    return y_val

def check_circle(real, imag, X_MIN, X_MAX, I_MIN, I_MAX):
    x = (real - (0.5 * (X_MIN + X_MAX))) ** 2 * 4 / ((X_MIN - X_MAX) ** 2)
    y = (imag - (0.5 * (I_MIN + I_MAX))) ** 2 * 4 / ((I_MIN - I_MAX) ** 2)
    return x + y <= 1

def offset_polar(radians, type, SHAPE):
    if (SHAPE != type or radians % (math.pi / 2) == 0):
        return 1
    else: # This code is ChatGPT's doing, not mine. I haven't taken trig yet and don't fully understand this :)
        left_right = abs(1 / math.cos(radians % (math.pi / 2)))
        up_down = abs(1 / math.sin(radians % (math.pi / 2)))
        return min(left_right, up_down)

@st.cache_data(hash_funcs={list: hash_list})
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