def empty_productions(text):
    temp = {}
    empty = {}
    start = text[0]
    nullable = []
    text = text.split("\n")
    for i in text:
        temp[i.split("->")[0]] = i.split("->")[1]
        empty[i.split("->")[0]] = i.split("->")[1]
        if(i.split("->")[1].count("$")>0):
            nullable.append(i.split("->")[0])
    for i in nullable:
        for j in empty.keys():
            empty[j] = empty[j].replace(i, "$")
            for k in empty[j].split("|"):
                if (len(k) == k.count("$")):
                    if (j in nullable):
                        continue
                    else:
                        nullable.append(j)
    text = ""
    for i in temp.keys():
        text = text + i + "->"
        temp[i] = temp[i].split("|")
        for j in temp[i]:
            for k in range(len(j)):
                if j[k] in nullable:
                    temp[i].append(j[0:k]+j[k+1:])
        temp[i]  = set(temp[i])
        if ("" in temp[i]):
            temp[i].remove("")
        if(i==start):
            if(i in nullable):
                temp[i].add("$")
        else:
            if("$" in temp[i]):
                temp[i].remove("$")
        text = text + str(temp[i])[1:-1].replace(", ","|")+"\n"
        text = text.replace("'","")
    return text.strip()

def unit_production(text):
    unit = {}
    text = empty_productions(text)
    print(text,"\n")
    text = text.split("\n")
    for i in text:
        unit[i.split("->")[0]] = i.split("->")[1].split("|")
    for i in range(len(text)-1,-1,-1):
        lx = unit[text[i][0]]
        for j in unit[text[i][0]]:
            if(j.isupper() and len(j)==1 and j == text[i][0]):
                lx.remove(j)
            elif(len(j)==1 and j.isupper() and j in unit.keys()):
                lx.append(str(unit[j])[1:-1].replace(", ","|").replace("'",""))
                lx.remove(j)
        unit[text[i][0]] = lx
    text = ""
    for i in unit.keys():
        text = text + i + "->"
        text = text + str(unit[i])[1:-1].replace(", ", "|") + "\n"
        text = text.replace("'", "")
    return text.strip()

def generating(text):
    variable = {}
    non_gen = set()
    text = unit_production(text)
    print(text,"\n")
    text = text.split("\n")
    for i in text:
        variable[i.split("->")[0]] = i.split("->")[1]
    temp = variable.copy()
    for i in variable.keys():
        upper = []
        for j in variable[i]:
            if(j.isupper() and j==i):
                upper.append(j)
                if(j not in variable.keys()):
                    non_gen.add(j)
        if(len(upper)==variable[i].count("|")+1 and i in upper and i!=text[0][0]):
            non_gen.add(i)
            del temp[i]
    variable = temp.copy()
    for i in variable.keys():
        counter = 0
        while counter != len(temp[i]):
            if(counter==len(temp[i])):
                break
            if(temp[i][counter] in non_gen):
                x = temp[i][0:counter]
                y = temp[i][counter+1:]
                if(x.rfind("|")==-1 and y.find("|")!=-1):
                    temp[i] = y[y.find("|")+1:]
                    counter = 0
                elif(x.rfind("|")!=-1 and y.find("|")==-1):
                    temp[i] = x[0:x.rfind("|")]
                    counter = 0
                elif(x.rfind("|")!=-1 and y.find("|")!=-1):
                    temp[i] = x[0:x.rfind("|")] + y[y.find("|"):]
                    counter = 0
                elif(x.rfind("|")==-1 and y.find("|")==-1):
                    del temp[i]
                    break
            counter = counter + 1
    variable = temp
    text = ""
    for i in variable.keys():
        text = text + i + "->" + variable[i]+"\n"
    return text.strip()

def reachable(text):
    reach = {}
    text = generating(text)
    print(text,"\n")
    text = text.split("\n")
    reachable = [text[0][0]]
    for i in text:
        reach[i.split("->")[0]] = i.split("->")[1]
    for i in reachable:
        for j in reach[i]:
            if(j.isupper() and j in reach.keys() and j not in reachable):
                reachable.append(j)
    temp = reach.copy()
    for i in reach.keys():
        if(i not in reachable):
            del temp[i]
    reach = temp.copy()
    text = ""
    for i in reach.keys():
        text = text + i + "->" + reach[i] + "\n"
    return text.strip()


# def cnf(text):
#     text = "X->"+text[0]+"\n"+text
#     text = reachable(text)

def get_new_variable(variables):
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if letter not in variables:
            return letter
    raise ValueError("No more available variable names")

def cnf(text):
    rules = {}
    variables = set()
    new_rules = {}
    new_char = {}
    terminal_to_variable = {}  
    text = reachable(text)
    text = text.split("\n")

    for line in text:
        lhs, rhs = line.split("->")
        variables.add(lhs)
        rules[lhs] = rhs.split("|")
#Creating a new start variable
    start = list(rules.keys())[0]
    rules["S0"] = [start]

    for lhs, rhs_list in list(rules.items()):
        new_rhs_list = []

        for rhs in rhs_list:
            if len(rhs) > 2:
                rem = rhs[1:len(rhs)] #Part to be added in the new terminal
                if [rem] in new_rules.values():
                    val_list = list(new_rules.values())
                    key_list = list(new_rules.keys())

                    pos = val_list.index([rem])

                    new_rhs_list.append(rhs[0] + key_list[pos])
                    rules[lhs] = rhs[0] + key_list[pos]

                else:
                    new_variables = [get_new_variable(variables) for _ in range(len(rhs) - 2)]
                    variables.update(new_variables)
                    new_rhs_list.append(rhs[0] + new_variables[0])
                    rules[new_variables[-1]] = [rem]
                    new_rules[new_variables[-1]] = [rem]
            else:
                new_rhs_list.append(rhs)
        rules[lhs] = new_rhs_list


    for lhs, rhs_list in list(rules.items()):
        new_rhs_list = []
        for rhs in rhs_list:
            if len(rhs) > 1:
                new_variables = []
                for ch in rhs:
                    if not ch.isupper():
                        combination = lhs + ch
                        if combination not in terminal_to_variable:

                            if [ch] in new_char.values():
                                val_list = list(new_char.values())
                                key_list = list(new_char.keys())
                                pos = val_list.index([ch])
                                rules[lhs] = key_list[pos]
                                terminal_to_variable[combination] = key_list[pos]

                            else:
                                new_var = get_new_variable(variables)
                                terminal_to_variable[combination] = new_var
                                variables.add(new_var)
                                rules[new_var] = [ch]
                                new_char[new_var] = [ch]
                        new_variables.append(terminal_to_variable[combination])
                    else:
                        new_variables.append(ch)

                new_rhs_list.append("".join(new_variables))
            else:
                new_rhs_list.append(rhs)
        rules[lhs] = new_rhs_list


    cnf_text = "\n".join([f"{lhs}->{'|'.join(rhs_list)}" for lhs, rhs_list in rules.items()])
    return cnf_text

# Example input
input_text = """S->ABA
A->aA|$
B->bBc|$"""


print("After eliminating epsilons......\n")
print(empty_productions(input_text))
print("After removing unit productions.......\n")
unit_production(input_text)
print("After removing non-generating terminals.......\n")
generating(input_text)
print("##### Chomsky Normal Form #####\n")
cnf_text = cnf(input_text)
print(cnf_text)
