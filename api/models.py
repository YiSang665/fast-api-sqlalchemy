from .database import Base
from sqlalchemy import Integer, String, Column

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(String(400))

