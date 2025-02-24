from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, LONGBLOB, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from typing import List, Optional, Dict
import os


load_dotenv()


SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# rule 表
class Rule(Base):
    __tablename__ = 'rules'

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(String, unique=True)
    file_name = Column(String)
    content = Column(Text)

# user 表
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    userid = Column(String, unique=True, index=True)
    password = Column(String)
    level = Column(Integer, default=1)
    realname = Column(String)
    phone_num = Column(String, default="")
    note = Column(Text, default="暂无")
    state = Column(Integer, default=1)
    profile_photo = Column(LONGBLOB, default=None)
    score = Column(Integer, default=0)

#3d_print表
class ThreeDPrint(Base):
    __tablename__ = '3d_print'

    id = Column(Integer, primary_key=True)
    apply_id = Column(String, unique=True)
    userid = Column(String)
    phone_num = Column(String)
    score = Column(Integer)
    score_change = Column(Integer)
    name = Column(String)
    quantity = Column(Float)
    printer = Column(Integer)
    file_zip = Column(LONGBLOB)
    created_at = Column(String)
    updated_at = Column(String)
    state = Column(Integer, default=0)
    reason = Column(Text)


Base.metadata.create_all(bind=engine)

# rule表的CRUD操作
# 插入数据
def create_rule(
        db: Session,
        file_id: str,
        file_name: str,
        content: str
) -> Rule:
    """
    创建新规则
    """
    db_rule = Rule(
        file_id=file_id,
        file_name=file_name,
        content=content
    )
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule
# 删除数据
def delete_rule(db: Session, file_id: str) -> bool:
    """
    删除规则
    """
    db_rule = db.query(Rule).filter(Rule.file_id == file_id).first()
    if not db_rule:
        return False

    # 删除
    db.delete(db_rule)
    db.commit()
    return True
# 查询数据
def get_rules(
        db: Session,
        skip: int = 0,
        limit: int = 10
) -> List[Rule]:
    """
    获取规则列表，支持分页
    """
    return db.query(Rule).offset(skip).limit(limit).all()
# 更改数据
def update_rule(
        db: Session,
        file_id: str,
        update_data: Dict[str, Optional[str]]
) -> Optional[Rule]:
    """
    更新规则字段
    """
    db_rule = db.query(Rule).filter(Rule.file_id == file_id).first()
    if not db_rule:
        return None

    # 更新字段
    for key, value in update_data.items():
        if hasattr(db_rule, key) and value is not None:
            setattr(db_rule, key, value)

    # 提交规则
    db.commit()
    db.refresh(db_rule)
    return db_rule

#user表的CRUD操作
# 插入数据
def create_user(
        db: Session,
        userid: str,
        password: str,
        level: int = 1,
        realname: str = "",
        phone_num: str = "",
        note: str = "暂无",
        state: int = 1,
        profile_photo: Optional[bytes] = None,
        score: int = 0
) -> User:
    """
    创建新用户
    """
    db_user = User(
        userid=userid,
        password=password,
        level=level,
        realname=realname,
        phone_num=phone_num,
        note=note,
        state=state,
        profile_photo=profile_photo,
        score=score
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
# 删除数据
def delete_user(db: Session, userid: str) -> bool:
    """
    删除用户
    """
    db_user = db.query(User).filter(User.userid == userid).first()
    if not db_user:
        return False

    # 删除记录
    db.delete(db_user)
    db.commit()
    return True
# 查询数据
def get_users(
        db: Session,
        skip: int = 0,
        limit: int = 10
) -> List[User]:
    """
    获取用户列表，支持分页
    """
    return db.query(User).offset(skip).limit(limit).all()
# 更新数据
def update_user(
        db: Session,
        userid: str,
        update_data: Dict[str, Optional[str | int | bytes]]
) -> Optional[User]:
    """
    更新用户字段
    """
    db_user = db.query(User).filter(User.userid == userid).first()
    if not db_user:
        return None

    # 更新字段
    for key, value in update_data.items():
        if hasattr(db_user, key) and value is not None:
            setattr(db_user, key, value)

    # 提交
    db.commit()
    db.refresh(db_user)
    return db_user

# 3d_print表的CRUD操作
# 插入数据
def create_3d_print(
        db: Session,
        apply_id: str,
        userid: str,
        phone_num: str,
        score: int,
        score_change: int,
        name: str,
        quantity: float,
        printer: int,
        file_zip: bytes,
        created_at: str,
        updated_at: str,
        state: int = 0,
        reason: str = ""
) -> ThreeDPrint:
    """
    创建 3D 打印申请记录
    """
    db_3d_print = ThreeDPrint(
        apply_id=apply_id,
        userid=userid,
        phone_num=phone_num,
        score=score,
        score_change=score_change,
        name=name,
        quantity=quantity,
        printer=printer,
        file_zip=file_zip,
        created_at=created_at,
        updated_at=updated_at,
        state=state,
        reason=reason
    )
    db.add(db_3d_print)
    db.commit()
    db.refresh(db_3d_print)
    return db_3d_print
# 删除数据
def delete_3d_print(db: Session, apply_id: str) -> bool:
    """
    删除 3D 打印申请记录
    """
    db_3d_print = db.query(ThreeDPrint).filter(ThreeDPrint.apply_id == apply_id).first()
    if not db_3d_print:
        return False

    # 删除记录
    db.delete(db_3d_print)
    db.commit()
    return True
# 查询数据
def get_3d_prints(
        db: Session,
        skip: int = 0,
        limit: int = 10
) -> List[ThreeDPrint]:
    """
    获取 3D 打印申请记录列表，支持分页
    """
    return db.query(ThreeDPrint).offset(skip).limit(limit).all()
# 更新数据
def update_3d_print(
        db: Session,
        apply_id: str,
        update_data: Dict[str, Optional[str | int | float | bytes]]
) -> Optional[ThreeDPrint]:
    """
    更新 3D 打印申请记录字段
    """
    db_3d_print = db.query(ThreeDPrint).filter(ThreeDPrint.apply_id == apply_id).first()
    if not db_3d_print:
        return None

    # 更新字段
    for key, value in update_data.items():
        if hasattr(db_3d_print, key) and value is not None:
            setattr(db_3d_print, key, value)

    # 提交
    db.commit()
    db.refresh(db_3d_print)
    return db_3d_print
