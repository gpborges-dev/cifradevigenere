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
    return re.sub(r'[^a-z]', '', format_str);


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
    key_ext = key;
    while (len(format_msg) > len(key_ext)):
        key_ext += key;

    criptograma = '';
    for i, c in enumerate(format_msg):
        c_index = alfabeto.find(c)
        k_index = alfabeto.find(key_ext[i])
        criptograma += alfabeto[(c_index + k_index) % len(alfabeto)];
    
    return criptograma


def decifrador(criptograma, key):
    key_ext = key;
    while (len(criptograma) > len(key_ext)):
        key_ext += key;
    
    msg = '';
    for i, c in enumerate(criptograma):
        c_index = alfabeto.find(c)
        k_index = alfabeto.find(key_ext[i])
        msg += alfabeto[(c_index - k_index) % len(alfabeto)];
    
    return msg


def find_key_size(criptograma):
    cript_num = [alfatonum[c] for c in criptograma];
    freq_matrix = [];
    for i in range(1, len(criptograma)):
        freq_matrix.append([-1]*i + cript_num[:-i])

    rows_freq = [0];
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


def find_key(criptograma, eh_portugues = False):
    stats_lang = stats_port if eh_portugues else stats_ing
    stats_lang = [stats_lang[l] for l in alfabeto]

    key_size = find_key_size(criptograma)
    key = ''
    for i in range(0, key_size):
        subcript = criptograma[i::key_size]
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
###################

key = 'ketchup'
msg_ing = "Something that is impossible cannot be done or cannot happen.It was impossible for anyone to get in because no one knew the password. He thinks the tax is impossible to administer. You shouldn't promise what's impossible. Keller is good at describing music–an almost impossible task to do well. Synonyms: unachievable, hopeless, out of the question, vain   More Synonyms of impossibleThe impossible is something which is impossible.They were expected to do the impossible. No one can achieve the impossible."
encoded = cifrador(msg_ing, key)
found_key = find_key(encoded)
found_decoded = decifrador(encoded, found_key)

print_prop('CHAVE', key)
print_prop('MENSAGEM ORIGINAL', msg_ing)
print_prop('MENSAGEM CIFRADA', encoded)
print_prop('CHAVE DESCOBERTA', found_key)
print_prop('MENSAGEM DESCOBERTA', found_decoded)


# msg_port = 'quenaoseconseguefazermuitodificildeconseguirmissaoimpossiveldeocorrencingiaouexistenciaexageradamentedificileimprovavelinviaveleimpossivelencontrardinheiroemarvoresquesedistanciadarealidadeirrealdesejoimpossivelcontrarioarazaosemsentidoracionalabsurdotravessiaimpossivelquenaoseconseguesuportarinsuportavelotrabalhoficouimpossivelnaempresa'
# msg_ing = 'somethingthatisimpossiblecannotbedoneorcannothappenitwasimpossibleforanyonetogetinbecausenooneknewthepasswordhethinksthetaxisimpossibletoadministeryoushouldntpromisewhatsimpossiblekellerisgoodatdescribingmusicanalmostimpossibletasktodowellsynonymsunachievablehopelessoutofthequestionvainmoresynonymsofimpossibletheimpossibleissomethingwhichisimpossibletheywereexpectedtodotheimpossiblenoonecanachievetheimpossible'



