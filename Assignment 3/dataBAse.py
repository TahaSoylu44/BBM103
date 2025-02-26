from sys import argv
import locale
locale.setlocale(locale.LC_ALL, "en_US")
import json
def main():
    with open(argv[1].strip(),"r",encoding="utf-8") as file:
        lines=file.readlines()
        command_list=[]
        joining=[]
        joined_list=[]
    for line in lines:
        if line!="\n":
            splitted_line=line.split()
            if splitted_line[0]=="CREATE_TABLE":
                table_name=splitted_line[1]
                columns=splitted_line[2].split(",")
                command_list.append((table_name,columns.copy()))
        else:
            continue 
    for line in lines:
        if line!="\n":
            splitted_line=line.split()
            if splitted_line[0]=="JOIN":
                tables=splitted_line[1].split(",")
                joining.append(tables[0])
                joining.append(tables.copy()[1])
                joining.append(splitted_line.copy()[3])
                joined_list.append(joining.copy())
                joining.clear() 
    def data_func(name):              #This function returns a list which includes both the name of the table and datas as dictionaries.
        datas=[]             #Keeps datas acquired from "INSERT" section as lists in a list.
        data_list=[]         #Keeps the table's name and datas as dictionaries.    
        columns_dict={}      #Was used to add datas to "data_list"
        conditions=[]
        condition_list=[]
        updating=[]
        deleting=[]
        counting=[]
        with open(argv[1].strip(),"r",encoding="utf-8") as file:
            lines=file.readlines()
            for line in lines:
                if line!="\n":
                    splitted_line=line.split()
                    if splitted_line[1]==name:
                        if splitted_line[0]=="CREATE_TABLE":
                            data_list.append(splitted_line[1])
                            columns=splitted_line[2].split(",")
            for line in lines:
                if line!="\n":
                    splitted_line=line.split()
                    if splitted_line[1]==name:
                        if splitted_line[0]=="INSERT":
                            counter=0
                            for index,character in enumerate(line):
                                if character==" ":
                                    counter+=1
                                    if counter==2:
                                        datas.append(line[(index+1):].strip().split(","))
            for i in datas:
                counter=0
                for k in i:
                    columns_dict.update({columns[counter]:k})
                    counter+=1
                    copied_dict=columns_dict.copy()
                data_list.append(copied_dict) 
            for line in lines:
                if line!="\n":
                    splitted_line=line.split()
                    if splitted_line[1]==name:
                        if splitted_line[0]=="SELECT":
                            conditions.append(splitted_line[1])
                            wanted=splitted_line[2].split(",")
                            for i in wanted:
                                conditions.append(i)
                            counter=0
                            for index,character in enumerate(line):
                                if character==" ":
                                    counter+=1
                                    if counter==4:
                                        conditions.append(line[(index+1):].strip())
                                        condition_list.append(conditions.copy())
                                        conditions.clear()
            for line in lines:
                if line!="\n":
                    splitted_line=line.split()
                    if splitted_line[1]==name:
                        if splitted_line[0]=="UPDATE":
                            updating.append(splitted_line[1])
                            wanted_start_index=line.find("{")
                            wanted_end_index=line.find("}")
                            condition_start_index=line.find("{",wanted_start_index+1)
                            condition_end_index=line.find("}",wanted_end_index+1)
                            updating.append(line[wanted_start_index:wanted_end_index+1])
                            updating.append(line[condition_start_index:condition_end_index+1])
            for line in lines:
                if line!="\n":
                    splitted_line=line.split()
                    if splitted_line[1]==name:
                        if splitted_line[0]=="DELETE":
                            deleting.append(splitted_line[1])
                            counter=0
                            for index,character in enumerate(line):
                                if character==" ":
                                    counter+=1
                                    if counter==3:
                                        be_deleted=line[(index+1):].strip()
                                        deleting.append(json.loads(be_deleted))               
            for line in lines:
                if line!="\n":
                    splitted_line=line.split()
                    if splitted_line[1]==name:
                        if splitted_line[0]=="COUNT":
                            counting.append(splitted_line[1])
                            start_index=line.find("{")
                            end_index=line.find("}")
                            counting.append(line[start_index:end_index+1])
        return data_list,condition_list,updating,deleting,counting
    return data_func,command_list,joined_list

def minus(a,b):       #Was used to determine the number of "-"
    return((max(len(str(a)),len(str(b)))+2)*"-")

