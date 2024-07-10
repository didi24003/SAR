#! -*- encoding: utf8 -*-

## Nombres: 

########################################################################
########################################################################
###                                                                  ###
###  Todos los métodos y funciones que se añadan deben documentarse  ###
###                                                                  ###
########################################################################
########################################################################

import argparse
import os
import re
from typing import Optional


#Método que ordena por el valor de la clave
def sort_dic_by_values(d:dict) -> list:
    return sorted(d.items(), key=lambda a: (-a[1], a[0]))

#Método que ordena por clave 
def sort_dic_by_keys(d:dict) -> list:
    return sorted(d.items(), key=lambda item: item[0]) 

class WordCounter:

    def __init__(self):
        """
           Constructor de la clase WordCounter
        """
        self.clean_re = re.compile('\W+')

    def write_stats(self, filename:str, stats:dict, use_stopwords:bool, full:bool):
        """
        Este método escribe en fichero las estadísticas de un texto
            
        :param 
            filename: el nombre del fichero destino.
            stats: las estadísticas del texto.
            use_stopwords: booleano, si se han utilizado stopwords
            full: boolean, si se deben mostrar las stats completas
        """

        with open(filename, 'w', encoding='utf-8', newline='\n') as fh:

            #Nº de líneas
            fh.write(f"Lines: {stats['nlines']}\n") 

            #Nº de palabras
            fh.write((f"Number words (including stopwords): {stats['nwords']}\n"))
            if use_stopwords:
                fh.write((f"Number words (without stopwords): {stats['nswords']}\n"))

            #Vocabulary 
            fh.write(f"Vocabulary size: {len(stats['word'])}\n") 

            #Símbolos
            fh.write(f"Number of symbols: {sum(stats['symbol'].values())}\n")
            
            #Símbolos distintos
            fh.write(f"Number of different symbols: {len(stats['symbol'])}\n")
            

            #Palabras ordenadas alfabéticamente
            fh.write('Words (alphabetical order):\n')
            if full:
               cont = 0
               for (word, num) in sort_dic_by_keys(stats['word']): #usamos el método sort_dic_by_keys porque nos interesa ordenar la clave alfabéticamente
                   fh.write(f"{word}: {num}\n")
            else:
                cont=0
                for (word, num) in sort_dic_by_keys(stats['word']):
                    if cont == 20:
                        break
                    fh.write(f"{word}: {num}\n")
                    cont += 1
            
            #Palabras ordenadas por frecuencia
            fh.write('Words (by frequency):\n')
            if full:
               for (word, num) in sort_dic_by_values(stats['word']): #usamos el método sort_dic_by_values porque queremos ordenadar de mayor a menor frecuencia
                   fh.write(f"{word}: {num}\n")
            else:
                cont=0
                for (word, num) in sort_dic_by_values(stats['word']):
                    if cont == 20:
                        break
                    fh.write(f"{word}: {num}\n")
                    cont += 1

            #Letras ordenadas alfabéticamente        
            fh.write('Symbols (alphabetical order):\n') 
            if full:
               for (word, num) in sort_dic_by_keys(stats['symbol']): 
                   fh.write(f"{word}: {num}\n")  
            else:
                for (word, num) in sort_dic_by_keys(stats['symbol'])[:20]:
                    fh.write(f"{word}: {num}\n")
                        

            #Letras ordenadas por frecuencia
            fh.write('Symbols (by frequency):\n')
            if full:
               for (word, num) in sort_dic_by_values(stats['symbol']): 
                   fh.write(f"{word}: {num}\n")
            else:
                cont=0
                for (word, num) in sort_dic_by_values(stats['symbol']):
                    if cont == 20:
                        break
                    fh.write(f"{word}: {num}\n")
                    cont += 1     

            #Si se activa la opción -b de biword
            if 'biword' in stats and stats['biword'] and 'bisymbol' in stats and stats['bisymbol'] and (stats['biword'] or stats['bisymbol']):

                #Biwords ordenados alfabéticamente
                fh.write('Word pairs (alphabetical order):\n')
                if full: 
                    for (word, num) in sort_dic_by_keys(stats['biword']):
                        fh.write(f'{word}: {num}\n')
                else:
                    cont=0
                    for (word, num) in sort_dic_by_keys(stats['biword']):
                        if cont == 20:
                            break
                        fh.write(f"{word}: {num}\n")
                        cont += 1     

                #Biwords ordenados por frecuencia
                fh.write('Word pairs (by frequency):\n')
                if full: 
                    for (word, num) in sort_dic_by_values(stats['biword']):
                        fh.write(f'{word}: {num}\n')
                else:
                    cont=0
                    for (word, num) in sort_dic_by_values(stats['biword']):
                        if cont == 20:
                            break
                        fh.write(f"{word}: {num}\n")
                        cont += 1  

                #Bisymbol ordenados alfabéticamente
                fh.write('Symbol pairs (alphabetical order):\n')
                if full: 
                    for (word, num) in sort_dic_by_keys(stats['bisymbol']):
                        fh.write(f'{word}: {num}\n')
                else:
                    cont=0
                    for (word, num) in sort_dic_by_keys(stats['bisymbol']):
                        if cont == 20:
                            break
                        fh.write(f"{word}: {num}\n")
                        cont += 1  

                #Bisymbol ordenados por frecuencia
                fh.write('Symbol pairs (by frequency):\n')
                if full: 
                    for (word, num) in sort_dic_by_values(stats['bisymbol']):
                        fh.write(f'{word}: {num}\n')
                else:
                    cont=0
                    for (word, num) in sort_dic_by_values(stats['bisymbol']):
                        if cont == 20:
                            break
                        fh.write(f"{word}: {num}\n")
                        cont += 1  

            #Prefijos por frecuencia
            fh.write("Prefixes (by frequency):\n")
            if full:
                for (prefix, num) in sort_dic_by_values(stats['prefix']):
                    fh.write(f"{prefix}-: {num}\n")
            else:
                cont=0
                for (prefix, num) in sort_dic_by_values(stats['prefix']):
                        if cont == 20:
                            break
                        fh.write(f"{prefix}-: {num}\n")
                        cont += 1  
            
            #Sufijos por frecuencia
            fh.write("Suffixes (by frequency):\n")
            if full:
                for (suffix, num) in sort_dic_by_values(stats['suffix']):
                    fh.write(f"-{suffix}: {num}\n")
            else:
                cont=0
                for (suffix, num) in sort_dic_by_values(stats['suffix']):
                        if cont == 20:
                            break
                        fh.write(f"-{suffix}: {num}\n")
                        cont += 1 
  
        

    def file_stats(self, fullfilename:str, lower:bool, stopwordsfile:Optional[str], bigrams:bool, full:bool):
        """
        Este método calcula las estadísticas de un fichero de texto

        :param 
            fullfilename: el nombre del fichero, puede incluir ruta.
            lower: booleano, se debe pasar todo a minúsculas?
            stopwordsfile: nombre del fichero con las stopwords o None si no se aplican
            bigram: booleano, se deben calcular bigramas?
            full: booleano, se deben montrar la estadísticas completas?
        """

        stopwords = set() if stopwordsfile is None else set(open(stopwordsfile, encoding='utf-8').read().split())


        # variables for results

        sts = {
                'nwords': 0,
                'nswords':0,
                'nlines': 0,
                'word': {},
                'symbol': {},
                'prefix': {},
                'suffix': {},
                'biword' : {},
                'bisymbol': {}

                }

        with_bigrams = bigrams 

        if with_bigrams:
            sts['biword'] = {}
            sts['bisymbol'] = {}

        new_filename = fullfilename.split('.')

        sufijo = ''
        if lower:
            sufijo += 'l'
        if stopwordsfile is not None:
            sufijo += 's'
        if bigrams:
            sufijo += 'b'       
        if full:
            sufijo += 'f'
        if not sufijo == '_':
             new_filename[0] += '_' + sufijo

        new_filename = new_filename[0] + '_stats.' + new_filename[1]


        with open(fullfilename, 'r', encoding = 'utf-8') as file:
            for line in file:
                # Contador de líneas
                sts['nlines'] += 1

                line = re.sub(self.clean_re, ' ', line)

                if lower:
                    line = line.lower()

                line = line.split()

                lastword = '$'
                for word in line:

                    sts['nwords'] = sts['nwords'] + 1

                    if stopwords != []:
                        if bigrams and lastword not in stopwords and word not in stopwords:
                            pair = lastword + ' ' + word
                            if pair not in sts['biword']:
                                sts['biword'][pair] = 1
                            else:
                                sts['biword'][pair] +=  1
                        lastword = word

                    if word not in stopwords: #si la palabra no es una stopword

                        sts['nswords'] +=  1 #sumamos uno al diccionario de las palabras sin stopwords
                        if word not in sts['word']:
                            sts['word'][word] = 1 #si no hay estadisticas guardadas de antes, inicializamos a 1 el contador 
                        else:
                            sts['word'][word] += 1

                        # Calcula prefijos
                        for i in range(2, min(len(word), 5)): #solo me interesa los prefijos de 2-3-4 letras
                            prefix = word[:i]
                            sts['prefix'][prefix] = sts['prefix'].get(prefix, 0) + 1

                        # Calcula sufijos
                        for i in range(2, min(len(word), 5)): #solo me interesa los sufijos de 2-3-4 letras
                            suffix = word[-i:]
                            sts['suffix'][suffix] = sts['suffix'].get(suffix, 0) + 1

 
                        if stopwords == []: 
                            if bigrams: #si tenemos activada la opción de bigrams procedemos a calcular las frecuencias de biwords
                                pair = lastword + ' ' + word
                                if pair not in sts['biword']:
                                    sts['biword'][pair] = 1
                                else:
                                    sts['biword'][pair] +=  1
                            lastword = word

                        lastchar = ''
                        for char in word:
                            if char not in sts['symbol']: #calcula la frecuencia de simbolos
                                sts['symbol'][char] = 1
                            else:
                                sts['symbol'][char] +=  1

                            if bigrams and lastchar != '': #si la opción bigrama está activada calculamos la frecuencia de bysimbolos
                                lastchar = lastchar + char
                                if lastchar not in sts['bisymbol']:
                                    sts['bisymbol'][lastchar] = 1
                                else:
                                    sts['bisymbol'][lastchar] += 1
                            lastchar = char

                if lastword != '$':  #si la ultima palabra no es un símbolo
                    if stopwords == []:
                        pair = lastword + ' ' + '$'  #añadimos esa palabra más el simbolo $
                        if pair not in sts['biword']:
                            sts['biword'][pair] = 1
                        else:
                            sts['biword'][pair] +=  1

                    elif lastword not in stopwords:
                        pair = lastword + ' ' + '$'
                        if pair not in sts['biword']:
                            sts['biword'][pair] = 1
                        else:
                            sts['biword'][pair] +=  1
                    lastword = '$' #esto lo establezco para que la próxima palabra, la primera de línea empiece por $

        self.write_stats(new_filename, sts, stopwordsfile is not None, full)


    def compute_files(self, filenames:str, **args):
        """
        Este método calcula las estadísticas de una lista de ficheros de texto

        :param 
            filenames: lista con los nombre de los ficheros.
            args: argumentos que se pasan a "file_stats".

        :return: None
        """

        for filename in filenames:
            self.file_stats(filename, **args)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Compute some statistics from text files.')
    parser.add_argument('file', metavar='file', type=str, nargs='+',
                        help='text file.')

    parser.add_argument('-l', '--lower', dest='lower',
                        action='store_true', default=False, 
                        help='lowercase all words before computing stats.')

    parser.add_argument('-s', '--stop', dest='stopwords', action='store',
                        help='filename with the stopwords.')

    parser.add_argument('-b', '--bigram', dest='bigram',
                        action='store_true', default=False, 
                        help='compute bigram stats.')

    parser.add_argument('-f', '--full', dest='full',
                        action='store_true', default=False, 
                        help='show full stats.')

    args = parser.parse_args()
    wc = WordCounter()
    wc.compute_files(args.file,
                     lower=args.lower,
                     stopwordsfile=args.stopwords,
                     bigrams=args.bigram,
                     full=args.full)
