def infix_to_postfix(regex):
    precedence = {'*': 3, '|': 2, '.': 1, '(': 0}
    output = ''
    operator_stack = []
    for char in regex:
        if char.isalpha():
            output += char
        elif char == '(':
            operator_stack.append(char)
        elif char == ')':
            while operator_stack and operator_stack[-1] != '(':
                output += operator_stack.pop()
            operator_stack.pop()
        else:
            while operator_stack and precedence[char] <= precedence.get(operator_stack[-1], -1):
                output += operator_stack.pop()
            operator_stack.append(char)
    while operator_stack:
        output += operator_stack.pop()
    return output



def nfa(exp,nfa={},stack = []):
    state = 0
    for i in range(0,len(exp)):
        if(exp[i]=="*"):
            nfa[state] = set()
            nfa[state + 1] = set()
            nfa[state].add(("ϵ", state + 1))
            nfa[state].add(("ϵ", stack[-1][0]))
            nfa[stack[0][-1]].add(("ϵ", stack[-1][0]))
            nfa[stack[0][-1]].add(("ϵ", state + 1))
            stack[0].append(state + 1)
            stack[0].insert(0, state)
            state = state + 2

        elif(exp[i]=="."):
                nfa[stack[-2][-1]].add(("ϵ",stack[-1][0]))
                x = stack[-2]
                y = stack[-1]
                x.extend(y)
                del stack[-2:]
                stack.append(x)
        elif(exp[i]=="|"):
            nfa[state] = set()
            nfa[state+1] = set()
            nfa[state].add(("ϵ", stack[-2][0]))
            nfa[state].add(("ϵ", stack[-1][0]))
            nfa[stack[-2][-1]].add(("ϵ", state+1))
            nfa[stack[-1][-1]].add(("ϵ", state + 1))
            stack[-1].append(state+1)
            stack[-2].insert(0,state)
            x = stack[-2]
            y = stack[-1]
            x.extend(y)
            del stack[-2:]
            stack.append(x)
            state = state + 2
        else:
            nfa[state] = set()
            nfa[state].add((exp[i],state+1))
            nfa[state+1] = set()
            stack.append([state,state+1])
            state = state + 2
    return nfa,stack[0][0],stack[0][-1]

def nfa_to_dfa(regex):
    alphabet = set()
    nfa_dict,start_,finaL_ = nfa(infix_to_postfix(regex))
    start = [set()]
    start[0].add(start_)
    start[0] = set(sorted(start[0]))
    mem = []
    dfa = {}
    mapper = {}
    queue = []
    while len(start) != 0:
        transitions = {}
        state_s = set()
        for i in start[0]:
            queue.append(i)
            while len(queue)!=0:
                x = queue[0]
                del queue[0]
                state_s.add(i)
                for j in nfa_dict[x]:
                    if(j[0]=="ϵ"):
                        state_s.add(j[1])
                        queue.append(j[1])
                    else:
                        alphabet.add(j[0])
                        if(j[0] in transitions.keys()):
                            transitions[j[0]].add(j[1])
                        else:
                            transitions[j[0]] = set()
                            transitions[j[0]].add(j[1])
        dfa[str(start[0])] = transitions
        if(len(state_s)>0):
            mapper[str(start[0])] = set(sorted(state_s))
        for i in transitions.keys():
            if (set(sorted(transitions[i])) in mem):
                continue
            else:
                start.append(set(sorted(transitions[i])))
                mem.append(set(sorted(transitions[i])))
        del start[0]
    start = set()
    start.add(start_)
    start = mapper[str(start)]
    queue = list(mapper.keys())
    mem = list(dfa.values())
    for i in queue:
        dfa[str(mapper[i])] = dfa[i]
        for j in dfa[i].keys():
            dfa[i][j] = mapper[str(dfa[i][j])]
        dfa.pop(i)
    return dfa,sorted(alphabet)
from tabulate import tabulate
def dfa_table(regex):
    dfa_dict,alphabet = nfa_to_dfa(regex)
    alphabet.insert(0,"state")
    table = [alphabet]
    for i in dfa_dict.keys():
        list = []
        list.append(i)
        for j in dfa_dict[i].keys():
            list.insert(table[0].index(j),dfa_dict[i][j])
        table.append(list)
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
dfa_table("(a|b)*")


