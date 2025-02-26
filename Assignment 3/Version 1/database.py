from sys import argv
import locale
locale.setlocale(locale.LC_ALL, "en_US")
def main():
    datas=[]
    data_list=[]
    columns_dict={}
    with open(argv[1].strip(),"r",encoding="utf-8") as file:
        lines=file.readlines()
        for line in lines:
            splitted_line=line.split()
            if splitted_line[0]=="CREATE_TABLE":
                data_list.append(splitted_line[1])
                columns=splitted_line[2].split(",")     
        def INSERT():
            for line in lines:
                splitted_line=line.split()
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
                data_list.append(columns_dict)
        INSERT()
    return data_list
main()

def CREATE():
    print(22*"#"+" "+"CREATE"+" "+25*"#")
    print(f"Table '{main()[0]}' created with columns: {list(main()[1].keys())}")
    print(55*"#")
    print()







































