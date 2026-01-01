from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base

# Note - each class in the models file represents a table

class Post(Base):
    __tablename__ = "Posts"
    
    id = Column(Integer, primary_key=True, nullable=False)
    User_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user = relationship("User")


class User(Base):
    __tablename__ = "Users"

    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Vote(Base):
    __tablename__ = "Votes"

    post_id = Column(Integer, ForeignKey("Posts.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    voter_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    upvote = Column(Boolean, nullable=True)
    downvote = Column(Boolean, nullable=True)

    