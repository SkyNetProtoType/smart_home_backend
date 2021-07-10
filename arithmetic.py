import re

class BasicMath:
    '''This class allows you to perform basic arithmetic by passing in a
    statement containing an expression

    E.g. what is 2 + 2 would return 4
    '''

    MATH_REGEX = "[0-9]|[+-/*//]"

    def __init__(self):
        self._is_add, self._is_subtract = False, False
        self._is_multiply, self._is_divide = False, False
        self._result = 0

    def solve(self, stmt):
        '''The method solves the expression from a statement by obtaining all the
        operators and numbers and determining which operation to perform'''

        expression = re.findall(self.MATH_REGEX, stmt)
        print(f"Expression: {expression}") # TO BE REMOVED
        self._result = int(expression.pop(0))  # get the first number

        for value in expression:
            if value == "+":
                self._is_add = True
            elif value == "-":
                self._is_subtract = True
            elif value == '*':
                self._is_multiply = True
            elif value == "/":
                self._is_divide = True
            else:
                try:
                    self.__perform_operation(int(value))
                except Exception:
                    return f"I ran into an error trying to solve your question"

        return self._result

    def __perform_operation(self, num):
        '''This method performs the actual operation based on operator before the passed
        value. Once the operation is complete, all operator flags are reset to their
        default state (i.e. set to False)'''

        if self._is_add:
            self._result += num
        elif self._is_subtract:
            self._result -= num
        elif self._is_multiply:
            self._result *= num
        else:
            self._result /= num
        
        self.__reset_operator_flags()

    def __reset_operator_flags(self):
        '''Resets all the operator flags to be False'''
        
        self._is_add, self._is_subtract = False, False
        self._is_multiply, self._is_divide = False, False


if __name__ == "__main__":
    b_math = BasicMath()
    expr1 = b_math.solve("what is 2 + 2")
    expr2 = b_math.solve("what is the result of 3 + 5 - 8 + 1")
    expr3 = b_math.solve("Result of 8 - 5")
    expr4 = b_math.solve("What is 4 / 2")
    expr5 = b_math.solve("Result of 4 * 5")
    
    assert expr1 == 4
    assert expr2 == 1 
    assert expr3 == 3 
    assert expr4 == 2
    assert expr5 == 20 

    print("All test passed!")
    # print(f"Result of 'what is 2+2' is {sum}")