import re

alfabeto = 'abcdefghijklmnopqrstuvwxyz';
alfatonum = dict(zip(alfabeto, range(len(alfabeto))));

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
    stats = { l: 0 for l in alfabeto }
    for c in format_msg:
        stats[c] += 1

    for l in stats:
        stats[l] /= len(format_msg)

    return stats

def descobre_mensagem(criptograma, eh_portugues = False):
    stats = calc_stats(criptograma)
    stats_script = sorted(stats.keys(), key=stats.get, reverse=True)
    print(stats_script)

    lang = stats_port if eh_portugues else stats_ing
    stats_lang = sorted(lang.keys(), key=lang.get, reverse=True)
    print(stats_lang)

    alf_dict = dict(zip(stats_script, stats_lang))
    print(alf_dict)
    # print(criptograma)
    msg = ''.join([alf_dict[c] for c in criptograma])

    return msg

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

def key_size(criptograma):
    # print(criptograma)
    cript_num = [alfatonum[c] for c in criptograma];
    # print(cript_num)
    freq_matrix = [];
    for i in range(1, len(criptograma)//3):
    # for i in range(1, len(criptograma)):
        freq_matrix.append([-1]*i + cript_num[:-i])

    rows_freq = [0];
    for cript in freq_matrix:
        freq = 0
        for n, letter in enumerate(cript):
            if letter == cript_num[n]:
                freq += 1
        rows_freq.append(freq)

    print(rows_freq)

    return freq_matrix;


msg_ing = "Something é é à ô that is impossible cannot be done or cannot happen.It was impossible for anyone to get in because no one knew the password. He thinks the tax is impossible to administer. You shouldn't promise what's impossible. Keller is good at describing music–an almost impossible task to do well. Synonyms: unachievable, hopeless, out of the question, vain   More Synonyms of impossibleThe impossible is something which is impossible.They were expected to do the impossible. No one can achieve the impossible."
encoded = cifrador(msg_ing, 'ketchup')
# encoded = cifrador('teste', 'ketchup')
print(key_size(encoded))
# decoded = decifrador(encoded, 'ketchup')
# descoberta = descobre_mensagem(encoded)

# print('-' * 30)
# print('encoded ' + encoded)
# print('-' * 30)
# print('descobre_mensagem ' + descoberta);
# print('-' * 30)
# print('decoded ' + decoded)
# print('-' * 30)



# msg_port = 'quenaoseconseguefazermuitodificildeconseguirmissaoimpossiveldeocorrencingiaouexistenciaexageradamentedificileimprovavelinviaveleimpossivelencontrardinheiroemarvoresquesedistanciadarealidadeirrealdesejoimpossivelcontrarioarazaosemsentidoracionalabsurdotravessiaimpossivelquenaoseconseguesuportarinsuportavelotrabalhoficouimpossivelnaempresa'
# msg_ing = 'somethingthatisimpossiblecannotbedoneorcannothappenitwasimpossibleforanyonetogetinbecausenooneknewthepasswordhethinksthetaxisimpossibletoadministeryoushouldntpromisewhatsimpossiblekellerisgoodatdescribingmusicanalmostimpossibletasktodowellsynonymsunachievablehopelessoutofthequestionvainmoresynonymsofimpossibletheimpossibleissomethingwhichisimpossibletheywereexpectedtodotheimpossiblenoonecanachievetheimpossible'



