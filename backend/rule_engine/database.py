from sqlalchemy.orm import Session
from rule_engine.models import Rule

def get_rule(db: Session, rule_id: int):
    return db.query(Rule).filter(Rule.id == rule_id).first()

def create_rule(db: Session, rule_name: str, ast_json: str):
    db_rule = Rule(name=rule_name, ast_json=ast_json)
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule
