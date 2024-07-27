from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from rule_engine import models, database
from rule_engine.parser_utils import Parser, tokenize
from rule_engine.ast_utils import Node, AST

app = FastAPI()

class RuleString(BaseModel):
    rule: str
    name: str

class RuleList(BaseModel):
    rules: List[str]

class EvaluateRequest(BaseModel):
    rule_id: int
    data: Dict

class ASTNode(BaseModel):
    node_type: str
    left: Dict = None
    right: Dict = None
    value: Dict = None

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create_rule", response_model=ASTNode)
def create_rule(rule_string: RuleString, db: Session = Depends(get_db)):
    tokens = tokenize(rule_string.rule)
    parser = Parser(tokens)
    try:
        root = parser.parse()
        ast_json = root_to_json(root)
        database.create_rule(db, rule_string.name, ast_json)
        return root
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/combine_rules", response_model=ASTNode)
def combine_rules(rule_list: RuleList):
    combined_root = None
    for rule in rule_list.rules:
        tokens = tokenize(rule)
        parser = Parser(tokens)
        root = parser.parse()
        if combined_root is None:
            combined_root = root
        else:
            combined_root = Node("operator", left=combined_root, right=root, value=ANDOperator())
    return combined_root

@app.post("/evaluate_rule")
def evaluate_rule(request: EvaluateRequest, db: Session = Depends(get_db)):
    db_rule = database.get_rule(db, request.rule_id)
    if db_rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    ast = json_to_ast(db_rule.ast_json)
    result = ast.evaluate_rule(request.data)
    return {"result": result}

def root_to_json(root: Node) -> str:
    if root is None:
        return ""
    return json.dumps(root, default=lambda o: o.__dict__)

def json_to_ast(json_str: str) -> AST:
    data = json.loads(json_str)
    root = dict_to_node(data)
    return AST(root)

def dict_to_node(data: dict) -> Node:
    if data is None:
        return None
    node = Node(node_type=data['node_type'])
    node.left = dict_to_node(data.get('left'))
    node.right = dict_to_node(data.get('right'))
    if data['node_type'] == 'operand':
        node.value = Condition(
            lvariable=data['value']['lvariable'],
            rvalue=data['value']['rvalue'],
            comparison_type=data['value']['comparison_type']
        )
    else:
        operator = data['value']
        if operator == 'ANDOperator':
            node.value = ANDOperator()
        elif operator == 'OROperator':
            node.value = OROperator()
    return node

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
