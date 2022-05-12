from sqlalchemy.orm import Session


def unique(model, db: Session, attr, value) -> bool:
    return db.query(model).filter(getattr(model, attr)==value).first() == None