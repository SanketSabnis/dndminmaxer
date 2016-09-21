import math
import random
import re
from numpy import mean

operators = ["+","-","*","/","(",")","."]
def roll(die, randomize=False,fighting_style=None,crit=False,crit_chance=None):
    die_size = int(die.split("d")[-1])
    value = 0
    if randomize:
        value = random.randint(1, die_size)
    elif fighting_style=="GWF":
        # Reroll on 1 and 2:
        value = (die_size-2)/float(die_size)*mean(range(3,die_size+1)) + 2/float(die_size)*roll(die, randomize)
    else:
        value = (die_size+1)/float(2)
    if crit and crit_chance:
        value += (crit_chance*roll(die, randomize, fighting_style, crit=False))
    if fighting_style=="DUELLING":
        value +=2
    return value

def get_die(pos, tokens):
    die = ""
    multiplier = ""
    if pos>0 and tokens[pos-1].isdigit():
        multiplier = "*"
    while(tokens[pos] not in operators):
        die += tokens[pos]
        if pos == len(tokens)-1:
            break
        pos += 1
    return die, multiplier, pos

def parse_match(m, droplowest=False):
    if len(m.groups()) ==2:
        num_dice = int(m.group(1))
        die = m.group(2)
        if die:
            die_size = int(die.split("d")[-1])
            sum_dies = (die_size +1)*(num_dice/2.0)*pow(die_size, num_dice)
            drop_sum = 0
            for die_face in range(1, die_size+1):
                if droplowest:
                    all_face = pow(die_size+1-die_face, num_dice) - pow(die_size-die_face, num_dice)
                else:
                    all_face = pow(die_face, num_dice) - pow(die_face-1, num_dice)
                drop_sum += die_face*(all_face)
            avgroll = (sum_dies - drop_sum)/float(pow(die_size, num_dice))
    return avgroll

def evaluate(string, randomize=False, fighting_style=None, crit=False,crit_chance=0.05):
    tokens = strip_spaces(string)
    eval_tokens = []
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
            die, multiplier, pos = get_die(pos, tokens)
            if die:
                die_roll = roll(die, randomize, fighting_style, crit, crit_chance)
                eval_tokens.append("%s%s"%(multiplier, die_roll))
            if pos != len(tokens)-1:
                eval_tokens.append(tokens[pos])
        elif "D" == token:
            # Search for highest , highest = drop lowest
            patt = r"Droplowest(\d+)(d\d+)"
            p = re.compile(patt)
            m = re.search(p, tokens[pos:])
            if m and m.groups():
                avgroll = parse_match(m, droplowest=True)
                if avgroll: eval_tokens.append(avgroll)
                pos += len(m.group(0))
            else:
                # Search for lowest , lowest = drop highest
                patt = r"Drophighest(\d+)(d\d+)"
                p = re.compile(patt)
                m = re.search(p, tokens[pos:])
                if m and m.groups():
                    avgroll = parse_match(m, droplowest=False)
                    if avgroll: eval_tokens.append(avgroll)
                    pos += len(m.group(0))
        pos += 1
    eval_str = "".join(map(str,eval_tokens))
    return eval(eval_str)

def strip_spaces(string):
    tokens = []
    for ch in string:
        if ch == " ":
           continue
        tokens.append(ch)
    return "".join(tokens)
