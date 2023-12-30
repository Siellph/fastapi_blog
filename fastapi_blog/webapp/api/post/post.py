from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .router import post_router
from webapp.crud.post import create_post, delete_post, get_all_posts, get_post_by_id, get_posts_by_user, update_post
from webapp.db.postgres import get_session
from webapp.schema.content.post import PostCreate, PostRead, PostUpdate
from webapp.schema.login.user import User
from webapp.utils.auth.user import get_current_user


@post_router.get('/', response_model=List[PostRead])
async def read_posts(session: AsyncSession = Depends(get_session)):
    return await get_all_posts(session)


@post_router.get('/{post_id}', response_model=PostRead)
async def read_post_by_id(post_id: int, session: AsyncSession = Depends(get_session)):
    post = await get_post_by_id(session, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    return post


@post_router.get('/{user_id}', response_model=List[PostRead])
async def read_posts_by_user(user_id: int, session: AsyncSession = Depends(get_session)):
    posts = await get_posts_by_user(session, user_id)
    return posts


@post_router.post('/create', response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create(
    post: PostCreate, session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)
):
    return await create_post(session, post.content, current_user.id)


@post_router.put('/{post_id}', response_model=PostRead)
async def update(
    post_id: int,
    post_update: PostUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    post = await get_post_by_id(session, post_id)
    if not post or post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to update this post')
    return await update_post(session, post_id, post_update.content)


@post_router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    post_id: int, session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)
):
    post = await get_post_by_id(session, post_id)
    if not post or post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to delete this post')
    await delete_post(session, post_id)
    return {'detail': 'Post deleted'}
