from itertools import product

import pytest

from arg_format import get_arg_format

arg_names = ('arg1', 'a', '你好')
types = ('price', 'number', 'date')
styles = ('integer', 'simple')


@pytest.mark.parametrize('arg_name', arg_names)
def test_simple(arg_name):
    assert get_arg_format(f'This is a test {{{arg_name}}}.') == [{'key': arg_name}]
    # print(get_arg_format('This is a test {arg1} {arg2, select, one {test1} two {test2}}'))


@pytest.mark.parametrize('arg_name,type_name', product(arg_names, types))
def test_simple_with_type(arg_name, type_name):
    assert get_arg_format('This is a test {arg1, price}.') == [{'key': 'arg1', 'type': 'price'}]


@pytest.mark.parametrize(('arg_name'), arg_names)
def test_simple_with_type_and_style():
    assert get_arg_format('This is a test {arg1, number, integer}.') == [{'key': 'arg1', 'type': 'number', 'style': 'integer'}]
