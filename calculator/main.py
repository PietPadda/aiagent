# main.py

import sys
from pkg.calculator import Calculator
from pkg.render import render


def main():
    calculator = Calculator() # create calc object
    if len(sys.argv) <= 1: # some help if you run with args
        print("Calculator App")
        print('Usage: python main.py "<expression>"')
        print('Example: python main.py "3 + 5"')
        return

    expression = " ".join(sys.argv[1:]) # join all args as 1 expression
    try:
        result = calculator.evaluate(expression) # pass args to calculator
        to_print = render(expression, result) # setup calc render of the input args and calc results
        print(to_print) # print it to terminal
    except Exception as e: # error if can't calc
        print(f"Error: {e}")


if __name__ == "__main__":
    main()