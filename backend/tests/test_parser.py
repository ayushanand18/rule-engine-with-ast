"""
Unit tests for the rule engine parser and AST evaluation.
"""

import unittest
from rule_engine.parser_utils import tokenize, Parser
from rule_engine.ast_utils import Node, AST

class TestParser(unittest.TestCase):
    """
    Unit tests for the Parser and AST functionality.
    """

    def test_tokenizer(self):
        """
        Test the tokenizer function.
        """
        rule = (
            "((age > 30 AND department = 'Sales') OR (age < 25 AND department = "
            "'Marketing')) AND (salary > 50000 OR experience > 5)"
        )
        tokens = tokenize(rule)
        expected_tokens = [
            '(', '(', 'age', '>', '30', 'AND', 'department', '=', "'Sales'", ')',
            'OR', '(', 'age', '<', '25', 'AND', 'department', '=', "'Marketing'",
            ')', ')', 'AND', '(', 'salary', '>', '50000', 'OR', 'experience', '>',
            '5', ')'
        ]
        self.assertEqual(tokens, expected_tokens)

    def test_parser(self):
        """
        Test the parser function.
        """
        rule = (
            "((age > 30 AND department = 'Sales') OR (age < 25 AND department = "
            "'Marketing')) AND (salary > 50000 OR experience > 5)"
        )
        tokens = tokenize(rule)
        parser = Parser(tokens)
        ast = parser.parse()
        self.assertIsInstance(ast, Node)

    def test_ast_create_rule(self):
        """
        Test the AST create_rule and evaluate_rule functions.
        """
        rule = (
            "((age > 30 AND department = 'Sales') OR (age < 25 AND department = "
            "'Marketing')) AND (salary > 50000 OR experience > 5)"
        )
        ast = AST()
        ast.create_rule(rule)

        json_data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
        self.assertTrue(ast.evaluate_rule(json_data))

        json_data = {"age": 22, "department": "Marketing", "salary": 45000, "experience": 6}
        self.assertTrue(ast.evaluate_rule(json_data))

        json_data = {"age": 40, "department": "HR", "salary": 40000, "experience": 4}
        self.assertFalse(ast.evaluate_rule(json_data))

if __name__ == '__main__':
    unittest.main()
