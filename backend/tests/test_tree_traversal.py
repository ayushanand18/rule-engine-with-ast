"""
Unit tests for the rule engine AST evaluation and condition handling.
"""

import unittest
from rule_engine.ast_utils import Node, AST, Condition, ANDOperator, OROperator

class TestRuleEngine(unittest.TestCase):
    """
    Unit tests for the Rule Engine's AST and condition evaluation.
    """

    def test_condition_evaluate(self):
        """
        Test the evaluation of conditions.
        """
        condition_gt = Condition("age", 30, 'gt')
        self.assertTrue(condition_gt.evaluate(35))
        self.assertFalse(condition_gt.evaluate(25))

        condition_eq = Condition("department", "Sales", 'eq')
        self.assertTrue(condition_eq.evaluate("Sales"))
        self.assertFalse(condition_eq.evaluate("Marketing"))

    def test_and_operator(self):
        """
        Test the AND operator evaluation.
        """
        left_condition = Condition("age", 30, 'gt')
        right_condition = Condition("salary", 50000, 'gt')

        left_node = Node("operand", value=left_condition)
        right_node = Node("operand", value=right_condition)

        and_operator = ANDOperator()
        and_node = Node("operator", left=left_node, right=right_node)
        and_node.value = and_operator

        self.assertTrue(and_node.value.evaluate(left_node, right_node))

        right_condition = Condition("salary", 40000, 'gt')
        right_node = Node("operand", value=right_condition)

        self.assertFalse(and_node.value.evaluate(left_node, right_node))

    def test_or_operator(self):
        """
        Test the OR operator evaluation.
        """
        left_condition = Condition("age", 30, 'gt')
        right_condition = Condition("salary", 50000, 'gt')

        left_node = Node("operand", value=left_condition)
        right_node = Node("operand", value=right_condition)

        or_operator = OROperator()
        or_node = Node("operator", left=left_node, right=right_node)
        or_node.value = or_operator

        self.assertTrue(or_node.value.evaluate(left_node, right_node))

        left_condition = Condition("age", 25, 'gt')
        left_node = Node("operand", value=left_condition)

        self.assertTrue(or_node.value.evaluate(left_node, right_node))

    def test_ast_evaluate_rule(self):
        """
        Test the AST evaluation with a complex rule.
        """
        # Sample rule: (age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing') AND (salary > 50000 OR experience > 5)
        age_condition = Condition("age", 30, 'gt')
        department_condition = Condition("department", "Sales", 'eq')
        left_and_node = Node("operator", left=Node("operand", value=age_condition), right=Node("operand", value=department_condition))
        left_and_node.value = ANDOperator()

        age_condition = Condition("age", 25, 'lt')
        department_condition = Condition("department", "Marketing", 'eq')
        right_and_node = Node("operator", left=Node("operand", value=age_condition), right=Node("operand", value=department_condition))
        right_and_node.value = ANDOperator()

        or_node = Node("operator", left=left_and_node, right=right_and_node)
        or_node.value = OROperator()

        salary_condition = Condition("salary", 50000, 'gt')
        experience_condition = Condition("experience", 5, 'gt')
        and_node = Node("operator", left=Node("operand", value=salary_condition), right=Node("operand", value=experience_condition))
        and_node.value = ANDOperator()

        root = Node("operator", left=or_node, right=and_node)
        root.value = ANDOperator()

        ast = AST(root)

        json_data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
        self.assertTrue(ast.evaluate_rule(json_data))

        json_data = {"age": 22, "department": "Marketing", "salary": 45000, "experience": 6}
        self.assertTrue(ast.evaluate_rule(json_data))

        json_data = {"age": 40, "department": "HR", "salary": 40000, "experience": 4}
        self.assertFalse(ast.evaluate_rule(json_data))

if __name__ == '__main__':
    unittest.main()