def updated(table):
    DataList=table[1:].copy()
    if main()[0](name)[2]!=[]:
        condition_dict=json.loads(main()[0](name)[2][-1])
        wanted_dict=json.loads(main()[0](name)[2][1])
        condition_keys=tuple(condition_dict.keys())
        wanted_keys=tuple(wanted_dict.keys())
        for dictionary in table[1:]:
            k=0
            while k<len(condition_keys):
                try:
                    if condition_keys[k] in dictionary.keys():  
                        if condition_dict[condition_keys[k]]==dictionary[condition_keys[k]]:
                            if k==len(condition_keys)-1:
                                dictionary_index=DataList.index(dictionary)
                                DataList.remove(dictionary)
                                for wanted_key in wanted_keys:
                                    if wanted_key in dictionary.keys():
                                        dictionary.update({wanted_key:wanted_dict[wanted_key]})
                                DataList.insert(dictionary_index,dictionary.copy())
                            k+=1
                        else:
                            break
                        return DataList,None,None
                    else:
                        raise Exception
                except Exception:
                    nonexist_condition_column=condition_keys[k]
                    k+=1
            try:
                for wanted_key in wanted_keys:
                    if wanted_key in dictionary.keys():
                        return DataList,nonexist_condition_column,None
                    else:
                        raise KeyError
            except KeyError:
                nonexist_wanted_column=wanted_key
                return DataList,nonexist_condition_column,nonexist_wanted_column

def INSERT(table):
    mylist=[]         #It contains the data dictionaries.
    for dictionary in table[1:]:
        last_item=tuple(dictionary.keys())[-1]
    def TABLE():                 #This function faciliated printing the datas to the table.It contains the datas which will be printed.
        widths=[]
        nonlocal mylist
        nonlocal dictionary
        nonlocal last_item
        for anydict in mylist:
            for keys,value in anydict.items():
                WidthLists=[]         #Needed a list to determine what the largest string is.
                if keys!=last_item:
                    for i in mylist:
                        WidthLists.append(str(i[keys]))
                    width=max(len(str(keys)),len(max(WidthLists,key=len)))       #The lenght of the column
                    widths.append(width)
                    length=max(len(str(keys)),max(widths))
                    print(f"| {value:{width}} ",end="")
                else:
                    WidthLists.clear()
                    for i in mylist:
                        WidthLists.append(str(i[last_item]))
                    width=max(len(str(last_item)),len(max(WidthLists,key=len)))        #The lenght of the column
                    widths.append(width)
                    length=max(len(str(keys)),max(widths))
                    print(f"| {value:{width}} ",end="")
                    print("|")
    for dictionary in table[1:]:
        mylist.append(dictionary)
        last_item=tuple(dictionary.keys())[-1]            #I need the last item to print the table correctly.
        print(22*"#"+" "+"INSERT"+" "+25*"#")
        print(f"Inserted into '{table[0]}': {tuple(dictionary.values())}") 
        print()
        print(f"Table: {table[0]}")  
    
        for keys,value in dictionary.items():
            WidthLists=[]
            if keys!=last_item:
                for i in mylist:
                    WidthLists.append(str(i[keys]))
                width=max(len(str(keys)),len(max(WidthLists,key=len)))
                print("+"+(width+2)*"-",end="")
            else:
                WidthLists.clear()
                for i in mylist:
                    WidthLists.append(str(i[last_item]))
                width=max(len(str(last_item)),len(max(WidthLists,key=len)))
                print("+"+(width+2)*"-",end="")
                print("+")
    
        for keys,value in dictionary.items():
            WidthLists=[]
            if keys!=last_item:
                for i in mylist:
                    WidthLists.append(str(i[keys]))
                width=max(len(str(keys)),len(max(WidthLists,key=len)))               
                print(f"| {keys:<{width}} ",end="")
            else:
                for i in mylist:
                    WidthLists.append(str(i[keys]))
                width=max(len(str(keys)),len(max(WidthLists,key=len)))
                print(f"| {keys:<{width}} ",end="")
                print("|")

        for keys,value in dictionary.items():
            WidthLists=[]
            if keys!=last_item:
                for i in mylist:
                    WidthLists.append(str(i[keys]))
                width=max(len(str(keys)),len(max(WidthLists,key=len)))
                print("+"+(width+2)*"-",end="")
            else:
                for i in mylist:
                    WidthLists.append(str(i[keys]))
                width=max(len(str(keys)),len(max(WidthLists,key=len)))
                print("+"+(width+2)*"-",end="")
                print("+")
    
        TABLE()
        
        for keys,value in dictionary.items():
            WidthLists=[]
            if keys!=last_item:
                for i in mylist:
                    WidthLists.append(str(i[keys]))
                width=max(len(str(keys)),len(max(WidthLists,key=len)))
                print("+"+(width+2)*"-",end="")
            else:
                for i in mylist:
                    WidthLists.append(str(i[keys]))
                width=max(len(str(keys)),len(max(WidthLists,key=len)))
                print("+"+(width+2)*"-",end="")
                print("+")
        
        print(55*"#")
        print()

