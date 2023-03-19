from typing import Dict, List, Union
from string import ascii_letters


class KnowledgeBase:
    ORDER_OF_PRECEDENCE = {
        '=>': 0,
        '|': 1,
        '&': 2,
        '~': 3,
    }
    LOGICAL_OPERATORS = {'|', '&', '~'}

    @staticmethod
    def _is_name(s: str):
        return s[0] in ascii_letters

    @classmethod
    def _is_complex_sentence(cls, node):
        return isinstance(node, list) and node[0] in cls.LOGICAL_OPERATORS

    @classmethod
    def _is_atomic_sentence(cls, node):
        return not cls._is_complex_sentence(node)

    @classmethod
    def _negate(cls, node, to_negate: bool):
        """Push down negation in a pre-order traversal."""
        if cls._is_atomic_sentence(node):
            return ['~', node] if to_negate else node

        if node[0] == '~':
            to_negate = not to_negate
            node = cls._negate(node[1], to_negate)
        else:
            # node must be a conjunction or disjunction.
            if to_negate:
                node[0] = '&' if node[0] == '|' else '|'
            node[1] = cls._negate(node[1], to_negate)
            node[2] = cls._negate(node[2], to_negate)

        return node

    @classmethod
    def _distribute(cls, node):
        """Distribute | over & in a post-order traversal."""
        if not (isinstance(node, list) and node[0] in '|&'):
            # node is a literal.
            return (node,),

        left_conjunction = cls._distribute(node[1])
        right_conjunction = cls._distribute(node[2])
        return left_conjunction + right_conjunction if node[0] == '&' \
            else tuple(l + r for l in left_conjunction for r in right_conjunction)

    def __init__(self):
        self._clauses = []

    @classmethod
    def _parse(cls, sentence: str):
        """Parse a sentence into an AST using the shunting-yard algorithm.
        Implications are replaced with disjunctions."""
        partial_name = ''
        next_var_id = 0
        var2id: Dict[str, int] = {}
        operand_stack = []
        function_stack: List[Union[str, List[str, int]]] = []
        """Each element is either a string representing an operator, or a list /
        pair of a function's name and its arity."""

        def eval_stack_top():
            """Evaluate the operator at the top of function_stack by creating a
            new AST node for the evaluation result.
            """
            op = function_stack.pop()
            if op == '~':
                operand_stack.append([op, operand_stack.pop()])
            else:
                op_2 = operand_stack.pop()
                op_1 = operand_stack.pop()
                if op == '=>':
                    op = '|'
                    op_1 = ['~', op_1]
                operand_stack.append([op, op_1, op_2])

        i = 0
        while i < len(sentence):
            c = sentence[i]

            if c in ascii_letters:
                partial_name += c
                i += 1
                continue

            # c not being a letter ends a name.
            if partial_name:
                if partial_name[0].islower():
                    # a variable name
                    var_id = var2id.setdefault(partial_name, next_var_id)
                    if var_id == next_var_id:
                        next_var_id += 1
                    operand_stack.append(var_id)
                elif c == '(':
                    # a function name
                    function_stack.append([partial_name, 1])
                else:
                    # a constant
                    operand_stack.append(partial_name)
                partial_name = ''

            if c == ',':
                function_stack[-2][1] += 1
                i += 1
                continue

            if c in '=|&~':
                if c == '=':
                    c = '=>'
                    i += 1

                order = cls.ORDER_OF_PRECEDENCE[c]
                while function_stack and function_stack[-1] != '('\
                        and cls.ORDER_OF_PRECEDENCE[function_stack[-1]] >= order:
                    eval_stack_top()

                function_stack.append(c)
            elif c == '(':
                function_stack.append(c)
            elif c == ')':
                while function_stack[-1] != '(':
                    eval_stack_top()

                function_stack.pop()
                if function_stack and isinstance(function_stack[-1], list)\
                        and cls._is_name(function_stack[-1][0]):
                    name, arity = function_stack.pop()
                    operand = [name]
                    operand.extend(operand_stack[-arity:])
                    del operand_stack[-arity:]
                    operand_stack.append(operand)

            i += 1

        while function_stack:
            eval_stack_top()

        return operand_stack[0]

    def tell(self, sentence: str):
        ast = self._parse(sentence)

        # Convert the AST into a CNF.
        ast = self._negate(ast, False)
        cnf = self._distribute(ast)

        for conjunct in cnf:
            positive_literals = []
            negative_literals = []
            for literal in conjunct:
                if isinstance(literal, list) and literal[0] == '~':
                    negative_literals.append(literal[1])
                else:
                    positive_literals.append(literal)
            self._clauses.append((negative_literals, positive_literals))
