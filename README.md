# Application 1 : Rule Engine with AST
> Zeotap | Software Engineer Intern | Assignment | Application 1

## Applicant Introduction
Hi! I am Ayush, prev. JP Morgan Chase, Google Summer of Code. Although all of
this is already written on my GitHub profile, I'd still want to point to my 
[LinkedIn](https://www.linkedin.com/in/theayushanand/).

## Table of Contents
+ [Introduction](#introduction)
+ [Technical Parts](#technical-parts)
  - [Installation](#installation)
  - [How to run](#how-to-run)
+ [About Solution](#about-solution)
  - [Solution Overview](#solution-overview)
  - [Code Structure](#code-structure)
+ [Non Technical Parts](#non-technical-parts)
  - [My Approach](#my-approach)
  - [Feedback](#feedback)
+ [Outro](#outro)

## Introduction
> I read the assginment description a lot of times, so as to make sure I don't 
> miss on anything important. 


Most of the code I have written would seem like a story, so I made sure the README 
doesn't :D. Everything would mostly be in bullets hereafter:
* code is heavily commented and accompany suitable docstrings (React code 
  compatible with Doxygen, and Python code with Sphinx).
* Unittests are written keeping in mind all edge cases that could occur, there are 
  positive as well as negative test cases. Coverage too is kept above 80%.
* This README will talk about the technical parts first, then about the solution.
  And later about all miscellenous things, which are although technical, yet I put
  them in the "non-technical" bracket. They talk more about my thinking and approach
  towards the solution, and a brief discussion on the design is also present.

## Technical Parts
### Installation
I have tried my best to make it platform agnostic, and packaged everything into a 
Docker Container. You can also execute the below seperately for running them on 
your machine without Docker.

+ Frontend
    ```bash
    cd frontend/
    npm install
    ```
+ Backend

    If `poetry` isn't previously installed, install it first. 
    ```bash
    python3 -m venv $VENV_PATH
    $VENV_PATH/bin/pip install -U pip setuptools
    $VENV_PATH/bin/pip install poetry
    ```

    Then continue to create a venv, and install dependencies
    ```bash
    cd backend/
    poetry install
    ```

+ Database

    After a `poetry install`, execute the following to setup raw data in your 
    postgres instance. Make sure to populate the connection creds in the `.env`.
    ```bash
    
    ```

### How to run
Expecting that above installation process, suceeded.

+ Frontend
    ```bash
    npm run dev
    ```
+ Backend
    ```bash
    poetry run python main.py --dev
    ```
+ Database
    ```bash
    
    ```

## About Solution
### Solution Overview
### Code Structure
### Design Discussion
Low-level design of classes:

```java
Class Node:
    Attribute node_type: String  // "operand" or "operator"
    Attribute left: Node
    Attribute right: Node
    Attribute value: Condition or Operator

Class Operator:
    Method evaluate(left: Node, right: Node) -> Boolean

Class ANDOperator inherits Operator:
    Method evaluate(left: Node, right: Node) -> Boolean:
        return left.value.evaluate() AND right.value.evaluate()

Class OROperator inherits Operator:
    Method evaluate(left: Node, right: Node) -> Boolean:
        return left.value.evaluate() OR right.value.evaluate()

Generic Type T
Class Condition<T>:
    Attribute lvariable: String
    Attribute rvalue: T
    Attribute comparison_type: String  // "gt", "lt", "eq", "lteq", "gteq", "neq"

    Method evaluate(input_value: T) -> Boolean:
        If comparison_type == "gt":
            return input_value > rvalue
        If comparison_type == "lt":
            return input_value < rvalue
        If comparison_type == "eq":
            return input_value == rvalue
        If comparison_type == "lteq":
            return input_value <= rvalue
        If comparison_type == "gteq":
            return input_value >= rvalue
        If comparison_type == "neq":
            return input_value != rvalue

Class AST:
    Attribute root: Node

    Method evaluate_rule(json_data: Dictionary) -> Boolean:
        return _evaluate_node(root, json_data)

    Method _evaluate_node(node: Node, data: Dictionary) -> Boolean:
        If node.node_type == "operand":
            return node.value.evaluate(data[node.value.lvariable])
        If node.node_type == "operator":
            return node.value.evaluate(node.left, node.right)

    Method create_rule(rule: String) -> Boolean:
        tokens = tokenize(rule)
        parser = Parser(tokens)
        root = parser.parse()
        return True

    Function combine_rules(rules: List<String>) -> Boolean:
      // Step 1: Parse each rule into its AST form
      Attribute asts: List<Node> = []
      For each rule in rules:
          tokens = tokenize(rule)
          parser = Parser(tokens)
          asts.append(parser.parse())
      
      // Step 2: Determine the most frequent operator
      Attribute operator_count: Dictionary<String, Integer> = {'AND': 0, 'OR': 0}
      For each rule in rules:
          operator_count['AND'] += count_occurrences(rule, 'AND')
          operator_count['OR'] += count_occurrences(rule, 'OR')
      
      Attribute most_frequent_operator: String
      If operator_count['AND'] >= operator_count['OR']:
          most_frequent_operator = 'AND'
      Else:
          most_frequent_operator = 'OR'
      
      Attribute operator_class: Class
      If most_frequent_operator == 'AND':
          operator_class = ANDOperator
      Else:
          operator_class = OROperator
      
      // Step 3: Combine all ASTs using the most frequent operator
      While length(asts) > 1:
          left_ast = asts.pop(0)
          right_ast = asts.pop(0)
          combined_ast = Node(
              node_type="operator",
              left=left_ast,
              right=right_ast,
              value=operator_class()
          )
          asts.append(combined_ast)
      
      root = asts[0]
      Return True

```

Parser and Tokenizer
```java
Function tokenize(rule: String) -> List<String]:
    token_pattern = compile_regex('\s*(=>|<=|>=|&&|\|\||[()=><!]|[\w]+)\s*')
    Return [token for token in find_all(token_pattern, rule) if token.strip()]

Class Parser:
    Attribute tokens: List<String>
    Attribute pos: Integer

    Constructor(tokens: List<String>):
        tokens = tokens
        pos = 0

    Method parse() -> Node:
        If tokens is empty:
            Raise ValueError("Empty tokens list")
        Return parse_expression()

    Method parse_expression() -> Node:
        node = parse_term()
        While pos < length(tokens) AND tokens[pos] in ('AND', 'OR'):
            operator = tokens[pos]
            pos += 1
            right = parse_term()
            If operator == 'AND':
                node = Node("operator", left=node, right=right, value=ANDOperator())
            Else If operator == 'OR':
                node = Node("operator", left=node, right=right, value=OROperator())
        Return node

    Method parse_term() -> Node:
        If tokens[pos] == '(':
            pos += 1
            node = parse_expression()
            pos += 1  // skip ')'
            Return node
        Else:
            Return parse_condition()

    Method parse_condition() -> Node:
        lvariable = tokens[pos]
        pos += 1
        comparison_type = tokens[pos]
        pos += 1
        rvalue = tokens[pos]
        pos += 1
        If is_digit(rvalue):
            rvalue = to_integer(rvalue)
        Else If is_float(rvalue):
            rvalue = to_float(rvalue)
        Else:
            rvalue = strip_quotes(rvalue)
        condition = Condition(lvariable, rvalue, comparison_type)
        Return Node("operand", value=condition)
```

## Non Technical Parts
### My Approach
### Feedback

## Outro

Thanks.
