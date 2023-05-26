from django.shortcuts import render
import requests
import numpy as np

"""--------------------------------
        LOGICA DE VISTAS
--------------------------------"""

# Numeros decimales

def decimal_base(number, base):
    digits = []
    while number > 0:
        digits.append(number % base)
        number = number // base
    digits.reverse()
    return np.array(digits)

def digits_string(digits, base):
    symbols = "0123456789ABCDEF"
    string = ""
    for digit in digits:
        string += symbols[digit]
    return string

# Numeros Octales

def octal_binary(octal_number):
    binary_number = ""
    octal_digits = str(octal_number)
    
    for digit in octal_digits:
        decimal_digit = int(digit)
        binary_digit = ""
        
        while decimal_digit > 0:
            binary_digit = str(decimal_digit % 2) + binary_digit
            decimal_digit = decimal_digit // 2
        
        # Asegurar que cada dígito binario tenga 3 bits
        if len(binary_digit) < 3:
            binary_digit = "0" * (3 - len(binary_digit)) + binary_digit
        
        binary_number += binary_digit
    
    return binary_number

# Numeros Hexadecimales

def hexadecimal_to_binary(hex_number):
    hex_digits = "0123456789ABCDEF"
    binary_digits = ""

    for digit in hex_number:
        if digit.upper() in hex_digits:
            decimal_value = hex_digits.index(digit.upper())
            binary_value = ""

            while decimal_value > 0:
                binary_value = str(decimal_value % 2) + binary_value
                decimal_value = decimal_value // 2

            # Asegurar que cada dígito binario tenga 4 bits
            if len(binary_value) < 4:
                binary_value = "0" * (4 - len(binary_value)) + binary_value

            binary_digits += binary_value
        else:
            raise ValueError("Caracter hexadecimal inválido: {}".format(digit))

    return binary_digits

# Numeros Binarios

def binary_octal(binary_number):
    octal_number = ""
    binary_digits = str(binary_number)
    
    # Asegurar que la longitud del número binario sea múltiplo de 3
    binary_digits = binary_digits.zfill((len(binary_digits) // 3 + 1) * 3)
    
    for i in range(0, len(binary_digits), 3):
        binary_digit = binary_digits[i:i+3]
        decimal_digit = int(binary_digit, 2)
        octal_number += str(decimal_digit)
    
    return octal_number


def binary_hexadecimal(binary_number):
    hexadecimal_number = ""
    binary_digits = str(binary_number)
    
    # Asegurar que la longitud del número binario sea múltiplo de 4
    binary_digits = binary_digits.zfill((len(binary_digits) // 4 + 1) * 4)
    
    for i in range(0, len(binary_digits), 4):
        binary_digit = binary_digits[i:i+4]
        decimal_digit = int(binary_digit, 2)
        hexadecimal_digit = hex(decimal_digit)[2:].upper()
        hexadecimal_number += hexadecimal_digit
    
    return hexadecimal_number


def binary_decimal(binary_number):
    decimal_number = 0
    binary_digits = str(binary_number)
    
    for digit in binary_digits:
        decimal_number = decimal_number * 2 + int(digit)
    
    return decimal_number




"""--------------------------------
        VISTAS PRINCIPALES
--------------------------------"""

def index(request):
    return render(request, 'index.html')

def decimal_views(request):
    if request.method == 'POST':
        number = int(request.POST.get('number', 0))
        bases = request.POST.getlist('base')

        # Conversión a las bases seleccionadas
        results = []
        for base in bases:
            base = int(base)
            digits = decimal_base(number, base)
            result = digits_string(digits, base)
            results.append(result)

        context = {
            'results': results
        }
        return render(request, 'conv_decimal.html', context)
    else:
        return render(request, 'conv_decimal.html')

def binary_view(request):
    if request.method == 'POST':
        binary_number = request.POST.get('number', '')
        bases = request.POST.getlist('base')

        # Validar que el número binario solo contenga caracteres válidos
        valid_chars = set('01')
        if not all(char in valid_chars for char in binary_number):
            return render(request, 'conv_binary.html', {'error': 'Número binario inválido'})

        # Inicializar los resultados de cada base en None
        octal_number = None
        hexadecimal_number = None
        decimal_number = None

        # Realizar las conversiones solo para las bases seleccionadas
        if 'octal' in bases:
            octal_number = binary_octal(binary_number)
        if 'hexadecimal' in bases:
            hexadecimal_number = binary_hexadecimal(binary_number)
        if 'decimal' in bases:
            decimal_number = binary_decimal(binary_number)

        context = {
            'binary_number': binary_number,
            'octal_number': octal_number,
            'hexadecimal_number': hexadecimal_number,
            'decimal_number': decimal_number,
            'bases': bases  # Pasar las bases seleccionadas al contexto
        }
        return render(request, 'conv_binary.html', context)
    else:
        return render(request, 'conv_binary.html')

def octal_views(request):
    if request.method == 'POST':
        octal_number = request.POST.get('number', '')
        binary_number = octal_binary(octal_number)
        
        context = {
            'result': binary_number
        }
        return render(request, 'conv_octal.html', context)
    else:
        return render(request, 'conv_octal.html')

def hex_view(request):
    if request.method == 'POST':
        hex_number = request.POST.get('number', '')
        binary_number = hexadecimal_to_binary(hex_number)
        
        context = {
            'result': binary_number
        }
        return render(request, 'conv_hex.html', context)
    else:
        return render(request, 'conv_hex.html')
