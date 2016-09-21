import math
import random
from numpy import mean

def roll(die, randomize=False,fighting_style=None,crit=False,crit_chance=False):
    die_size = int(die.split("d")[-1])
    value = 0
    if randomize:
        value = random.randint(1, die_size)
    elif fighting_style=="GWF":
        # Reroll on 1 and 2:
        value = (die_size-2)/float(die_size)*mean(range(3,die_size+1)) + 2/float(die_size)*roll(die, randomize)
    else:
        value = (die_size+1)/float(2)
    if crit:
        value += (0.05*roll(die, randomize, gwf))
    if fighting_style=="DUELLING":
        value +=2
    return value

def evaluate(string, randomize=False, fighting_style=None, crit=False,crit_chance=0.05):
    tokens = strip_spaces(string)
    eval_tokens = []
    operators = ["+","-","*","/","(",")","."]
    die = ""
    pos = 0
    while (pos <len(tokens)):
        token = tokens[pos]
        multiplier = ""
        #print pos, token
        if token == "(":
            eval_tokens.append("*(")
        elif token in operators or token.isdigit():
            eval_tokens.append(token)
        elif "d" == token:
            if pos>0 and tokens[pos-1].isdigit():
                multiplier = "*"
            while(tokens[pos] not in operators):
                die += tokens[pos]
                if pos == len(tokens)-1:
                    break
                pos += 1
            if die:
                die_roll = roll(die, randomize, fighting_style, crit, crit_chance)
                eval_tokens.append("%s%s"%(multiplier, die_roll))
                multiplier = ""
            if pos != len(tokens)-1:
                eval_tokens.append(tokens[pos])

            die = ""
        pos += 1
        #print eval_tokens
    eval_str = "".join(map(str,eval_tokens))
    return eval(eval_str)

def strip_spaces(string):
    tokens = []
    for ch in string:
        if ch == " ":
            pass
        tokens.append(ch)
    return "".join(tokens)
