####################################
# => WordlistGenerator <=          #
# By 000Tonio                      #
# https://github.com/000Tonio      #                 
####################################

import itertools
from collections import Counter
from datetime import datetime
import os.path


print ("\n---------------------------------------")
print ("  |-----> WordlistGenerator v 1.0.0 <---|")
print ("  ---------------------------------------")
print ("  |    By 000Tonio                      |")
print ("  |    https://github.com/000Tonio      |")
print ("  =======================================\n")
print ("\n")

keywords = input("Mot clés sur la personne (Divisé avec ','): ")

words=keywords.split(",")
length_words = len(words)

if(length_words<=0 or len(keywords.strip())<=0):
    print("\n\tDésolé , vous devez sesire au moin un mot. GOODBYE!\n")
    exit()

length_numbers=0
numbers_entered = input("Numéro en rapport avec la personne (Divisé avec ','): ")
numbers=numbers_entered.split(",")
length_numbers=len(numbers)

length_pointings=0
rule_pointings = input("Des mots contiennent ces signes de ponctuation ( Ex: '. , _'): ")
pointings=rule_pointings.split(" ")
length_pointings=len(pointings)

 
character_limit=None
try:
    character_limit=int(input("Combien de lettre contien le mot au maximum? (Ex: 12): "))
except ValueError:
    print("\n\tVous devez rentrer un chiffre . Merci!\n")
    try:
        character_limit=int(input("Combien de lettre contien le mot au maximum? (Ex: 12): "))
    except ValueError:
        print("\n\tGoodbye!")
        exit()


words_lists=[]
words_lists_with_number=[]
complex_words=[]
complex_words_removed=[]

all_words=[]


for counter in range(0,length_words):
    words_lists.append([])

for counter in range(0,length_words):
    words_lists_with_number.append([])

#Informations
print("\n\tWord(s):{}\n\tPonctuation(s):{}\n\tNombre(s):{}\n".format(length_words,length_pointings or None,length_numbers or None))

def generate_word(words, min, max):

    for i in range(int(min), int(max)+1):
        for j in itertools.product(words, repeat=i):
            
            counter_for_join_word=len(j)
         
            counter_list = Counter(j)
            
            for element in j:
                if (counter_list[element]<3):
                   
                    if not ''.join(j) in words_lists[counter_for_join_word-1]:
                        words_lists[counter_for_join_word-1].append(''.join(j))
                     
                        add_numbers(''.join(j),counter_for_join_word-1) if length_numbers>0 else False

                  
                    if(length_pointings>0 and len(j)==1):
                        for mark in pointings:
                         
                            if not j[0]+mark in words_lists[0]:
                                words_lists[0].append(j[0]+mark)
                                
                                add_numbers(j[0]+mark,0) if length_numbers>0 else False
                           
                            if not mark+j[0] in words_lists[0]:
                                words_lists[0].append(mark+j[0])
                              
                                add_numbers(mark+j[0],0) if length_numbers>0 else False


                    if(length_pointings > 0 and len(j) > 1):
                        for mark in pointings:
                            if not mark.join(j) in words_lists[counter_for_join_word-1]:
                                words_lists[counter_for_join_word-1].append(mark.join(j))
                                
                                add_numbers(mark.join(j),counter_for_join_word-1) if length_numbers>0 else False
    all_words.append(words_lists)


def add_numbers(word_for_add, howmanywords):
  
    for number in numbers:
       
        if not number+word_for_add in words_lists[howmanywords]:
            words_lists_with_number[howmanywords].append(number+word_for_add)
            
        if not word_for_add+number in words_lists[howmanywords]:
            words_lists_with_number[howmanywords].append(word_for_add+number)
            
    all_words.append(words_lists_with_number)


def generate_complex():
    for words_list in words_lists:
        for word in words_list:
            for words_list_with_number in words_lists_with_number:
                for word_with_number in words_list_with_number:
                    complex_words.append(word+word_with_number)

    for complex_word in complex_words:
        for word_to_count in words:
            if(complex_word.count(word_to_count)>1):
                
                complex_words_removed.append(complex_word)

    complex_words_finally=list(set(complex_words).difference(complex_words_removed))
    
    all_words.append(complex_words_finally)

generate_word(words, 1, length_words)
generate_complex()


file_existed_checked=0


filename=None


word_counter=0


added_words=[]
def write_words_from_list(all_words_list):
    global file_existed_checked
    global filename
    global word_counter
    global character_limit
    global added_words

    if(file_existed_checked==0):
        filename="password_list-{}.txt".format(datetime.now().strftime('%H-%M'))
        filename=file_existed(filename)
        file_existed_checked=1

    password_list_file=open(filename,mode='a')

    for item in all_words_list:
        if(type(item)==list):
            write_words_from_list(item)
        elif(type(item)==str):
            if(character_limit is not None):
                if(len(item)<=character_limit):
                    if(item not in added_words):
                        password_list_file.write("{}\n".format(item))
                        added_words.append(item)
                        word_counter+=1
            else:
                if(item not in added_words):
                    password_list_file.write("{}\n".format(item))
                    added_words.append(item)
                    word_counter+=1
        else:
            print("Type inconnu: ",item)

    password_list_file.close()
   

def file_existed(filename_for_check,counter=0):
    global filename
    if(os.path.isfile(filename_for_check)):
        new_counter=counter+1
        new_filename="password_list-{}({}).txt".format(datetime.now().strftime('%H-%M'),new_counter)
        return file_existed(new_filename,new_counter)
    else:
       
        filename=filename_for_check
        return filename

write_words_from_list(all_words)
print("\t{} Wordlist générés. Vous pouvez voir ces mots à {}\n".format(word_counter,filename))
