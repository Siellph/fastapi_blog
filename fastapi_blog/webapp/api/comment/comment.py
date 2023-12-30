from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .router import comment_router
from webapp.crud.comment import create_comment, delete_comment, get_comment_by_id, get_comments_by_post, update_comment
from webapp.db.postgres import get_session
from webapp.models.sirius.user import User
from webapp.schema.content.comment import CommentCreate, CommentRead, CommentUpdate
from webapp.utils.auth.user import get_current_user


@comment_router.get('/{post_id}', response_model=List[CommentRead])
async def read_comments(post_id: int, session: AsyncSession = Depends(get_session)):
    return await get_comments_by_post(session, post_id)


@comment_router.post('/{post_id}/create_comments', response_model=CommentRead, status_code=status.HTTP_201_CREATED)
async def create(
    post_id: int,
    comment: CommentCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await create_comment(session, comment.content, current_user.id, post_id)


@comment_router.put('/{comment_id}', response_model=CommentRead)
async def update(
    comment_id: int,
    comment_update: CommentUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    comment = await get_comment_by_id(session, comment_id)
    if not comment or comment.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to update this comment')
    return await update_comment(session, comment_id, comment_update.content)


@comment_router.delete('/{comment_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    comment_id: int, session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)
):
    comment = await get_comment_by_id(session, comment_id)
    if not comment or comment.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to delete this comment')
    await delete_comment(session, comment_id)
    return {'detail': 'Comment deleted'}