def CREATE(table):
    print(22*"#"+" "+"CREATE"+" "+25*"#")
    print(f"Table '{table[0]}' created with columns: {list(table[1].keys())}")
    print(55*"#")
    print()

def SELECT(table):
    selected=[]
    SubList=[]
    for lists in main()[0](name)[1]:
        condition_dictionary=json.loads(lists[-1])
        print(22*"#"+" "+"SELECT"+" "+25*"#")
        try:
            for dictionaries in table[1:]:
                if main()[0](name)[1][0][1] in dictionaries.keys() and main()[0](name)[1][0][2] in dictionaries.keys():
                    if tuple(condition_dictionary.keys())[0] in dictionaries.keys():
                        print(f"Condition: {condition_dictionary}")
                        for i in condition_dictionary.keys():
                            condition_key=i
                        for dictionaries in table[1:]:
                            if condition_dictionary[condition_key]==dictionaries[condition_key]:
                                if lists[1]=="*":
                                    for column in dictionaries.keys():
                                        SubList.append(dictionaries[column])
                                    selected.append(tuple(SubList.copy()))
                                    SubList.clear()
                                else:
                                    for column in lists[1:-1]:
                                        SubList.append(dictionaries[column])
                                    selected.append(tuple(SubList.copy()))
                                    SubList.clear()         
                        print(f"Select result from '{lists[0]}': {selected}")
                        selected.clear()
                        print(55*"#")
                        print()
                        break
                    else:
                        nonexisted=tuple(condition_dictionary.keys())[0]
                        raise KeyError
                else:
                    column1=main()[0](name)[1][0][1] in dictionaries.keys()
                    column2=main()[0](name)[1][0][2] in dictionaries.keys()
                    if column1:
                        nonexisted=main()[0](name)[1][0][2]
                    else:
                        nonexisted=main()[0](name)[1][0][1]
                    raise KeyError          
        except KeyError:
            print(f"Column {nonexisted} does not exist")
            print(f"Condition: {condition_dictionary}")
            print(f"Select result from '{table[0]}': None")
            print(55*"#")
            print()

def UPDATE(table):
    count=main()[0](name)[2].count(name)
    k=0
    while k<count:
        try:
            print(22*"#"+" "+"UPDATE"+" "+25*"#")
            print(f"Updated '{main()[0](name)[2][0]}' with {main()[0](name)[2][1]} where {main()[0](name)[2][2]}")
            if type(updated(table)[2])==str:
                print(f"Column {updated(table)[2]} does not exist")
                print("0 rows updated.")      
            elif type(updated(table)[1])==str:
                print(f"Column {updated(table)[1]} does not exist")
                print("0 rows updated.")
            else:
                print(f"{(len(main()[0](name)[2])-2)} rows updated.")
            print()
            print(f"Table: {main()[0](name)[2][0]}")
            mydict=[]
            WidthList=[]
            widths=[]
            columns=[]
            for dictionary in updated(table)[0]:
                last_item=tuple(dictionary.keys())[-1]    
            for dictionaries in updated(table)[0]:
                mydict.append(dictionaries.copy())
            for i in mydict:
                for column in i.keys():
                    columns.append(column)
                break
            for dictionary in mydict:
                for key in dictionary.keys():
                    for i in mydict:
                        WidthList.append(str(i[key]))
                    width=len(minus(key,max(WidthList,key=len)))
                    WidthList.clear()
                    widths.append(width)
                break
            def bars():
                nonlocal columns
                nonlocal last_item
                k=0
                while k<4:
                    for column in columns:
                        if column!=last_item:
                            print("+"+(widths[k])*"-",end="")
                            k+=1
                        else:
                            print("+"+(widths[k])*"-",end="")
                            print("+")
                            k+=1
            bars()
            k=0
            while k<4:
                for column in columns:
                    if column!=last_item:
                        print(f"| {columns[k]:<{widths[k]-2}} ",end="")
                        k+=1
                    else:
                        print(f"| {columns[k]:<{widths[k]-2}} ",end="")
                        print("|")
                        k+=1
            bars()  
            for data_dictionary in mydict:
                k=0
                while k<4:    
                    for value in data_dictionary.values():
                        if value!=None:
                            if value!=data_dictionary[last_item]:
                                print(f"| {value:<{widths[k]-2}} ",end="")
                                k+=1
                            else:
                                print(f"| {value:<{widths[k]-2}} ",end="")
                                print("|")
                                k+=1    
            bars()
            print(55*"#")
            print()
        except Exception:
            pass
        k+=1

