from typing import Dict, Any, List, Union, Set, Tuple, FrozenSet, cast
from string import ascii_letters
from heapq import heappush, heappop


class KnowledgeBase:
    ORDER_OF_PRECEDENCE = {
        '=>': 0,
        '|': 1,
        '&': 2,
        '~': 3,
    }
    LOGICAL_OPERATORS = {'|', '&', '~'}
    Substitution = Dict[int, Any]
    Variable = int
    FunctionApplication = tuple
    ASTNode = Union[Variable, str, FunctionApplication]
    Clause = Tuple[FrozenSet, FrozenSet]

    @staticmethod
    def _is_name(s: str):
        return s[0] in ascii_letters

    @staticmethod
    def _is_variable_name(node: ASTNode):
        return isinstance(node, str) and node[0].islower()

    @classmethod
    def _is_function(cls, node: ASTNode):
        """Check whether an AST node is a logical operator or a function application."""
        return isinstance(node, cls.FunctionApplication)

    @classmethod
    def _is_variable(cls, node: ASTNode):
        return isinstance(node, cls.Variable)

    @classmethod
    def _is_complex_sentence(cls, node: ASTNode):
        return cls._is_function(node) and node[0] in cls.LOGICAL_OPERATORS

    @classmethod
    def _is_atomic_sentence(cls, node: ASTNode):
        return not cls._is_complex_sentence(node)

    @classmethod
    def _negate(cls, node, to_negate: bool):
        """Push down negation in a pre-order traversal."""
        if cls._is_atomic_sentence(node):
            return ('~', node) if to_negate else node

        if node[0] == '~':
            to_negate = not to_negate
            node = cls._negate(node[1], to_negate)
        else:
            # node must be a conjunction or disjunction.
            op = node[0]
            if to_negate:
                op = '&' if op == '|' else '|'
            node = (op, cls._negate(node[1], to_negate), cls._negate(node[2], to_negate))

        return node

    @classmethod
    def _distribute(cls, node):
        """Distribute | over & in a post-order traversal."""
        if not (cls._is_function(node) and node[0] in '|&'):
            # node is a literal.
            return (node,),

        left_conjunction = cls._distribute(node[1])
        right_conjunction = cls._distribute(node[2])
        return left_conjunction + right_conjunction if node[0] == '&' \
            else tuple(l + r for l in left_conjunction for r in right_conjunction)

    @classmethod
    def _parse(cls, sentence: str):
        """Parse a sentence into an AST using the shunting-yard algorithm.
        Implications are replaced with disjunctions.

        This method assumes that constants and variables only appear inside functions."""
        partial_name = ''
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
                operand_stack.append((op, operand_stack.pop()))
            else:
                op_2 = operand_stack.pop()
                op_1 = operand_stack.pop()
                if op == '=>':
                    op = '|'
                    op_1 = ('~', op_1)
                operand_stack.append((op, op_1, op_2))

        i = 0
        while i < len(sentence):
            c = sentence[i]

            if c in ascii_letters:
                partial_name += c
                i += 1
                continue

            # c not being a letter ends a name.
            if partial_name:
                if c == '(':
                    # a function name
                    function_stack.append([partial_name, 1])
                else:
                    # a constant or a variable name
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
                while function_stack and function_stack[-1] != '(' \
                        and cls.ORDER_OF_PRECEDENCE[function_stack[-1]] >= order:
                    eval_stack_top()

                function_stack.append(c)
            elif c == '(':
                function_stack.append(c)
            elif c == ')':
                while function_stack[-1] != '(':
                    eval_stack_top()

                function_stack.pop()
                if function_stack and isinstance(function_stack[-1], list) \
                        and cls._is_name(function_stack[-1][0]):
                    name, arity = function_stack.pop()
                    arguments = tuple(operand_stack[-arity:])
                    del operand_stack[-arity:]
                    operand_stack.append((name,) + arguments)

            i += 1

        while function_stack:
            eval_stack_top()

        return operand_stack[0]

    @classmethod
    def _substitute(cls, node: ASTNode, sub: Substitution):
        if cls._is_variable(node):
            return sub.get(node, node)
        if cls._is_function(node):
            return (node[0],) + tuple(cls._substitute(arg, sub) for arg in node[1:])
        return node

    @classmethod
    def _occur_check_and_substitute(cls, var: int, node: ASTNode, sub: Substitution):
        """Apply substitution to node and check whether var occurs in the
        substituted node. If not, return the substituted node."""
        subbed_node = cls._substitute(node, sub)
        stack = [subbed_node]
        while stack:
            node = stack.pop()
            if cls._is_function(node):
                stack.extend(node[1:])
            elif cls._is_variable(node) and node == var:
                return None
        return subbed_node

    @classmethod
    def _unify_var(cls, var: int, node: ASTNode, sub: Substitution) -> bool:
        if var in sub:
            return cls._unify(sub[var], node, sub)
        if cls._is_variable_name(node) and node in sub:
            return cls._unify(var, sub[node], sub)

        var_assignment = cls._occur_check_and_substitute(var, node, sub)
        if var_assignment is None:
            return False
        # Variables in sub can be divided into two categories: those that occur
        # in node and those that do not. Now that var -> node passed the occur
        # check, we know that variables occur in node don't contain var, but
        # variables that do not occur in node may contain var. To make sub stay
        # in normal form after adding var -> node, we need another round of
        # substitution.
        for v in sub:
            sub[v] = cls._substitute(sub[v], {var: var_assignment})
        sub[var] = var_assignment
        return True

    @classmethod
    def _unify(cls, node1: ASTNode, node2: ASTNode, sub: Substitution) -> bool:
        """
        :param node1:
        :param node2:
        :param sub: a dict which will contains the substitution on return if
        unification succeeds. The substitution will be in the so-called normal
        form: If a variable is mapped to an expression in the substitution, that
        expression will not contain any variable in the substitution. For
        example, the substitution {0: 1, 1: 2} is not in normal form, but
        {0: 2, 1: 2} is.
        :return:
        """
        if node1 == node2:
            return True
        if cls._is_variable(node1):
            return cls._unify_var(node1, node2, sub)
        if cls._is_variable(node2):
            return cls._unify_var(node2, node1, sub)
        if cls._is_function(node1) and cls._is_function(node2):
            if node1[0] != node2[0] or len(node1) != len(node2):
                return False
            for i in range(1, len(node1)):
                if not cls._unify(node1[i], node2[i], sub):
                    return False
            return True

        return False

    def __init__(self):
        self._next_var_id = 0
        self._clauses: Set[KnowledgeBase.Clause] = set()

    def _standardize_vars_apart_recursive(self, node, var2id: Dict[str, int]):
        if isinstance(node, str):
            if node[0].islower():
                # node is a variable.
                node = var2id.setdefault(node, self._next_var_id)
                if node == self._next_var_id:
                    self._next_var_id += 1
        else:
            node = (node[0],) + tuple(self._standardize_vars_apart_recursive(n, var2id) for n in node[1:])
        return node

    def _standardize_vars_apart(self, nodes: tuple):
        return self._standardize_vars_apart_recursive(('PlaceholderFunction',) + nodes, {})[1:]

    def tell(self, sentence: str):
        ast = self._parse(sentence)

        # Convert the AST into a CNF.
        ast = self._negate(ast, False)
        cnf = self._distribute(ast)

        for conjunct in cnf:
            conjunct = self._standardize_vars_apart(conjunct)

            positive_literals = []
            negative_literals = []
            for literal in conjunct:
                if self._is_function(literal) and literal[0] == '~':
                    negative_literals.append(literal[1])
                else:
                    positive_literals.append(literal)
            self._clauses.add((frozenset(negative_literals), frozenset(positive_literals)))

    @classmethod
    def _substitute_set(cls, atomic_sentence_set: FrozenSet, sub: Substitution):
        return frozenset(cls._substitute(atomic_sentence, sub) for atomic_sentence in atomic_sentence_set)

    @classmethod
    def _binary_resolve(cls, clause1: Clause, clause2: Clause, resolvents: List[Clause]):
        for i in range(2):
            for atomic_sentence1 in clause1[i]:
                for atomic_sentence2 in clause2[1 - i]:
                    sub = {}
                    if cls._unify(atomic_sentence1, atomic_sentence2, sub):
                        resolvent = [None, None]
                        resolvent[i] = cls._substitute_set(clause1[i] - {atomic_sentence1}, sub) \
                                       | cls._substitute_set(clause2[i], sub)
                        resolvent[1 - i] = cls._substitute_set(clause1[1 - i], sub) \
                                           | cls._substitute_set(clause2[1 - i] - {atomic_sentence2}, sub)
                        if not resolvent[0] and not resolvent[1]:
                            return True
                        resolvent = cast(cls.Clause, tuple(resolvent))
                        resolvents.append(resolvent)
        return False

    def ask(self, query: str):
        set_of_support_kb = KnowledgeBase()
        set_of_support_kb.tell(f'~({query})')
        set_of_support_heap = [(len(c[0]) + len(c[1]), c) for c in set_of_support_kb._clauses]
        unit_clauses = set(c for c in self._clauses if len(c[0]) + len(c[1]) == 1)
        usable = self._clauses.copy()
        while set_of_support_heap:
            c = heappop(set_of_support_heap)[1]
            for d in usable:
                resolvents = []
                if self._binary_resolve(c, d, resolvents):
                    return True
                for r in resolvents:
                    if r in usable or r in set_of_support_kb._clauses:
                        continue

                    # Unit forward subsumption: whether the newly derived clause
                    # can be subsumed by existing unit clauses.
                    for u in unit_clauses:
                        for i in range(2):
                            for atomic_sentence1 in u[i]:
                                for atomic_sentence2 in r[i]:
                                    sub = {}
                                    if self._unify(atomic_sentence1, atomic_sentence2, sub) \
                                            and self._substitute(atomic_sentence1, sub) == atomic_sentence2:
                                        break
                                else:
                                    break
                    heappush(set_of_support_heap, (len(r[0]) + len(r[1]), r))
                    set_of_support_kb._clauses.add(r)

            set_of_support_kb._clauses.remove(c)
            if c not in usable:
                usable.add(c)
                if len(c[0]) + len(c[1]) == 1:
                    unit_clauses.add(c)
        return False

    def __len__(self):
        return len(self._clauses)


if __name__ == '__main__':
    kb = KnowledgeBase()
    with open('input.txt', 'r') as f:
        f_iter = iter(f)
        question = next(f_iter).rstrip('\n')
        n_sentences = int(next(f_iter).rstrip('\n'))
        for _ in range(n_sentences):
            kb.tell(next(f_iter).rstrip('\n'))

    with open('output.txt', 'w') as f:
        print('TRUE' if kb.ask(question) else 'FALSE', file=f)
