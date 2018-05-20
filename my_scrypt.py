
# https://stackoverflow.com/questions/7083313/python-get-mac-clipboard-contents

"""
my script interpriter

print(instance.help) to get availabe functions

create my_scrypt.runner instance
pass script path to set_path function
set instance.booltesting to false to run actively
instance.run_code 
"""


import time
import os
import sys
import numpy as np
import random
#import my_scrypt_custom_funcs

from pymouse import PyMouse
from pykeyboard import PyKeyboard

from PIL import ImageGrab
import textprocess_lib

funcDict = {}


class runner():

    global function_Dict

    def __init__(self):
        """obtaines commands and creates class variables"""

        #self.custom_funcs = my_scrypt_custom_funcs.functions()
        # funcDict.update(self.custom_funcs.get_added())

        self.currentLine = 0
        self.createdPlaceholders = {}
        self.booltesting = True
        self.path_to_scrypt = ''

    def help(self):
        """Returns commands"""

        string = (
            "base commands:\n\n"
            "   rclick x,y\n"
            "   click x,y\n"
            "   hover x,y\n"
            "   if (bool)(do)(else)\n"
            "   phold val = 4\n"
            "   poshold position 'holds position that can be returned to with goto'\n"
            "   goto position\n"
            "   log('to be logged')\n"
            "   wait seconds\n"
            "   waitfor (bool)(timeout)(do if timeout)\n"
            "   boolean_operation (bool1 and/or bool2) returns bool\n"
            "   movefile (path current) (path new) returns bool\n"
            "   del (path to file) returns bool\n"
            "   look (x,y r,g,b) returns bool, allows for rgb values to be within 10 of given value\n"
            "   path_exists (path) returns bool\n"
            "   exit stuff to log 'ends program'\n"
            "   classify 'not supported yet'\n"
            "   type stuff to type\n"
            "   pressenter\n"
            "   plus (num1, num2 ) returns num\n"
            "   equ (num1, num2) returns bool\n"
            #"\n" + self.custom_funcs.helpp
        )

        return string

    def set_path(self, pathToScrypt):
        """sets path to scrypt"""
        self.path_to_scrypt = pathToScrypt

    def testing(self, state):  # when test boolean is true, all mouse, keyboard and sleep functions are off and all paths of logic are tested
        """change testing boolean"""
        self.booltesting = state

    '''
    '''

    def look_function(self, args):

        img = np.array(ImageGrab.grab().convert('RGB'))
        pix = img[args[0], args[1]]
        boolian = True
        for i in range(3):
            if not (args[i + 2] < pix[i] + 10 and args[i + 2] > pix[i] - 10):
                boolian = False
                break
        return boolian

    '''
    '''

    def run(self, inp):
        """interpriter: takes a single line if code"""

        tp = textprocess_lib

        '''
        '''

        def click_function(inp, click_type):

            inp = inp.split()
            x, y = inp[0].split(',')
            x = float(do(x))
            y = float(do(y))
            mouse = PyMouse()
            screen_size_value = mouse.screen_size()

            if x > screen_size_value[0] or y > screen_size_value[1]:
                raise RuntimeError('__________ERROR: click coordinates to big')

            if click_type not in [1, 2, 3]:
                raise RuntimeError('internal function error: invalid click type')

            if not self.booltesting:

                if click_type == 3:
                    mouse.move(x, y)
                else:
                    mouse.click(x, y, click_type)

                if len(inp) == 2:
                    time.sleep(float(do(inp[1])))

            '''
            '''

        def click(inp):
            click_function(inp, 1)

        def rclick(inp):
            click_function(inp, 2)

        def hover(inp):
            click_function(inp, 3)

        def If(inp):  # if (bool) (func do) (func else)
            inp = tp.breakOuter(inp)
            if self.booltesting:  # runs all options during test
                _ = [do(inp[x]) for x in range(3)]
            else:
                if do(inp[0]):
                    do(inp[1])
                else:
                    do(inp[2])

        def phold(inp):  # "phold one = 1"  will instantaite or mutate
            inp = inp.split()
            for i in inp[3:]:
                inp[2] += i + ' '

            if inp[1] != '=':
                raise RuntimeError("no = at pos 2")
            if inp[0] in self.createdPlaceholders:
                self.createdPlaceholders[inp[0]] = do(inp[2])
            else:
                self.createdPlaceholders.update({inp[0]: do(inp[2])})

        def log(inp):  # l(message to be logged)

            inp = tp.breakOuter(inp)
            inp = tp.splitExcludingBrackets(inp)
            out = ''
            for i in inp:
                done = do(i)
                if isinstance(done, bool):
                    '''
                    if done:
                        out += 'True '
                    else:
                       out += 'False '
                    '''
                    pass
                else:
                    out += str(done) + ' '
            print('log:    ' + str(out))

        def goto(inp):  # will not execute during test to prevent forever loop due to all paths of logic being followed

            if not self.booltesting:
                try:
                    self.currentLine = self.createdPlaceholders[inp]
                except Exception as e:
                    raise RuntimeError(inp + " not in createdPlaceholders")

        def poshold(inp):  # placeholder z

            if inp not in self.createdPlaceholders:
                self.createdPlaceholders.update({inp: self.currentLine})

        def waitfor(inp):  # waitfor (bool)(timeout)(timeout func) will wait for bool true untill timeout if timoe out will execute func

            inp = tp.breakOuter(inp)
            if self.booltesting:
                _ = [do(inp[x]) for x in range(3)]
            else:
                timeout = time.time() + float(do(inp[1]))
                while True:
                    if time.time() > timeout:
                        do(inp[2])
                        break
                    if do(inp[0]):
                        break

        def wait(inp):

            inp = inp.strip()
            if not inp.isdigit() and not ''.join(inp.split('.')).isdigit():
                raise RuntimeError("_________ERROR: value is not a number ")

            if not self.booltesting:
                time.sleep(float(do(inp)))

        def boolean_operation(inp):  # boolean_operation (bool and/or bool)

            inp = tp.breakOuter(inp)[0]
            inp = tp.splitExcludingBrackets(inp)
            if len(inp) == 1:
                if inp[0] == "True":
                    return True
                if inp[0] == "False":
                    return False
            if len(inp) > 3:
                raise RuntimeError('to many booleans in b')
            if inp[1] == 'and':
                return do(inp[0]) and do(inp[2])
            elif inp[1] == 'or':
                return do(inp[0]) or do(inp[2])
            else:
                raise RuntimeError("invalid boolean operander")

        def movefile(inp):  # movefile(path1) (path2), movefile(path placehold)(path2) returns bool

            if self.booltesting:
                return False

            inp = tp.breakOuter(inp)
            p1 = tp.splitExcludingBrackets(inp[0])[0]
            p2 = tp.splitExcludingBrackets(inp[1])[0]
            pp1 = ''
            pp2 = ''
            for i in p1.split():
                pp1 += do(i)
            for i in p2.split():
                pp2 += do(i)
            try:
                os.rename(pp1, pp2)
                return True
            except:
                return False

        def delete(inp):  # delete(path) returns bool

            if self.booltesting:
                return False

            inp = tp.breakOuter(inp)
            inp = tp.splitExcludingBrackets(inp)
            p = ''
            for i in inp:
                p += do(i)
            try:
                os.remove(p)
            except:
                try:
                    os.rmdir(p)
                except:
                    return False
            return True

        def look(inp):  # look (x,y r,g,b x,y r,g,b) returns bool
            inp = tp.breakOuter(inp)[0]
            inp = inp.split()

            boo = True
            for i in range(int(len(inp) / 2)):
                xy = inp[i * 2]
                rgb = inp[i * 2 + 1]
                x, y = xy.split(',')
                r, g, b = rgb.split(',')
                args = [int(do(j)) for j in [y, x, r, g, b]]
                boo = boo and self.look_function(args)

            return boo

        def function(inp):  # func (func name)(args)

            inp = tp.breakOuter(inp)
            inp[1] = inp[1].split()
            args = []
            for i in inp[1]:
                args.append(do(i))

            return self.createdPlaceholders[inp[0]](args)

        def plus(inp):
            inp = tp.breakOuter(inp)[0]
            inp = inp.split(',')
            return str(int(do(inp[0])) + int(do(inp[1])))

        def equal(inp):
            inp = tp.breakOuter(inp)[0]
            inp = inp.split(',')
            try:
                return (int(do(inp[0])) == int(do(inp[1])))
            except Exception as e:
                print(e)
                print('Error checking equals at line ' + str(self.currentLine) + " " + inp)
                return False

        def path_exists(inp):  # exists(path var)
            inp = tp.breakOuter(inp)[0]
            inp = inp.split()
            p = ''
            for i in inp:
                p += do(i)
            return os.path.exists(p)

        def search(inp):
            keyboard = PyKeyboard()
            if self.booltesting:
                _ = ' '.join([do(x) for x in tp.splitExcludingBrackets(inp)])
                return

            for i in range(40):
                keyboard.tap_key('delete')
            time.sleep(0.5)

            keyboard.type_string(' '.join([do(x) for x in tp.splitExcludingBrackets(inp)]))
            keyboard.tap_key('return')

        def typeEnter(inp):
            keyboard = PyKeyboard()
            keyboard.tap_key('return')

        def type_space(inp):
            keyboard = PyKeyboard()
            keyboard.tap_key('space')

        def exitt(inp):  # exit
            if not self.booltesting:
                print(inp)
                exit()

        def classify(inp):
            raiseRuntimeError("classify not yet suppored")
            inp = tp.breakOuter(inp)
            inp = inp[0].split()
            clasFunc = {'phone': cla.phone}
            return clasFunc[do(inp[0])](do(inp[1]))

        def typee(inp):
            keyboard = PyKeyboard()
            if self.booltesting:
                _ = ' '.join([do(x) for x in tp.splitExcludingBrackets(inp)])
                return

            keyboard.type_string(' '.join([do(x) for x in tp.splitExcludingBrackets(inp)]))

        def desktop_by_number(inp):  # switches desktop on mac
            inp = tp.breakOuter()
            if self.booltesting:
                if not inp.isdigit() or len(inp) != 1:
                    raise RuntimeError("invald direction")
            kb = PyKeyboard()
            kb.press_key('control')
            kb.tap_key(inp)
            kb.release_key('control')

        funcDict.update({
            'rclick': rclick,
            'click': click,
            'hover': hover,
            'if': If,
            'phold': phold,
            'log': log,
            'goto': goto,
            'poshold': poshold,
            'waitfor': waitfor,
            'wait': wait,
            'boolean_operation': boolean_operation,
            'movefile': movefile,
            'del': delete,
            'look': look,
            'function': function,
            'path_exists': path_exists,
            'search': search,
            'exit': exitt,
            'classify': classify,
            'type': typee,
            'typeenter': typeEnter,
            'plus': plus,
            'equal': equal,
            'desktop_by_number': desktop_by_number,
            'type_space': type_space
        })

        def do(inp):
            """this function controls input and calles scrypt functions"""

            inp = inp.strip()

            for inp in tp.splitExcludingBrackets(inp, delimiter='|'):
                inp = inp.strip()

                token = tp.getTokenAtPos(inp, 0)

                if token in self.createdPlaceholders:
                    return self.createdPlaceholders[inp]

                if token not in funcDict:
                    if self.first_recursion:  # this checks that atleast the first token is understood
                        print("error token not recognised at line " + str(self.currentLine) + ": " + str(token))
                    out = inp
                    continue

                try:
                    self.first_recursion = False
                    out = funcDict[token](inp[len(token):].strip())

                except Exception as e:
                    print(
                        "error:\n",
                        "" + token + ': ' + inp[len(token):].strip() + "\n"
                        "" + e + "\n"
                        "at line: " + str(self.currentLine))
                    '''
                    print ("error:")
                    print (token + ': ' + inp[len(token):].strip())
                    print (e)
                    print ("at line: " + str(self.currentLine))
                    exit()
                    '''
            return out

        do(inp)

    def run_code(self):
        """iterates through scrypt and runs lines"""

        f = open(self.path_to_scrypt).readlines()
        while True:
            self.first_recursion = True
            if self.currentLine >= len(f):
                break
            if len(f[self.currentLine]) > 2 and '#' not in f[self.currentLine]:
                self.run(f[self.currentLine])
            elif '#' in f[self.currentLine]:
                temp = f[self.currentLine][:f[self.currentLine].index('#')]

                if len(temp) > 2:
                    self.run(temp)

            self.currentLine += 1

        if self.booltesting:
            print("looks like it all checked out...")
