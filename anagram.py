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

'''
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
'''

#GENERATE RAW PHRASE LIST
wordlist_reduced = open('C:\\Users\\slava.sukhoy\\Desktop\\DataScience\\python\\wordlist_reduced','r')

wordlist_reduced_list = []
for line in wordlist_reduced: #push the reduced wordlist into a list from the file
    line = line.rstrip('\n')
    wordlist_reduced_list.append(line)

end = 2496
start = 4
#generate backbone uinteger list for generation of phrases, 2691 - number of words
master_array = list(range(start, end))

#last_tested = [4,915,1066] #fast forward to the loast tested

#Generate and write in the file the phrases with the number of letters 18 (no permutations)
#next step will be to generate the permutations of the found phrases
for n in [3,4,5,6]: #n - number of words in the phrase
key = 0
    for i_lst in itertools.combinations_with_replacement(master_array, n):
        #fast forward to the last tested
        if i_lst == last_tested:
            break

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
#        with open('C:\\Users\\slava.sukhoy\\Desktop\\DataScience\\python\\raw_phrases_last_processed', 'w+') as raw_phrases_last_processed:
#            i_string = ','.join(map(str, i))
#            raw_phrases_last_processed.write('['+i_string + '] : [' + phrase + ']')
#            raw_phrases_last_processed.close()
        if len(phrase_stripped) == 18: #if length is OK, then compare the dict
            phrase_dict = string_to_dict(phrase_stripped)
            if len(phrase_dict.keys()) == source_dict_length:
                if phrase_dict == source_dict:
                    with open('C:\\Users\\slava.sukhoy\\Desktop\\DataScience\\python\\raw_phrases','a+') as raw_phrases:
                        raw_phrases.write(phrase + '\n')
                        raw_phrases.close()
#END OF GENERATE RAW PHRASE LIST
'''
def phrase_constructor(list,wordlist,sub_list):
    phrase = ''
    for i in list:
        if phrase == '':
            phrase = wordlist[i]
        else:
            phrase = phrase + ' ' + wordlist[i]
    phrase_stripped = strip_text(phrase)
    phrase_length = len(phrase_stripped)

#this piece just to record the last processed combination in the file
    list_text = ''
    for j in sub_list:
        if list_text == '':
            list_text = str(j)
        else:
            list_text = list_text + ',' + str(j)
    with open('C:\\Users\\slava.sukhoy\\Desktop\\DataScience\\python\\last_checked_combination','w+') as log:
        log.write('Combination [' + list_text + '], phrase: [' + phrase + ']')
        log.close()
    
    if phrase_length == source_length:
        phrase_dict = string_to_dict(phrase_stripped)
        if phrase_dict == source_dict:
        #if (md5(phrase) == 'md5_1' or md5(phrase) ==  'md5_2' or md5(phrase) ==  'md5_3'):
            with open('C:\\Users\\slava.sukhoy\\Desktop\\DataScience\\python\\phrases_to_test','a+') as file:
                file.write(phrase + '\n')
                file.close()
            return phrase
    else:
        return 'zz'

def permutation(lst): #generate all permutations for each list generated by printCombinations
    #https://www.geeksforgeeks.org/generate-all-the-permutation-of-a-list-in-python/
    if len(lst) == 0:
        return []
    if len(lst) == 1:
        return [lst]
    l = []
    b = range(len(lst))
    for i in range(len(lst)):
       m = lst[i]
       remLst = lst[:i] + lst[i+1:]
       for p in permutation(remLst):
           l.append([m] + p)
    return l

def printCombination(arr, arr_len, sub_arr_len): #triggers generation of combinations of the lists
#https://www.geeksforgeeks.org/print-all-possible-combinations-of-r-elements-in-a-given-array-of-size-n/      
    data = [0]*sub_arr_len
    combinationUtil(arr, data, 0, arr_len - 1, 0, sub_arr_len)
                    # arr[]:       Input/master Array
                    # data[]:      Temporary array to store current combination 
                    # start & end: Staring and Ending indexes of the input array arr[]
                    # index:       Current index in data[] (data[] has length = r)
                    # r:           Length of the sub array

phrase_list = []



#generate combinations of numbers

def combinationUtil(arr, data, start, end, index, sub_arr_len):
    sub_array = []
    if (index == sub_arr_len):
        for j in range(sub_arr_len):
            sub_array.append(data[j])
        #1-st round - find the phrases that have the same length as the source

        
        #Permutations will not be used at the 1-st round.
        for p in permutation(sub_array): #p is array.
            +phrase = phrase_constructor(p, wordlist_reduced_list,sub_array)
            if phrase != 'zz':
                phrase_list.append(phrase)
            else:
                pass
        return phrase_list

    i = start #at start - i = 0
    while(i <= end and end - i + 1 >= sub_arr_len - index): # i <= length of the master array;
        data[index] = arr[i]
        combinationUtil(arr, data, i + 1, end, index + 1, sub_arr_len)
        i += 1 #go to the get member of the master array
'''

'''
arr = []

sub_arr_len = 3  #2 - checked, no hits (as expected)
arr_len = len(arr)
#ww = []
#ww = printCombination(arr, arr_len, sub_arr_len)
#print (ww)

for i in itertools.combinations_with_replacement(arr, sub_arr_len):
    phrase = ''
    for j in i:
        if phrase == '':
             if phrase == '':
            phrase = wordlist[i]
        else:
            phrase = phrase + ' ' + wordlist[i]
    phrase_stripped =  strip_text (phrase)
    if len(phrase_stripped) == 
    


'''
