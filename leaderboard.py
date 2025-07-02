'''
Usage:
python3 leaderboard.py --projects <project names> --url <your instance url>
Example:
python3 leaderboard.py --projects arvp-test arvp-test2 --url https://labelstudio.example.test/
'''

import json
import requests
import argparse

def load_api_key():
    with open('secrets.txt') as f:
        return json.load(f)['API_KEY']

def refresh_token(url, api_key):
    response = requests.post(
        f'{url}api/token/refresh/',
    headers={
        'Content-Type': 'application/json'
    },
    json={
        'refresh': f'{api_key}'
    })

    return response.json()['access']

def get_project_info(url, project_names, token):
    response = requests.get(
        f'{url}api/projects/',
    headers={
        'Authorization': f'Bearer {token}'
    })

    res = [(r['id'], r['task_number']) for r in response.json()['results'] if r['title'] in project_names]
    return res


def get_annotators(url, project_info, token):
    annotators = {}
    for info in project_info:
        response = requests.get(
            f'{url}api/tasks/',
            headers={
                'Authorization': f'Bearer {token}'
            },
            params={
                'project': info[0],
                'page_size': info[1]
            }
        )

        for task in response.json()['tasks']:
            for annotator in task['updated_by']:
                uid = annotator.get('user_id')
                if (uid != None):
                    annotators[uid] = annotators.get(uid, 0) + 1 

    return annotators

def pretty_print_leaderboard(url, annotators, token):
    leaderboard = []

    for uid, score in annotators.items():
        response = requests.get(
            f'{url}api/users/{uid}/',
            headers={
                'Authorization': f'Bearer {token}'
            }
        )

        leaderboard.append({'email': response.json()['email'], 'score': score})

    leaderboard.sort(key=lambda x: x['score'], reverse=True)

    separator = '-' * 60

    print(f"{'Rank':<5} {'Email':40} {'Score':>5}")
    print(separator)

    for i, entry in enumerate(leaderboard, start=1):
        print(f"{i:<5} {entry['email']:40} {entry['score']:>5}")
    print(separator)
    print(f"{'Total':<46} {sum(annotators.values()):>5}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--projects', nargs='+', type=str, required=True)
    parser.add_argument('--url', nargs=1, type=str, required=True)

    parsed_args = parser.parse_args()
    project_names = parsed_args.projects
    url = parsed_args.url[0]
    
    if url[-1] != '/':
        url += '/'

    api_key = load_api_key()
    token = refresh_token(url, api_key)
    project_info = get_project_info(url, project_names, token)
    annotators = get_annotators(url, project_info, token)
    pretty_print_leaderboard(url, annotators, token)

if __name__ == '__main__':
    main()