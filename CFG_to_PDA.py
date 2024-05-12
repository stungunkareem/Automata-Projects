#Kareem Ayman Rezk_202001618
#Ali Abdelrasheed_202000761
#Aly Tarek_202001384
#Omar Eldeeb_202001456








def skeleton(cfg):
    transitions = []
    transitions.append("(S0,Ɛ,Ɛ)->(S1,$)")
    transitions.append("(S1,Ɛ,Ɛ)->(S2,"+cfg[0]+")")
    transitions.append("(S2,Ɛ,$)->(S3,Ɛ)")
    saved = []
    for i in cfg:
        if(i.islower()==True and i not in saved):
            saved.append(i)
            transitions.append("(S2,"+i+","+i+")->(S2,Ɛ)")
    return transitions

# print(skeleton("S->A\nA->aA|bA|Ɛ"))



def productions(cfg):
    counter = 4
    map = {}
    transitions = skeleton(cfg)
    cfg = cfg.split("\n")
    for i in cfg:
        map[i.split("->")[0]] = ''.join(reversed(i.split("->")[1])).split("|")
    for i in map.keys():
        transitions.append("(S2,Ɛ,"+i+")->(S"+str(counter)+",Ɛ)")
        x = counter
        for j in map[i]:
            for m in range(len(j)):
                if(j[m]=="Ɛ"):
                    transitions.append("(S"+str(x)+",Ɛ,Ɛ)->(S2,Ɛ)")
                    counter = counter + 1
                elif (m == len(j)-1):
                    transitions.append("(S" + str(counter) + ",Ɛ,Ɛ)->(S2,"+j[m]+")")
                    counter = counter + 1
                else:
                    if (m == 0 and m+1 != len(j)-1):
                        transitions.append("(S" + str(x) + ",Ɛ,Ɛ)->(S" + str(counter) + "," + j[m] + ")")
                        counter = counter + 1
                    elif(m == 0 and m+1 == len(j)-1):
                        transitions.append("(S" + str(x) + ",Ɛ,Ɛ)->(S" + str(counter) + "," + j[m] + ")")
                    elif(m != 0 and m+1 == len(j)-1):
                        transitions.append("(S" + str(counter-1) + ",Ɛ,Ɛ)->(S" + str(counter) + "," + j[m] + ")")
                    else:
                        transitions.append("(S" + str(counter-1) + ",Ɛ,Ɛ)->(S" + str(counter) + "," + j[m] + ")")
                        counter = counter + 1
    return transitions






def cfg_to_pda(cfg):
    pda = productions(cfg)
    pda = '\n'.join(pda)
    return pda



    #     x = counter
    #     transitions[("S2", "Ɛ", i.split("->")[0])] = ("S"+str(x), "Ɛ")
    #     variable = i.split("->")[0]
    #     productions = i.split("->")[1].split("|")
    #     productions = ''.join(reversed(productions))
    #     counter = counter + 1
    #     for j in productions.split("|"):
    #         for m in range(0,len(j)):
    #             if(m=="Ɛ"):
    #                 transitions[("S" + str(x), "Ɛ", "Ɛ")] = ("S2","Ɛ")
    #                 continue
    #             if(m==len(j)-1):
    #                 transitions[("S" + str(counter), "Ɛ", "Ɛ")] = ("S2",j[m])
    #                 continue
    #             transitions[("S"+str(x), "Ɛ", "Ɛ")] = ("S" + str(counter+1), j[m])
    #             counter = counter + 1
    # for i in transitions.keys():
    #     print(str(i)+"->"+str(transitions[i]))


print(cfg_to_pda("S->A\nA->aA|bA|Ɛ"))
print("\n\n")
print(cfg_to_pda("S->aTb|b\nT->Tb|Ɛ"))




