from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from webapp.models.meta import DEFAULT_SCHEMA, Base
from datetime import datetime

class Post(Base):
    __tablename__ = 'posts'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    text: Mapped[str] = Column(String)
    author_id: Mapped[int] = Column(Integer, ForeignKey('users.id'))
    comment_id: Mapped[int] = Column(Integer, ForeignKey('comments.id'))
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)

    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")