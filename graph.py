import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import base64
import io
import re
import sympy as sp
import matplotlib.pyplot as plt
from scipy import signal
import matplotlib
import ast
import numpy as np

def calculate_asymptotes(numerator, denominator, frequencies):
    zeros = np.roots(numerator)
    poles = np.roots(denominator)

    # Inicializar os valores de magnitude e fase assintóticas
    asymptotic_mag = np.zeros_like(frequencies)
    asymptotic_phase = np.zeros_like(frequencies)
    
    # Obter as magnitudes dos zeros e polos (frequências)
    zero_frequencies = np.abs(zeros)
    pole_frequencies = np.abs(poles)
    
    
    #all_frequencies = np.concatenate([np.abs(zeros), np.abs(poles)])
    # Combinar e ordenar todas as frequências de interesse
    all_frequencies = np.concatenate([zero_frequencies, pole_frequencies])
    all_frequencies.sort()
    
    phase_zero_frequencies = []
    for f in zero_frequencies:
        phase_zero_frequencies.append(f / 10)
        #phase_zero_frequencies.append(f)
        phase_zero_frequencies.append(f * 10)

    phase_pole_frequencies = []
    for f in pole_frequencies:
        phase_pole_frequencies.append(f / 10)
        #phase_pole_frequencies.append(f)
        phase_pole_frequencies.append(f * 10)

    # Crie o novo array paaara as frequências de fase
    phase_frequencies = []
    

    # Adicione f/10 e 10f para cada frequência no array
    for f in all_frequencies:
        phase_frequencies.append(f / 10)
        phase_frequencies.append(f)
        phase_frequencies.append(f * 10)

    # Converta o resultado de volta para um array numpy
    phase_frequencies = np.array(phase_frequencies)

    # Ordene o array em ordem crescente
    phase_frequencies = np.sort(phase_frequencies)

    # Exibindo o resultado
    phase_frequencies
    phase_change = 0

    # Calcular as assíntotas com base nos polos e zeros
    for f in all_frequencies:
        if f in zero_frequencies:
            slope_change = 20  # Incrementa a inclinação em +20 dB/dec para cada zero
            #phase_change = 45  # Incrementa a fase em +90° para cada zero
        elif f in pole_frequencies:
            slope_change = -20  # Decrementa a inclinação em -20 dB/dec para cada polo
            #phase_change = -45  # Decrementa a fase em -90° para cada polo
        if f != 0:
            asymptotic_mag += slope_change * np.log10(frequencies / f) * (frequencies >= f)

    count = 0
    for f in phase_frequencies:
        count += 1
        phase_change = 0
        if (f in phase_zero_frequencies):
            phase_change += 45  # Incrementa a fase em +90° para cada zero
        if (f/10 in phase_zero_frequencies):
            phase_change += 45
        if (10*f in phase_zero_frequencies):
            phase_change = 0
        
        if (f/10 in phase_pole_frequencies):
            phase_change -= 45
        if (10*f in phase_pole_frequencies):
            phase_change +=  0
        if (f in phase_pole_frequencies):
            phase_change = - 45  # Decrementa a fase em -90° para cada polo
        if f != 0:
            asymptotic_phase += phase_change * np.log10(frequencies / (f)) * (frequencies >= f )
        #asymptotic_phase += phase_change * np.log10(frequencies / (f / 10)) * (frequencies >= f / 10)

    
    return asymptotic_mag, asymptotic_phase

