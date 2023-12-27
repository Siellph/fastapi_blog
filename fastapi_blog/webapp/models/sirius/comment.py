from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from webapp.models.meta import DEFAULT_SCHEMA, Base
from datetime import datetime

class Comment(Base):
    __tablename__ = 'comments'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    text: Mapped[str] = Column(String)
    author_id: Mapped[int] = Column(Integer, ForeignKey('users.id'))
    post_id: Mapped[int] = Column(Integer, ForeignKey('posts.id'))
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)

    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")