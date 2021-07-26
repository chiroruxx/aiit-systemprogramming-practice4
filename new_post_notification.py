import datetime
import json
import os
import urllib.request
import urllib.parse
from dotenv import load_dotenv
from http.client import HTTPResponse
from urllib.error import HTTPError


# esa.io から記事を取得する
def get_posts_from_esa(from_date: datetime, to_date: datetime) -> list:
    esa_api_url: str = 'https://api.esa.io/v1/teams/' + os.environ.get('ESA_API_TEAM') + '/posts'

    from_string: str = from_date.strftime('%Y-%m-%d')
    to_string: str = to_date.strftime('%Y-%m-%d')
    esa_api_query: dict = {
        'access_token': os.environ.get('ESA_API_TOKEN'),
        'q': '-category:Archived created:>' + from_string + ' ' + 'created:<' + to_string
    }
    esa_api_query_string: str = urllib.parse.urlencode(esa_api_query)

    try:
        response: HTTPResponse = urllib.request.urlopen(esa_api_url + '?' + esa_api_query_string)
    except HTTPError as e:
        print('Failed to send request to esa.io')
        print(e)
        exit(1)

    response_content: dict = json.loads(response.read().decode('utf8'))
    if 'posts' not in response_content:
        print('Failed to parse response from esa.io')
        print('Check format of esa.io API.')
        exit(1)

    return response_content['posts']


# 記事を slack へ送信する
def send_posts_to_slack(posts: list):
    # 作成日降順
    sorted(posts, key=lambda x: datetime.datetime.fromisoformat(x['created_at']).timestamp(), reverse=True)

    message: dict = {
        'blocks': [
            {
                'type': 'section',
                'text': {
                    'type': 'plain_text',
                    'text': 'こんにちは。今日の新着の投稿です。'
                }
            },
            {
                'type': 'divider'
            }
        ]
    }

    for post in posts:
        url: str = post['url']
        created_at: str = datetime.datetime.fromisoformat(post['created_at']).strftime('%Y-%m-%d %H:%M')
        title: str = post['full_name']
        author: str = post['created_by']['name']

        message['blocks'].append({
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': '<' + url + '|*' + title + '*> ' + created_at + '\nFrom ' + author
            }
        })

    header: dict = {
        'Content-Type': 'application/json'
    }

    request = urllib.request.Request(os.environ.get('SLACK_INCOMING_WEBHOOK'), json.dumps(message).encode(), header)
    try:
        urllib.request.urlopen(request)
    except HTTPError as e:
        print('Failed to send request to slack')
        print(e)
        exit(1)


load_dotenv()

from_date: datetime = datetime.datetime.now()
to_date: datetime = from_date + datetime.timedelta(days=1)

posts: list = get_posts_from_esa(from_date, to_date)
send_posts_to_slack(posts)
