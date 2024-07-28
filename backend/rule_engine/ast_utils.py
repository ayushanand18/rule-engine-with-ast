"""
Module for rule engine AST and related classes.

This module defines the classes and methods to create and evaluate
an Abstract Syntax Tree (AST) for rules, as well as to combine
multiple rules into a single AST.
"""

from typing import List, Literal, TypeVar, Generic
from abc import ABC, abstractmethod


T = TypeVar('T')


class Node:
    """
    Class representing a node in the AST.

    Attributes:
        node_type (Literal): The type of the node ("operand" or "operator").
        left (Node): The left child node.
        right (Node): The right child node.
        value (Condition or Operator): The value of the node.
    """

    def __init__(self, node_type: Literal["operand", "operator"],
                 left: 'Node' = None, right: 'Node' = None,
                 value: 'Condition' = None):
        self.node_type = node_type
        self.left = left
        self.right = right
        self.value = value


class Operator(ABC):
    """
    Abstract base class for operators.
    """

    @abstractmethod
    def evaluate(self, left: Node, right: Node) -> bool:
        """
        Evaluate the operator with given left and right nodes.

        Args:
            left (Node): The left child node.
            right (Node): The right child node.

        Returns:
            bool: The result of the evaluation.
        """
        pass


class ANDOperator(Operator):
    """
    Class representing the AND operator.
    """

    def evaluate(self, left: Node, right: Node) -> bool:
        return left.value.evaluate() and right.value.evaluate()


class OROperator(Operator):
    """
    Class representing the OR operator.
    """

    def evaluate(self, left: Node, right: Node) -> bool:
        return left.value.evaluate() or right.value.evaluate()


class Condition(Generic[T]):
    """
    Class representing a condition in the AST.

    Attributes:
        lvariable (str): The left variable of the condition.
        rvalue (T): The right value of the condition.
        comparison_type (Literal): The type of comparison ('gt', 'lt',
                                   'eq', 'lteq', 'gteq', 'neq').
    """

    def __init__(self, lvariable: str, rvalue: T,
                 comparison_type: Literal['gt', 'lt', 'eq',
                                          'lteq', 'gteq', 'neq']):
        self.lvariable = lvariable
        self.rvalue = rvalue
        self.comparison_type = comparison_type

    def evaluate(self, input_value: T) -> bool:
        """
        Evaluate the condition with given input value.

        Args:
            input_value (T): The input value to be compared.

        Returns:
            bool: The result of the evaluation.
        """
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
    """
    Class representing the Abstract Syntax Tree (AST) for rules.

    Attributes:
        root (Node): The root node of the AST.
    """

    def __init__(self, root: Node = None):
        self.root = root

    def evaluate_rule(self, json_data: dict) -> bool:
        """
        Evaluate the rule represented by the AST with given JSON data.

        Args:
            json_data (dict): The data to evaluate the rule against.

        Returns:
            bool: The result of the evaluation.
        """
        return self._evaluate_node(self.root, json_data)

    def _evaluate_node(self, node: Node, data: dict) -> bool:
        """
        Recursively evaluate a node in the AST.

        Args:
            node (Node): The node to evaluate.
            data (dict): The data to evaluate the node against.

        Returns:
            bool: The result of the evaluation.
        """
        if node.node_type == "operand":
            return node.value.evaluate(data[node.value.lvariable])
        elif node.node_type == "operator":
            return node.value.evaluate(node.left, node.right)

    def create_rule(self, rule: str) -> bool:
        """
        Create an AST from a rule string.

        Args:
            rule (str): The rule string.

        Returns:
            bool: True if the rule was created successfully.
        """
        from rule_engine.parser_utils import tokenize, Parser

        tokens = tokenize(rule)
        parser = Parser(tokens)
        self.root = parser.parse()
        return True

    def combine_rules(self, rules: List[str]) -> bool:
        """
        Combine multiple rules into a single AST.

        Args:
            rules (List[str]): The list of rule strings.

        Returns:
            bool: True if the rules were combined successfully.
        """
        from rule_engine.parser_utils import tokenize, Parser
        
        # Parse each rule into its AST form
        asts = []
        for rule in rules:
            tokens = tokenize(rule)
            parser = Parser(tokens)
            asts.append(parser.parse())

        # Determine the most frequent operator to use as the root
        operator_count = {'AND': 0, 'OR': 0}
        for rule in rules:
            operator_count['AND'] += rule.count('AND')
            operator_count['OR'] += rule.count('OR')

        most_frequent_operator = 'AND' if operator_count['AND'] >= \
            operator_count['OR'] else 'OR'
        operator_class = ANDOperator if most_frequent_operator == 'AND' \
            else OROperator

        # Combine all ASTs into one using the most frequent operator
        while len(asts) > 1:
            left_ast = asts.pop(0)
            right_ast = asts.pop(0)
            combined_ast = Node(
                node_type="operator",
                left=left_ast,
                right=right_ast,
                value=operator_class()
            )
            asts.append(combined_ast)

        self.root = asts[0]
        return True
