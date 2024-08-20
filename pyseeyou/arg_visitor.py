from __future__ import unicode_literals

from builtins import str
from decimal import Decimal
from parsimonious.nodes import NodeVisitor
from toolz import merge


class ArgNodeVisitor(NodeVisitor):
    def __init__(self):
        self.args = []

    #     '''
    #     ICUNodeVisitor is a walker for the generated parse tree from
    #     pyseeyou.grammar.ICUMessageFormat.
    #
    #     Calling visit() on an instance of the ICUNodeVisitor will traverse the
    #     tree, returning a fully formed string, using the self.options dict as
    #     the values to replace any IDs that were parsed using the grammar.
    #
    #     :param options: Values used to replace parsed IDs with.
    #     :param lang: Language used to derive pluralisation phrase of number
    #     '''
    #     self.options = options
    #     self.lang = lang

    def generic_visit(self, node, visited_children):
        '''
        Each of the methods below beginning with visit_ are called when
        visiting a node of that type. These methods deal with how to parse and
        process the data that has reached that node.

        This generic_visit method deals with visiting nodes that have no
        specific type.
        '''
        #return visited_children or node
        if visited_children:
            return merge(self._filter_none(visited_children)) #[child for child in visited_children if child]
        return None
        #
        # if len(visited_children) > 1:
        #     return merge(visited_children)
        #
        # elif len(visited_children) == 1:
        #     return visited_children[0]

    def visit_message_format_pattern(self, node, visited_children):
        args = []

        for item in visited_children:
            if not item:
                continue
            if 'args' in item:
                args += item['args']

        return args

    def visit_message_format_element(self, node, visited_children):
        #visited_children = self._filter_none(visited_children)

        #return visited_children
        if visited_children:
            this_arg = {}
            new_args = []
            for child in visited_children:
                if child and isinstance(child, dict):
                    if 'args' in child:
                        new_args += child['args']
                    elif 'key' in child:
                        this_arg['key'] = child['key']
                    elif 'type' in child:
                        if 'key' in child['type']:
                            this_arg['type'] = child['type']['key']
                        if 'style' in child['type']:
                            this_arg['style'] = child['type']['style']
            if this_arg:
                new_args.append(this_arg)
            return {'args': new_args}
        return {'args': []}
        # key = visited_children[0].get('key')
        #
        # if len(visited_children) == 1:
        #     return {key: None}
        # else:
        #     values = visited_children[1]
        #     return {key: values}

    def visit_element_format(self, node, visited_children):
        return {'type': visited_children[0]}

    def visit_select_format_pattern(self, node, visited_children):
        other_args = []
        select = {}
        for child in visited_children:
            if 'key' in child:
                select['arg_name'] = child['key']
            if 'select_form' in child:
                select['clauses'] = child['select_form']
            if 'args' in child:
                other_args += child['args']
        return [select] + other_args

    def visit_select_form(self, node, visited_children):
        select_form = {}
        other_args = []
        for child in visited_children:
            if 'key' in child:
                select_form['key'] = child['key']
            if 'args' in child:
                other_args += child['args']
        return {'select_form': select_form, 'args': other_args}

    def visit_plural_format_pattern(self, node, visited_children):
        visited_children = self._filter_none(visited_children)
        return merge(visited_children)

    def visit_plural_form(self, node, visited_children):
        return self._get_key_value(visited_children)

    def visit_plural_key(self, node, visited_children):
        if isinstance(visited_children[0], str):
            return {'key': visited_children[0]}

        return visited_children[0]

    def visit_arg_style_pattern(self, node, visited_children):
        key = self._filter_none(visited_children)[0]['key']
        return {'style': key}

    def visit_offset(self, node, visited_children):
        for child in visited_children:
            if isinstance(child, int):
                return {'offset': child}

    def visit_octothorpe(self, node, visited_children):
        return None

    def visit_string(self, node, visited_children):
        return None

    def visit_id(self, node, visited_children):
        return {'key': str(node.text)}

    def visit_replace_type(self, node, visited_children):
        return {'replace_type': str(node.text)}

    def visit_decimal(self, node, visited_children):
        return None
        # return str(node.text)

    def visit_digits(self, node, visited_children):
        return None
        # return int(node.text)

    def visit__(self, node, visited_children):
        pass

    def _get_formed_string(self, item, key):
        self.args[key] = item
        # # Direct replacement, {} style
        # if not item[key]:
        #     return self.options[key]
        #
        # replace_type = item[key]['replace_type']
        # if replace_type.lower() == 'select':
        #     self.args[key] = ('select', item)
        #     # return self._select_replace(item[key], key)
        #
        # elif replace_type.lower() == 'plural':
        #     self.args[key] = ('plural', item)
        #     # return self._plural_replace(item[key], key)

    # def _select_replace(self, item, key):
    #     self.args[key] = item
    #     # if key in self.options:
    #     #     self.args[key] = item
    #     #     # return item[self.options[key]]
    #     #
    #     # else:
    #     #     return item['other']
    #
    # def _plural_replace(self, item, key):
    #     str_key = str(self.options[key])
    #
    #     if 'offset' in item:
    #         dec_str_key = Decimal(str_key)
    #         dec_str_key -= item['offset']
    #
    #         if dec_str_key < 0:
    #             str_key = '0'
    #         else:
    #             str_key = str(dec_str_key)
    #
    #     if str_key in item:
    #         return item[str_key]
    #
    #     else:
    #         # plural_key = get_cardinal_category(str_key, self.lang)
    #
    #         text = item[plural_key] if plural_key in item else item['other'] # fall back to 'other' for optional keys where other and many are the same
    #
    #         if '#' in text:
    #             return text.replace(
    #                 '#', str(str_key))
    #
    #         else:
    #             return text
    #
    def _get_key_value(self, items):
        key, value = None, None
        for item in items:
            if not item:
                continue

            elif isinstance(item, str):
                value = item

            elif isinstance(item, dict):
                key = item['key']

        return {key: value}

    #
    def _filter_none(self, items):
        return [item for item in items if item is not None]
