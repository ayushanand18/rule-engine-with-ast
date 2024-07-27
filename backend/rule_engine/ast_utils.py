from typing import List, Literal, TypeVar, Generic
from abc import ABC, abstractmethod

T = TypeVar('T')

class Node:
    def __init__(self, node_type: Literal["operand", "operator"], left: 'Node' = None, right: 'Node' = None, value: 'Condition' = None):
        self.node_type = node_type
        self.left = left
        self.right = right
        self.value = value

class Operator(ABC):
    @abstractmethod
    def evaluate(self, left: Node, right: Node) -> bool:
        pass

class ANDOperator(Operator):
    def evaluate(self, left: Node, right: Node) -> bool:
        return left.value.evaluate() and right.value.evaluate()

class OROperator(Operator):
    def evaluate(self, left: Node, right: Node) -> bool:
        return left.value.evaluate() or right.value.evaluate()

class Condition(Generic[T]):
    def __init__(self, lvariable: str, rvalue: T, comparison_type: Literal['gt', 'lt', 'eq', 'lteq', 'gteq', 'neq']):
        self.lvariable = lvariable
        self.rvalue = rvalue
        self.comparison_type = comparison_type

    def evaluate(self, input_value: T) -> bool:
        if self.comparison_type == 'gt':
            return input_value > self.rvalue
        elif self.comparison_type == 'lt':
            return input_value < self.rvalue
        elif self.comparison_type == 'eq':
            return input_value == self.rvalue
        elif self.comparison_type == 'lteq':
            return input_value <= self.rvalue
        elif self.comparison_type == 'gteq':
            return input_value >= self.rvalue
        elif self.comparison_type == 'neq':
            return input_value != self.rvalue

class AST:
    def __init__(self, root: Node = None):
        self.root = root

    def evaluate_rule(self, json_data: dict) -> bool:
        return self._evaluate_node(self.root, json_data)

    def _evaluate_node(self, node: Node, data: dict) -> bool:
        if node.node_type == "operand":
            return node.value.evaluate(data[node.value.lvariable])
        elif node.node_type == "operator":
            return node.value.evaluate(node.left, node.right)

    def create_rule(self, rule: str) -> bool:
        tokens = tokenize(rule)
        parser = Parser(tokens)
        self.root = parser.parse()
        return True

    def combine_rules(self, rules: List[str]) -> bool:
        # Implementation for combining multiple rules into one AST
        pass
