from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from parser import tokenize, Parser, AST, Node  # Assuming your classes are in a file named parser.py

app = FastAPI()

class RuleString(BaseModel):
    rule: str

class RuleList(BaseModel):
    rules: List[str]

class EvaluateRequest(BaseModel):
    ast: Dict
    data: Dict

class ASTNode(BaseModel):
    node_type: str
    left: Dict = None
    right: Dict = None
    value: Dict = None

@app.post("/create_rule", response_model=ASTNode)
def create_rule(rule_string: RuleString):
    tokens = tokenize(rule_string.rule)
    parser = Parser(tokens)
    try:
        root = parser.parse()
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
def evaluate_rule(request: EvaluateRequest):
    ast = AST(root=Node(**request.ast))
    result = ast.evaluate_rule(request.data)
    return {"result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
