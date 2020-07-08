from collections import deque


class SmartCalculator:
    def __init__(self):
        self.inp_string = None
        self.vars = dict()
        self.opers = {'stack_end': 5, '+': 1, '-': 1,
                      '*': 2, '/': 2, '^': 3, '(': 4, ')': 4}

    def isnum(self, x):
        try:
            float(x)
            return True
        except:
            return False

    def assign(self, assign_op):
        if ('+' in assign_op or '-' in assign_op) and ('=' not in assign_op):
            full_op = assign_op.split()
            sending_op = []
            try:
                for val in full_op:
                    if val.isalpha():
                        sending_op.append(int(self.vars[val]))
                    else:
                        sending_op.append(val)
            except KeyError:
                pass
            self.expression(' '.join([str(x) for x in sending_op]))
            return

        if '=' in assign_op:
            full_op = assign_op.split('=')
        else:
            full_op = assign_op.split()
        if len(full_op) == 1:
            if not full_op[0].isalpha():
                print('Invalid identifier')
                return
            else:
                try:
                    print(int(self.vars[full_op[0]]))
                except KeyError:
                    print('Unknown variable')

        else:
            try:
                # and not self.isnum(assign_op[assign_op.index('=') - 1])
                if assign_op.count('=') == 1:
                    full_op = assign_op.split('=')
                    for i, val in enumerate(full_op):
                        if ' ' in val:
                            full_op[i] = val.replace(' ', '')
                    if self.isnum(full_op[1]):
                        if not full_op[0].isalpha():
                            print('Invalid identifier')
                            return
                        self.vars[full_op[0]] = float(full_op[1])
                    elif full_op[1] in self.vars.keys():
                        if not full_op[0].isalpha():
                            print('Invalid identifier')
                            return
                        self.vars[full_op[0]] = self.vars[full_op[1]]
                    elif not self.isnum(full_op[1]) and not full_op[0].isalpha():
                        if not full_op[0].isalpha():
                            print('Invalid identifier')
                            return
                        print('Invalid assignment')
                    elif full_op[0].isalpha() and not full_op[1].isalpha():
                        print('Invalid assignment')
                    elif full_op[0].isalpha() and full_op[1].isalpha() and full_op[1] not in self.vars.keys():
                        print('Unknown variable')
                    else:
                        print('Invalid assignment')
                else:
                    print('Invalid assignment')
            except IndexError:
                print('index error')

    def postfix(self, inp):
        result = ''
        stack = deque(['stack_end'])
        for i, val in enumerate(inp):
            if val.isalpha():
                if val in self.vars.keys():
                    result += ' ' + str(int(self.vars[val]))
                else:
                    print('Unknown variable ')
                    return

            elif self.isnum(val):
                result += ' '+str(val)
            elif val in self.opers.keys():
                if stack[(len(stack)-1)] == 'stack_end' or stack[(len(stack)-1)] == '(':
                    stack.append(val)
                elif val == '(':
                    stack.append(val)
                elif val == ')':
                    while stack[(len(stack)-1)] != '(':
                        result += ' ' + str(stack.pop())
                    stack.pop()
                elif self.opers[val] > self.opers[stack[(len(stack)-1)]]:

                    stack.append(val)
                elif self.opers[val] <= self.opers[stack[(len(stack)-1)]]:
                    try:
                        while self.opers[val] <= self.opers[stack[(len(stack)-1)]]:
                            if stack[(len(stack)-1)] == 'stack_end' or stack[(len(stack)-1)] == '(':
                                break
                            result += ' ' + str(stack.pop())
                    except KeyError:
                        print('Unknown variable')
                        return
                    stack.append(val)
        while(stack[(len(stack)-1)] != 'stack_end'):
            result += ' ' + str(stack.pop())
        return result

    def expression(self, expr):
        inp = expr.split()
        x = []
        for i, val in enumerate(inp):
            if val.startswith('('):
                i = 0
                while i < len(val):
                    if val[i] == '(':
                        x.append('(')
                    i += 1
                x.append(val.replace('(', ''))

            elif val.endswith(')'):
                x.append(val.replace(')', ''))
                i = 0
                while i < len(val):
                    if val[i] == ')':
                        x.append(')')
                    i += 1
            else:
                x.append(val)
        for i in range(0, len(x)):

            if x[i].startswith('+'):
                x[i] = '+'
            elif x[i].startswith('-'):
                if x[i].count('-') % 2 == 0:
                    x[i] = '+'
                else:
                    x[i] = '-'
            elif x[i].startswith('*') or x[i].startswith('/'):
                if x[i].count('*') > 1 or x[i].count('/') > 1:
                    print('invalid expression')
                    return
        if x.count('(') != x.count(')'):
            print('invalid expression')
            return
        postfix_expression = self.postfix(x).split(' ')
        print(postfix_expression)
        stack = deque()
        for val in postfix_expression:
            if self.isnum(val):
                stack.append(val)
            if val in self.opers.keys():
                a = stack.pop()
                b = stack.pop()
                if val == '+':
                    res = int(b) + int(a)
                    stack.append(res)
                elif val == '-':
                    res = int(b) - int(a)
                    stack.append(res)
                elif val == '/':
                    res = int(b) / int(a)
                    stack.append(res)
                elif val == '*':
                    res = int(b) * int(a)
                    stack.append(res)
        print(stack.pop())

        # items = expr.split()
        # print(items)
        # outp = float(items[0])
        # for i in range(1, len(items), 2):
        #     symb = items[i]
        #     try:
        #         num = int(items[i + 1])
        #     except:
        #         print('Invalid expression')
        #     if symb.startswith("+"):
        #         outp += num
        #     elif symb.startswith("-"):
        #         if symb.count("-") % 2 == 1:
        #             outp -= num
        #         else:
        #             outp += num
        #     else:
        #         print("Invalid operation")
        # print(int(outp))

    def verify(self, inp_string):
        self.inp_string = inp_string
        if self.inp_string.startswith('/'):
            if self.inp_string == '/exit':
                print('bye')
                return 0
            elif self.inp_string == '/help':
                print(
                    'This program calculates the sum and differences of number sequences.')
            else:
                print('Unknown command')
            return
        else:
            try:
                float(self.inp_string.split()[0])
            except TypeError:
                self.assign(self.inp_string)
            except ValueError:
                self.assign(self.inp_string)
            except IndexError:
                pass
            else:
                self.expression(self.inp_string)
            return

    def main(self):
        while True:
            flag = self.verify(input())
            if flag == 0:
                break


calculator = SmartCalculator()
calculator.main()
