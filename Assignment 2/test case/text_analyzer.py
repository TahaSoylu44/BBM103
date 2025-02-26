from sys import argv
import locale
locale.setlocale(locale.LC_ALL, "en_US")
with open(argv[1],"r",encoding="utf-8") as myinput:
        content=myinput.read().strip()
def main():      #It is my main function.Some values and lists are returned here.
    frequency={} #I needed a dictionary which contains of words as keys and words'frequencies as values.
    now=len(wlist(content))   #Calculated the number of words.
    for word in wlist(content):                       #This for loop for frequency of every word.
        frequency_words=wlist(content).count(word)/now
        frequency[word]="{:.4f}".format(frequency_words)
        #In here,I needed some sorting methods.I could not sort what I wanted in only one line.Thereby,I named some dictionaries primitive so as to resort them.Finally,I got what I expected :)
        sorted_dict_key_primitive=dict(sorted(frequency.items(),key=lambda x:(x[1],x[0]),reverse=True))
        sorted_dict_key_primitive2=dict(sorted(sorted_dict_key_primitive.items(),key=lambda x:(x[0])))
        sorted_dict_key=dict(sorted(sorted_dict_key_primitive2.items(),key=lambda x:(len(x[0]))))
        sorted_dict_value_primitive=dict(sorted(frequency.items(),key=lambda x:(x[0],len(x[0]))))
        sorted_dict_value=dict(sorted(sorted_dict_value_primitive.items(),key=lambda x:(x[1]),reverse=True))
        sorted_word_list_key=[]      #In here,I needed some lists to create my shortests and longests list.
        sorted_word_list_value=[]
        shortests=[]
        longests=[]
        counter=0
        for key,value in sorted_dict_key.items():
               sorted_word_list_key.append(key)
        for key,value in sorted_dict_value.items():
               sorted_word_list_value.append(key)
        for i in sorted_word_list_key:
               if len(i)==len(sorted_word_list_key[0]):
                shortests.append(i) 
        for i in sorted_word_list_key:
               if len(i)==len(sorted_word_list_key[-1]):
                      longests.append(i)
        for i in sorted_word_list_value:             #Meanwhile,I used i as variable for my "for loops" since it is my habit.
               if "'" in i:
                      try:
                             if i[i.index("'")+1]!=" ":      #It is complicated part.We should consider the words which include the apostrophe in the middle as a word.However,there are some words like "arms'".For such an example,I ought not to add this word in "Word and Frequencies" part and I handled it.
                                    continue                 
                      except:
                             sorted_word_list_value.remove(i)
        for i in wlist(content):
               if "'" in i:
                      try:
                             if i[i.index("'")+1]!=" ":       #While calculating only characters of words,there is a problem if the words include the apostrophe in the end.I handled it with my counter variable.
                                    continue                 
                      except:
                             counter+=1
    AweNumWor="{:.2f}".format(len(wlist(content))/nos(content)) if nos(content)!=0 else 0    #Average Number of Words per Sentence.
    return AweNumWor,frequency,now,sorted_dict_key,shortests,longests,sorted_word_list_key,sorted_word_list_value,sorted_dict_value,counter
def wlist(content):            #This function creates a list which includes the words.
        lower_case=[]           #This list includes lower case words which their originals have an uppercase letter.In my code,I seperarted this words via this list.
        seperated_words=[]           #While splitting my content,I encountered a problem.Python defines a word which actually includes two words due to comma.However,this is one word not two.For example,"Today,the" is not one word.To handle it,I needed a list.This list includes true ones.
        unwanted=[]           #This list for deleting some word groups I do not want to deal with.This list includes the words Python thinks as a one word such as "Today,the".
        wcontent=content.split()
        punctuations=[",",";","?","!",".",":","(",")","]","[","{","}","\"","/"]
        a=[]  #I could not find a special name for this list.If my word group such as "Today,the" includes a punctuation,I replaced the punctuation with white-space.This list contains them :)
        for i in wcontent:
                for k in punctuations:
                        if k in i:
                                unwanted.append(i)
                                i=i.replace(k," ")
                                a=i.split()   
                seperated_words.extend(a)
                a.clear()
        for i in unwanted:
                if i in wcontent:
                        wcontent.remove(i)
        wcontent.extend(seperated_words)
        for i in wcontent:
                if type(i)==str:
                        if i.lower()!=i: #By this loop I got lower case words which actually contain of uppercase word.
                                lower_case.append(i.lower())
        wcontent.extend(lower_case)           #I added new ones.
        for i in lower_case:
                if i.capitalize() in wcontent:
                        wcontent.remove(i.capitalize())      #I deleted old ones.
        while "" in wcontent:
               wcontent.remove("")    #Because of spliting my main wcontent list includes white spaces.I need to get rid of them.
        wcontent.sort()               #A sorted list is always nice :)
        return wcontent    
def nos(content):            #This function calculates the number of the sentences.
        wanted=[]
        punctuations=[".", "!", "?"]
        scontent=content.split()
        for i in scontent:
                for k in punctuations:
                        if k in i:
                                new=i.split(k)
                                for a in new:
                                        wanted.append(a)
                                        break
                                new.clear()
        return len(wanted)                                                                       
def noc(content):            #This function creates the character list.                 
        noccontent=[]
        for i in content:
            j=0               
            while j<len(i):
                noccontent.append(i[j])
                j+=1
        return noccontent
main()
print(content)
"""with open(argv[2],"w",encoding="utf-8") as file:
        file.write("Statistics about {} :\n".format(argv[1]))
        file.write(f"{'#Words':24}: {main()[2]}\n")
        file.write(f"{'#Sentences':24}: {nos(content)}\n")
        file.write(f"{'#Words/#Sentences':24}: {main()[0]}\n")
        file.write(f"{'#Characters':24}: {len(noc(content))}\n")
        file.write(f"{'#Characters (Just Words)':24}: {len(noc(wlist(content)))-main()[9]}\n")
        if len(main()[4])==1:
                file.write(f"{'The Shortest Word':24}: {main()[4][0]:24} ({main()[3][main()[4][0]]})\n")
        else:
                file.write(f"{'The Shortest Words':24}:\n")
                for i in main()[4]:
                        file.write(f"{i:24} ({main()[3][i]})\n")
        if len(main()[5])==1:
                file.write(f"{'The Longest Word':24}: {main()[5][0]:24} ({main()[3][main()[5][0]]})\n")
        else:
                file.write(f"{'The Longest Words':24}:\n")
                for i in main()[5]:
                        file.write(f"{i:24} ({main()[3][i]})\n")
        file.write(f"{'Words and Frequencies':24}:\n")
        for i in main()[7]:
               if i !=main()[7][-1]:
                file.write(f"{i:24}: {main()[8][i]}\n")     #If I do not use if-else,I may encounter an unnecessary line in the end of the output text :)
               else:
                file.write(f"{i:24}: {main()[8][i]}")"""