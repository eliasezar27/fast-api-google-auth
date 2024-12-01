from core.models.database import User, Session
from core.schemas.request_schema import GenericUser

# DAO pattern
class UserDAO:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, _id: int | str):
        if isinstance(_id, str) and not _id.isnumeric():
            _id = int(_id)
        return self.db.query(User).filter(User.id == _id).first()

    def create_user(self, user: GenericUser):
        db_user = User(name=user.name, email=user.email)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user