def setup_plot(numerator = [1, 1] , denominator= [1, 12, 100] ):
    system = signal.TransferFunction(numerator, denominator)

    # Gerar dados do gráfico de Bode
    frequencies, mag, phase = signal.bode(system, n=1000)

    # Gerar dados do gráfico de Bode
    zero_frequencies = np.abs(np.roots(numerator))
    pole_frequencies = np.abs(np.roots(denominator))
    
    
    # Combinar e ordenar todas as frequências de interesse
    all_frequencies = np.concatenate([zero_frequencies, pole_frequencies])
    phase_frequencies = [0.1]
    for f in all_frequencies:
        phase_frequencies.append(f / 10)
        phase_frequencies.append(f)
        phase_frequencies.append(f * 10)

    # Converta o resultado de volta para um array numpy
    phase_frequencies = np.array(phase_frequencies)

    # Ordene o array em ordem crescente
    phase_frequencies = np.sort(phase_frequencies)

    #n = len(np.roots(numerator) + np.roots(denominator)) + 2
    frequencies2, mag2, phase2 = signal.bode(system, w=phase_frequencies)

    # Calcular assíntotas
    asymptotic_mag, asymptotic_phase = calculate_asymptotes(numerator, denominator, frequencies)

    # Ajustar assíntota inicial da magnitude com base na magnitude em baixa frequência
    if (denominator[-1] != 0):
        initial_gain = 20 * np.log10(np.abs(numerator[-1] / denominator[-1]))
        asymptotic_mag += initial_gain

    # Criar o gráfico de magnitude de Bode
    plt.figure(figsize=(10, 6))

    # Plotar a resposta de magnitude (em dB)
    plt.subplot(2, 2, 1)
    plt.semilogx(frequencies, mag, label='Magnitude')
    plt.semilogx(frequencies2, mag2, 'r--', label='Assíntota da Magnitude')
    #plt.plot(frequencies, asymptotic_mag, 'r--', label='Assíntota da Magnitude')


    plt.ylim(-60, 60)  # Ajustar os limites do eixo Y para o gráfico de magnitude
    plt.yticks(np.arange(-60, 61, 20))  # Configurar os ticks do eixo Y para amplitude
    plt.xticks([0.1, 1, 10, 100, 1000], labels=['0.1', '1', '10', '100', '1000'])  # Ajustar os ticks do eixo X
    plt.xlim(0.1, 1000)  # Definir o limite do eixo X

    # Alinhar o eixo Y ao valor 0.1 do eixo X
    ax = plt.gca()
    ax.spines['left'].set_position(('data', 0.1))  # Move o eixo Y para cruzar o ponto 0.1 do eixo X
    ax.yaxis.tick_left()

    plt.ylabel('Magnitude (dB)')
    plt.title('Gráfico de Bode com Assíntotas Dinâmicas')
    plt.grid(True)
    plt.legend()

    # Plotar a resposta de fase (em graus)
    plt.subplot(2, 2, 2)
    plt.semilogx(frequencies, phase, label='Fase')
    plt.semilogx(frequencies2, phase2, 'r--', label='Assíntota da Fase')
    #plt.plot(frequencies, asymptotic_phase, 'r--', label='Assíntota da Fase')

    plt.ylim(-180, 181)  # Ajustar os limites do eixo Y para o gráfico de fase
    plt.yticks(np.arange(-135, 136, 45))  # Configurar os ticks do eixo Y para fase
    plt.xticks([0.1, 1, 10, 100, 1000], labels=['0.1', '1', '10', '100', '1000'])  # Ajustar os ticks do eixo X
    plt.xlim(0.1, 1000)  # Definir o limite do eixo X

    # Alinhar o eixo Y ao valor 0.1 do eixo X
    ax = plt.gca()
    ax.spines['left'].set_position(('data', 0.1))  # Move o eixo Y para cruzar o ponto 0.1 do eixo X
    ax.yaxis.tick_left()

    plt.ylabel('Fase (graus)')
    plt.xlabel('Frequência (rad/s)')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.savefig('grafico_bode.png')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    return img_base64

def preprocess_polynomial_string(polynomial_str):
    polynomial_str = polynomial_str.lower()
    
    superscript_map = {
        '¹': '**1', '²': '**2', '³': '**3', '⁴': '**4', '⁵': '**5',
        '⁶': '**6', '⁷': '**7', '⁸': '**8', '⁹': '**9'
    }
    
    for char, replacement in superscript_map.items():
        polynomial_str = polynomial_str.replace(char, replacement)
    
    polynomial_str = polynomial_str.replace('jω', 's').replace('jw', 's')
    polynomial_str = polynomial_str.replace('^', '**')    
    polynomial_str = re.sub(r'\)\s*(?=[a-zA-Z(])', ')*', polynomial_str)
    polynomial_str = re.sub(r'(?<=[a-zA-Z])\s*\(', '*(', polynomial_str)
    polynomial_str = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', polynomial_str)
    
    return polynomial_str

def parse_polynomial_string(polynomial_str):
    corrected_str = preprocess_polynomial_string(polynomial_str)    
    polynomial_expr = sp.sympify(corrected_str)
    
    return polynomial_expr

def get_bode_plot_blob(numerator, denominator):
    polynomial_str = numerator #input("Digite a expressão do numerador: ")
    corrected_expr = parse_polynomial_string(polynomial_str)
    expanded_polynomial = sp.expand(corrected_expr)
    coefficients_numerator = sp.Poly(expanded_polynomial, sp.Symbol('s')).all_coeffs()

        
    polynomial_str = denominator #input("Digite a expressão do denominador: ")
    corrected_expr = parse_polynomial_string(polynomial_str)
    expanded_polynomial = sp.expand(corrected_expr)
    coefficients_denominador = sp.Poly(expanded_polynomial, sp.Symbol('s')).all_coeffs()


    # Criar o sistema de função de transferência
    print(f" {coefficients_numerator[0]} / {coefficients_denominador}")

    #coefficients_numerator = [1] 
    #coefficients_denominador = [1, 1]
    num = ast.literal_eval(f"{coefficients_numerator}")#[200.3,0] # Numerador (exemplo)
    den = ast.literal_eval(f"{coefficients_denominador}")  # Denominador (exemplo)

    
    return setup_plot(num, den)

a = get_bode_plot_blob("(jw+10)", "(jw(jw +5)²)")
#print(a)