# calculator.py

class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b, # add
            "-": lambda a, b: a - b, # subtract
            "*": lambda a, b: a * b, # multiply
            "/": lambda a, b: a / b, # divide
        }
        self.precedence = {
            "+": 1, # + gets less precedence
            "-": 1, # - gets less precedence
            "*": 2, # * gets more precedence
            "/": 2, # * gets more precedence
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None # None if no input or just a space
        tokens = expression.strip().split() # strip white space and get list
        return self._evaluate_infix(tokens) # pass list to eval

    def _evaluate_infix(self, tokens):
        values = [] # init empty value list
        operators = [] # init empty operators list

        for token in tokens: # check each token in tokens list
            if token in self.operators: # if a token is an self.operators (+ - * /)
                # stack while loop
                while (
                    operators # is there an operator currently?
                    and operators[-1] in self.operators # check top of stack operator
                    and self.precedence[operators[-1]] >= self.precedence[token] # does top stack op have greater prec than current token
                    # operators operate in correct precedence order
                ):
                    self._apply_operator(operators, values) # includes popping off stack
                operators.append(token) # add new token to operators and repeat
            else: # not an operator?
                try:
                    values.append(float(token)) # add to the values list as a float
                except ValueError:
                    raise ValueError(f"invalid token: {token}") # or error if invalid!

        while operators:
            self._apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("invalid expression")

        return values[0]

    def _apply_operator(self, operators, values):
        if not operators:
            return

        operator = operators.pop()
        if len(values) < 2:
            raise ValueError(f"not enough operands for operator {operator}")

        b = values.pop()
        a = values.pop()
        values.append(self.operators[operator](a, b))