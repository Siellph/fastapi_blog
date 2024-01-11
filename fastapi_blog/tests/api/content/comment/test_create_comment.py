import json
from pathlib import Path
from typing import List

import pytest
import msgpack
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

# Пути к фикстурам
BASE_DIR = Path(__file__).parent
FIXTURES_PATH = BASE_DIR / 'fixtures'


# Тест на создание комментария
@pytest.mark.parametrize(
    (
        'username',
        'password',
        'post_id',
        'content',
        'expected_status',
        'fixtures',
        'kafka_expected_messages'
    ),
    [
        (
            'autotest',
            'qwerty',
            1,
            'Great job!',
            status.HTTP_201_CREATED,
            [
                FIXTURES_PATH / 'sirius.user.json',
                FIXTURES_PATH / 'sirius.post.json'
            ],
            [
                {
                    'partition': 1,
                    'topic': 'create_comment',
                    'value':
                        [
                            {
                                'content': 'Great job!',
                            }
                        ]
                }
            ],
        )
    ]
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures('_common_api_with_kafka_fixture')
async def test_create_comment(
    client: AsyncClient,
    username: str,
    password: str,
    post_id: int,
    content: str,
    expected_status: int,
    access_token,
    kafka_received_messages: List,
    kafka_expected_messages: List,
):
    headers = {'Authorization': f'Bearer Bearer {access_token}'}
    response = await client.post(
        URLS['comments']['create'].format(post_id=post_id),
        json={'content': content},
        headers=headers,
    )

    # Проверки ответа и сообщений Kafka
    assert response.status_code == expected_status
    assert kafka_received_messages == kafka_expected_messages
    # assert len(kafka_received_messages) == 1
    # kafka_message = kafka_received_messages[0]
    # assert kafka_message['topic'] == 'create_comment'
    # assert json.loads(kafka_message['value']) == {
    #     'id': response.json()['id'],
    #     'content': content
    # }