def DELETE(table):
    nonexist_key=None
    if main()[0](name)[2]!=[]:
        DataList=updated(table)[0]
        if len(main()[0](name)[3])!=1:
            for i in main()[0](name)[3][-1].keys():
                condition_key=i
                for dictionary in table[1:]:
                    try:
                        if condition_key in dictionary.keys():
                            if str(main()[0](name)[3][-1][condition_key])==str(dictionary[condition_key]):
                                DataList.remove(dictionary)
                        else:
                            raise KeyError
                    except KeyError:
                        nonexist_key=condition_key
            print(22*"#"+" "+"DELETE"+" "+25*"#")
            print(f"Deleted from '{main()[0](name)[3][0]}' where {main()[0](name)[3][-1]}")
            if type(nonexist_key)==str:
                print(f"Column {nonexist_key} does not exist")
                print("0 rows deleted.")
            else:
                print(f"{(len(main()[0](name)[3][-1].keys()))} rows deleted.")
            print()
            print(f"Table: {main()[0](name)[3][0]}")
            mydict=[]
            WidthList=[]
            widths=[]
            columns=[]
            for dictionary in DataList:
                last_item=tuple(dictionary.keys())[-1]    
            for dictionaries in DataList:
                a=dictionaries.copy()
                mydict.append(a)
            for i in mydict:
                for column in i.keys():
                    columns.append(column)
                break
            for dictionary in mydict:
                for key in dictionary.keys():
                    for i in mydict:
                        WidthList.append(i[key])
                        width=len(minus(key,max(WidthList,key=len)))
                        WidthList.clear()
                    widths.append(width)
                break
            def bars():
                nonlocal columns
                nonlocal last_item
                k=0
                while k<4:
                    for column in columns:
                        if column!=last_item:
                            print("+"+(widths[k])*"-",end="")
                            k+=1
                        else:
                            print("+"+(widths[k])*"-",end="")
                            print("+")
                            k+=1
            bars()
            k=0
            while k<4:
                for column in columns:
                    if column!=last_item:
                        print(f"| {columns[k]:<{widths[k]-2}} ",end="")
                        k+=1
                    else:
                        print(f"| {columns[k]:<{widths[k]-2}} ",end="")
                        print("|")
                        k+=1
            bars()  
            for data_dictionary in mydict:
                k=0
                while k<4:    
                    for value in data_dictionary.values():
                        if value!=None:
                            if value!=data_dictionary[last_item]:
                                print(f"| {value:<{widths[k]-2}} ",end="")
                                k+=1
                            else:
                                print(f"| {value:<{widths[k]-2}} ",end="")
                                print("|")
                                k+=1    
            bars()
            print(55*"#")
            print()
        else:
            print(22*"#"+" "+"DELETE"+" "+25*"#")
            print(f"Table: {main()[0](name)[3][0]}")
            print("There is no specified condition.All columns were deleted.")
            print(55*"#")

def COUNT(table):
    no_column=None
    if main()[0](name)[2]!=[]:
        DataList=updated(table)[0]
        for i in main()[0](name)[3][-1].keys():
            condition_key=i
            for dictionary in table[1:]:
                try:
                    if condition_key in dictionary.keys():
                        if str(main()[0](name)[3][-1][condition_key])==str(dictionary[condition_key]):
                            DataList.remove(dictionary)
                    else:
                        raise KeyError
                except KeyError:
                    pass     
        condition_dict=json.loads(main()[0](name)[4][-1])
        conditions=tuple(condition_dict.keys())
        counter=0
        for condition in conditions:
            for dictionary in DataList:
                try:
                    if condition in dictionary.keys():
                        if condition_dict[condition]==dictionary[condition]:
                            counter+=1
                    else:
                        raise KeyError
                except KeyError:
                    no_column=condition
        print(22*"#"+" "+"COUNT"+" "+25*"#")
        if type(no_column)==str:
            print(f"Column {no_column} does not exist")
            print(f"Total number of entries in {main()[0](name)[4][0]} is 0")
        else:
            print(f"Count: {counter}")
            print(f"Total number of entries in '{main()[0](name)[4][0]}' is {counter}")
        print(55*"#")
        print()

