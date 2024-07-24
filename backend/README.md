# Backend | Rule Engine

Go over to [README](/README.md) for full documentation.

## LL Design
```py
class AST:
    root: Node
    evaluate_rule(json_data: str) -> bool
    create_rule(rule: str) -> bool
    combine_rules(rules: List[str]) -> bool

class Node:
    type: Literal["operand", "operator"]
    left: Node
    right: Node
    value: Condition

class Operator:
    evaluate(Node, Node) -> bool

class ANDOperator(Operator):
    evaluate(Node, Node) -> bool

class OROperator(Operator):
    evaluate(Node, Node) -> bool

Generic<T>
class Condition:
    lvariable: str
    rvalue: T
    comparison_type: Literal['gt', 'lt', 'eq', 'lteq', 'gteq', 'neq']
    evaluate(input_value: T) -> bool
```