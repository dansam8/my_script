"""for general text prosessing functions"""

'''
replace_sub_by_index        returns string with everything from p1 up to p2 replaced by replacechar
                            ('input',pos1,pos2,replacechar = "")
getTokenAtPos               returns token and position delimited by space or (
                            ('dan sam', 1) > sam
breakOuter
splitByOperander            returns list of str broken by operander including operander:('1','+','1')
                            ('1+1') > ['1','+','1']
splitExcludingBrackets      splits by space what isnt in bracktes
                            1 (1 1) > ['1','(1 1)']
if_in_score                 returns % of one string that is in another string 0-1
                            ('dan#' ,'daniel') > 0.75
exclusion                   removes given chars for comparing
                            ("dan###iel", '#') > daniel
'''


def replace_sub_by_index(string, pos1, pos2, replacechar=""):
    """returns string with everything from p1 up to p2 replaced by replacechar
    ('input',pos1,pos2,replacechar = "")
    """

    if pos1 > pos2 or pos2 > len(string):
        return 0
    add = ""
    for i in range(pos2 - pos1):
        add += replacechar

    return string[0:pos1] + add + string[pos2:]


def getTokenAtPos(inp, pos):
    """returns token and position delimited by space or (
    ('dan sam', 1) > sam
    """

    for i in range(len(inp) - 1):
        if inp[i] != ' ' and inp[i + 1] == '(':
            inp = inp[:i + 1] + ' ' + inp[i + 1:]

    if pos > len(inp.split()) - 1:
        return False
    return inp.split()[pos].strip()


def breakOuter(inp):
    """removes outer moste brackets
    ( '(dansam (sam )) gone' ) > dansam (sam)
    """

    stepin = 0
    arr = []
    last = 0
    for i, ch in enumerate(inp):
        if ch == '(':
            stepin += 1
            if stepin == 1:
                last = i
        elif ch == ')':
            stepin += -1
            if stepin == 0:
                arr.append(inp[last + 1:i])
    return arr


def splitByOperander(inp):
    """returns list of str broken by operander including operander:('1','+','1')
    ('1+1') > ['1','+','1']
    """

    operand = ['+', '-', '*', '/']
    out = ['']
    for i in range(len(inp)):
        if inp[i] in operand:
            out.append(inp[i])
        elif inp[i - 1] in operand:
            out.append(inp[i])
        else:
            out[-1] += inp[i]

    return out


def splitExcludingBrackets(inp, delimiter=' '):
    """splits by space what isnt in bracktes
    1 (1 1) > ['1','(1 1)'] 
    """

    stepin = 0
    arr = ['']
    for i in inp:
        if i == '(':
            stepin += 1
        elif i == ')':
            stepin += -1

        if stepin == 0 and i == delimiter:
            arr.append('')
        else:
            arr[-1] += i
    return arr

# returns a score of how much of S1 is in S2


def string_similarity_score(one, two, exclusionSubs=[]):
    """returns % of one string that is in another string, value from 0 - 1
    ('dan#' ,'daniel') > 0.75
    """

    if len(one) > len(two):
        return 0
    one, two = [exclusion(one, exclusionSubs), exclusion(two, exclusionSubs)]

    score = 0.0
    oldScore = 0
    for i in range(len(one)):
        for j in range(len(one) - i):
            if one[j:i + j + 1] in two and (i + 1.0) / len(one) > score:
                score = (i + 1.0) / len(one)
        if oldScore == score:
            break
        oldScore = score
    return score


def exclusion(string, exclusionSubs):
    """removes given chars for comparing
    ("dan###iel", '#') > daniel

    """

    if len(exclusionSubs) > 0 and exclusionSubs[0] == 'default':
        out = '#$@!%^&*()+=_-.,><?/":;|\[]]\{\}\'\" '
        for i in out:
            string = string.replace(i, '')

    elif len(exclusionSubs) > 0:
        for i in exclusionSubs:
            string = string.replace(i, '')

    return string


'''
print replace_sub_by_index('daneil',0,3,'#')
print getTokenAtPos("daniel sam is",1)
print breakOuter('(dan (sam) is) (ja)')
print splitByOperander('1+1')
print splitExcludingBrackets("(daniel sam) (hello)")
print if_in_score('dan',"danile")
print exclusion('dan###iel','#')
'''