def JOIN():
    if len(main()[2])>=1:
        for join_list in main()[2]:
            table1=join_list[0]
            table2=join_list[1]
            common=join_list[-1]
            table1_DataList=main()[0](table1)[0][1:]
            table2_DataList=main()[0](table2)[0][1:]  
        counter=0
        try:
            if common in table1_DataList[0].keys() and common in table2_DataList[0].keys():
                for data_dict in table1_DataList:
                    for anydict in table2_DataList:
                        last_item=tuple(anydict.keys())[-1]
                        if data_dict[common]==anydict[common]:
                            for value in anydict.values():
                                if value!=anydict[last_item]:
                                    continue
                                else:
                                    counter+=1
                print(23*"#"+" "+"JOIN"+" "+26*"#")
                print(f"Join tables {table1} and {table2}")
                print(f"Join result ({counter} rows):")
                print()
                print("Table: joined table")
                def joined_table():   
                    mydict=[]
                    WidthList=[]
                    widths1=[]
                    columns=[]
                    for dictionary in table1_DataList:
                        last_item=tuple(dictionary.keys())[-1]    
                    for dictionaries in table1_DataList:
                        mydict.append(dictionaries.copy())
                    for i in mydict:
                        for column in i.keys():
                            columns.append(column)
                        break
                    for dictionary in mydict:
                        for key in dictionary.keys():
                            for i in mydict:
                                WidthList.append(str(i[key]))
                            width=len(minus(key,max(WidthList,key=len)))
                            WidthList.clear()
                            widths1.append(width)
                        break
                    mydict=[]
                    WidthList=[]
                    widths2=[]
                    columns=[]
                    for dictionary in table2_DataList:
                        last_item=tuple(dictionary.keys())[-1]    
                    for dictionaries in table2_DataList:
                        a=dictionaries.copy()
                        mydict.append(a)
                    for i in mydict:
                        for column in i.keys():
                            columns.append(column)
                        break
                    for dictionary in mydict:
                        for key in dictionary.keys():
                            for i in mydict:
                                WidthList.append(str(i[key]))
                            width=len(minus(key,max(WidthList,key=len)))
                            WidthList.clear()
                            widths2.append(width)
                        break  
                    def bar():
                        for data_dict in table1_DataList:
                            k=0
                            for keys in data_dict.keys():
                                print("+"+widths1[k]*"-",end="")
                                k+=1
                            break
                        for anydict in table2_DataList:
                            k=0
                            for keys in anydict.keys():
                                if keys!=tuple(anydict.keys())[-1]:
                                    print("+"+widths2[k]*"-",end="")
                                    k+=1
                                else:
                                    print("+"+widths2[k]*"-",end="")
                                    print("+")
                            break
                    bar()
                    for data_dict in table1_DataList:
                        k=0
                        for keys in data_dict.keys():
                            print(f"| {keys:<{widths1[k]-2}} ",end="")
                            k+=1
                        break
                    for anydict in table2_DataList:
                        k=0
                        for keys in anydict.keys():
                            if keys!=tuple(anydict.keys())[-1]:
                                print(f"| {keys:<{widths2[k]-2}} ",end="")
                                k+=1
                            else:
                                print(f"| {keys:<{widths2[k]-2}} ",end="")
                                print("|")
                        break
                    bar()
                    for data_dict in table1_DataList:
                        for anydict in table2_DataList:
                            last_item=tuple(anydict.keys())[-1]
                            if data_dict[common]==anydict[common]:
                                k=0
                                for value in data_dict.values():
                                    print(f"| {value:<{widths1[k]-2}} ",end="")
                                    k+=1
                                k=0
                                for value in anydict.values():
                                    if value!=anydict[last_item]:
                                        print(f"| {value:<{widths2[k]-2}} ",end="")
                                        k+=1
                                    else:
                                        print(f"| {value:<{widths2[k]-2}} ",end="")
                                        print("|")
                    bar()
                joined_table()
                print(55*"#")
                print()
            else:
                raise KeyError
        except KeyError:
            print(23*"#"+" "+"JOIN"+" "+26*"#")
            print(f"Join tables {table1} and {table2}")
            print(f"Column {common} does not exist")
            print(55*"#")
            print()

if __name__=="__main__":
    for tuples in main()[1]:
        name=tuples[0]
        main()[0](name)
        CREATE(main()[0](name)[0])
        INSERT(main()[0](name)[0])
        SELECT(main()[0](name)[0])
        UPDATE(main()[0](name)[0])
        DELETE(main()[0](name)[0])
        COUNT(main()[0](name)[0])
    JOIN()