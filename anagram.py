import hashlib
import itertools
import re
import unidecode

regex = re.compile('[^a-zA-Z]')

def strip_text(text0):
    text1 = unidecode.unidecode(text0)
    text2 = regex.sub('',text1)
    return text2

source = 'poultry outwits ants'
source_stripped = strip_text(source) #18 (no spaces, no apostrophes)
source_length = 18 #len(source_stripped)
md5_1 = 'e4820b45d2277f3844eac66c903e84be'
md5_2 = '23170acc097c24edb98fc5488ab033fe'
md5_3 = '665e5bcb0c20062fe8abaaf4628bb154'

def string_to_dict(string):
    #convert the input string into a dict: {'letter':number of ocurences,...}
    #stripped text should be converted!!!
    dict = {}
    for i in string: #generate an unsorted dict.
        if i not in dict.keys():
            dict[i] = 1
        else:
            dict[i] += 1
    #sort the dict by the key alphabetically
    keylist = sorted(dict)
    sorted_dict = {}
    for key in keylist:
        sorted_dict[key] = dict[key]
    return sorted_dict

def md5 (input):
    return hashlib.md5(input.encode('utf-8')).hexdigest()

source_dict = string_to_dict(source_stripped)
source_dict_length = len(source_dict.keys())


#GENERATE THE REDUCED WORDLIST
wordlist_reduced = open('C:\\Users\\slava.sukhoy\\Desktop\\DataScience\\python\\wordlist_reduced','r+')
wordlist_reduced.truncate(0) #Cleanup the file from the previous values

wordlist = open('C:\\Users\\slava.sukhoy\\Desktop\\DataScience\\python\\wordlist','r')

wordlist_reduced_list = []
wordlist_reduced_text = ''
word_count = 0
#FILTER1: reduce the wordlist to the words that have the letters same as in the source sentence
for line in wordlist:
    line = line.rstrip('\n')
    line_stripped = strip_text(line) #strip the line, remove the junk and convert accents, umlauts etc.
    line_dict = string_to_dict(line_stripped) #convert a given word into a dict
    is_candidate = True #will become false if at least one letter isn't in the sourcee
    for i in line_dict.keys(): #for each letter in the word:
        if i in source_dict.keys():
            a = line_dict[i]
            b = source_dict[i] 
            if line_dict[i] <= source_dict[i]:
                is_candidate = True
            else:
                is_candidate = False
                break
        else:
            is_candidate = False
            break
    if is_candidate:
        if line not in wordlist_reduced_list:
            wordlist_reduced_list.append(line)
            wordlist_reduced.write(line+'\n')
            word_count += 1
        else:
            None
wordlist_reduced.close()
print('number of word candidates found:', word_count)
#found 2496 words.
#END OF GENERATE THE REDUCED WORDLIST


#GENERATE RAW PHRASE LIST
wordlist_reduced = open('C:\\Users\\slava.sukhoy\\Desktop\\DataScience\\python\\wordlist_reduced','r')

wordlist_reduced_list = []
for line in wordlist_reduced: #push the reduced wordlist into a list from the file
    line = line.rstrip('\n')
    wordlist_reduced_list.append(line)

end = 2496
start = 0
#generate backbone uinteger list for generation of phrases, 2691 - number of words
master_array = list(range(start, end))

#last_tested = [4,915,1066] #fast forward to the loast tested

#generate the permutations of the found raw phrase and check if any of the permutations have the right MD5
def permutations (phrase_raw):
    phrase_list = list(phrase_raw.split(' '))
    for phrase_variant_lst in itertools.permutations(phrase_list):
        phrase_variant = ''
        for word in phrase_variant_lst:
            if phrase_variant == '':
                phrase_variant = word
            else:
                phrase_variant = phrase_variant + ' ' + word
        checksum = md5(phrase_variant)
        if checksum == md5_1: #'e4820b45d2277f3844eac66c903e84be'
            print ('Solution 1: ', phrase_variant, ' md5 = ', md5_1)
            with open('C:\\Users\\slava.sukhoy\\Desktop\\DataScience\\python\\anagram_solutions','a+') as solutions:
                solutions.append('Solution 1: ' + phrase_variant + ' md5 = ' + md5_1 +'\n')
                solutions.close
        elif checksum == md5_2: #'23170acc097c24edb98fc5488ab033fe'
            print ('Solution 2: ', phrase_variant, ' md5 = ', md5_2)
            with open('C:\\Users\\slava.sukhoy\\Desktop\\DataScience\\python\\anagram_solutions','a+') as solutions:
                solutions.append('Solution 2: ' + phrase_variant + ' md5 = ' + md5_2 +'\n')
                solutions.close
        elif checksum == md5_3: #'665e5bcb0c20062fe8abaaf4628bb154'
            print ('Solution 3: ', phrase_variant, ' md5 = ', md5_3)
            with open('C:\\Users\\slava.sukhoy\\Desktop\\DataScience\\python\\anagram_solutions','a+') as solutions:
                solutions.append('Solution 3: ' + phrase_variant + ' md5 = ' + md5_3 +'\n')
                solutions.close
        else:
            return None

#Generate and write in the file the phrases with the number of letters 18 (no permutations)
#and number of each letter occurence is the same as in the source
for n in [3,4,5,6]: #n - number of words in the phrase
    key = 0
    for i_lst in itertools.combinations_with_replacement(master_array, n):
        #i - list of numbers to test
        phrase = ''
        for j in i_lst:
            if phrase == '':
                if phrase == '':
                    phrase = wordlist_reduced_list[j]
            else:
                phrase = phrase + ' ' + wordlist_reduced_list[j]
        phrase_stripped =  strip_text(phrase)
        if len(phrase_stripped) == 18: #if length is OK, then compare the dict
            phrase_dict = string_to_dict(phrase_stripped)
            if len(phrase_dict.keys()) == source_dict_length:
                if phrase_dict == source_dict:
                    with open('C:\\Users\\slava.sukhoy\\Desktop\\DataScience\\python\\raw_phrases','a+') as raw_phrases:
                        raw_phrases.write(phrase + '\n')
                        raw_phrases.close()
                    permutations(phrase)
#END OF GENERATE RAW PHRASE LIST
