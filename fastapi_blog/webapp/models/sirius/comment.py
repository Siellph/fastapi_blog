from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from webapp.models.meta import DEFAULT_SCHEMA, Base
from datetime import datetime


class Comment(Base):
    __tablename__ = 'comments'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(String)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('posts.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime,
                                                 default=datetime.utcnow)

    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
