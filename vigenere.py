import numpy as np
import re

alfabeto = 'abcdefghijklmnopqrstuvwxyz';
alfatonum = dict(zip(alfabeto, range(len(alfabeto))));

cutoff_factor = 2

stats_port = {
    'a': 0.1463,
    'b': 0.0104,
    'c': 0.0388,
    'd': 0.0499,
    'e': 0.1257,
    'f': 0.0102,
    'g': 0.0130,
    'h': 0.0128,
    'i': 0.0618,
    'j': 0.0040,
    'k': 0.0002,
    'l': 0.0278,
    'm': 0.0474,
    'n': 0.0505,
    'o': 0.1073,
    'p': 0.0252,
    'q': 0.0120,
    'r': 0.0653,
    's': 0.0781,
    't': 0.0434,
    'u': 0.0463,
    'v': 0.0167,
    'w': 0.0001,
    'x': 0.0021,
    'y': 0.0001,
    'z': 0.0047,
}

stats_ing = {
    'a': 0.08167,
    'b': 0.01492,
    'c': 0.02782,
    'd': 0.04253,
    'e': 0.12702,
    'f': 0.02228,
    'g': 0.02015,
    'h': 0.06094,
    'i': 0.06966,
    'j': 0.00153,
    'k': 0.00772,
    'l': 0.04025,
    'm': 0.02406,
    'n': 0.06749,
    'o': 0.07507,
    'p': 0.01929,
    'q': 0.00095,
    'r': 0.05987,
    's': 0.06327,
    't': 0.09056,
    'u': 0.02758,
    'v': 0.00978,
    'w': 0.02360,
    'x': 0.00150,
    'y': 0.01974,
    'z': 0.00074,
}

def remover_acentos(input_str):
    acentos = {'á':'a', 'é':'e', 'í':'i', 'ó':'o', 'ú':'u', 'ã':'a', 'õ':'o', 'â':'a', 'ê':'e', 'ô':'o', 'à':'a', 'ç':'c'}
    return ''.join(acentos[i] if i in acentos else i for i in input_str)

def format_str(msg):
    format_str = remover_acentos(msg.lower())
    return re.sub(r'[^a-z]', '', format_str)

def deformat_str(original, formated):
    index = 0
    result = ''
    for l in original.lower():
        if l.isalpha():
            result += formated[index]
            index += 1
        else:
            result += l
    return result

def calc_stats(msg: str):
    format_msg = format_str(msg)
    stats = { l: float(0) for l in alfabeto }
    for c in format_msg:
        stats[c] += 1

    for l in stats:
        stats[l] /= len(format_msg)

    return stats

def cifrador(msg: str, key):
    format_msg = format_str(msg)
    key_ext = key
    while (len(format_msg) > len(key_ext)):
        key_ext += key

    criptograma = ''
    for i, c in enumerate(format_msg):
        c_index = alfabeto.find(c)
        k_index = alfabeto.find(key_ext[i])
        criptograma += alfabeto[(c_index + k_index) % len(alfabeto)]
    
    return deformat_str(msg, criptograma)


def decifrador(criptograma, key):
    format_cript = format_str(criptograma)
    key_ext = key
    while (len(format_cript) > len(key_ext)):
        key_ext += key
    
    msg = ''
    for i, c in enumerate(format_cript):
        c_index = alfabeto.find(c)
        k_index = alfabeto.find(key_ext[i])
        msg += alfabeto[(c_index - k_index) % len(alfabeto)]
    
    return deformat_str(criptograma, msg)

def find_key_size(criptograma):
    format_cript = format_str(criptograma)
    cript_num = [alfatonum[c] for c in format_cript]
    freq_matrix = []
    for i in range(1, len(format_cript)):
        freq_matrix.append([-1]*i + cript_num[:-i])

    rows_freq = [0]
    for cript in freq_matrix:
        freq = 0
        for n, letter in enumerate(cript):
            if letter == cript_num[n]:
                freq += 1
        rows_freq.append(freq)

    rows_freq = np.array(rows_freq)
    desvio = np.std(rows_freq)
    media = np.mean(rows_freq)
    cutoff = desvio * cutoff_factor
    lsup = media + cutoff
    lsup_outliers = np.where(rows_freq > lsup)[0]

    len_freqs = np.diff(lsup_outliers).tolist() # diff between each subsequent lsup_outliers
    most_freq_len = max(set(len_freqs), key=len_freqs.count)

    return most_freq_len

def find_key(criptograma, idioma = 'i'):
    format_cript = format_str(criptograma)
    stats_lang = stats_port if idioma == 'p' else stats_ing
    stats_lang = [stats_lang[l] for l in alfabeto]

    key_size = find_key_size(format_cript)
    key = ''
    for i in range(0, key_size):
        subcript = format_cript[i::key_size]
        stats_sub = calc_stats(subcript)
        
        max_accuracy, max_j = 0, 0
        for j in range(len(alfabeto)):
            shifted_alf = alfabeto[j:] + alfabeto[:j]
            shifted_stats = [stats_sub[l] for l in shifted_alf]
            result = sum([l * s for l, s in zip(stats_lang, shifted_stats)])
            
            if (result > max_accuracy):
                max_accuracy, max_j = result, j
        key += alfabeto[max_j]
                
    return key

def print_prop(label, value, size=50):
    print('{:=^{}}'.format(f' {label} ', size))
    print(value)
    print('=' * size)

def main():
    while True:
        print('Selecione um número:')
        print('1- Cifrar')
        print('2- Decifrar')
        print('3- Atacar')
        print('4- Encerrar')
        escolha = int(input())
        if (escolha == 1):
            msg = input('Escreva a mensagem: ')
            chave = input('Informe a chave: ')
            print_prop('CHAVE USADA', chave)
            print_prop('MENSAGEM CIFRADA', cifrador(msg, chave))
        elif (escolha == 2):
            cript = input('Informe o criptograma: ')
            chave = input('Informe a chave: ')
            print_prop('CHAVE USADA', chave)
            print_prop('MENSAGEM DECIFRADA', decifrador(cript, chave))
        elif (escolha == 3):
            while True:
                idioma = input('Informe o idioma (P/I): ')
                if (idioma.lower() == 'p' or idioma.lower() == 'i'):
                    break
                print('Idioma inválido')
            cript = input('Informe o criptograma: ')
            chave = find_key(cript, idioma)
            print_prop('CHAVE DESCOBERTA', chave)
            print_prop('MENSAGEM DECIFRADA', decifrador(cript, chave))
        elif (escolha == 4):
            break
        else:
            print('Escolha um número válido')

main()
