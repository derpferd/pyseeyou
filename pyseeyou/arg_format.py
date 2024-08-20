from arg_visitor import ArgNodeVisitor
from pyseeyou import ICUMessageFormat


def get_arg_format(msg):
    ast = ICUMessageFormat.parse(msg)
    args = ArgNodeVisitor()
    a = args.visit(ast)
    print(a)
    return a
