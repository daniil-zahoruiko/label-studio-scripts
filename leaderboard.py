import json
import requests
import argparse

def load_api_key():
    with open('secrets.txt') as f:
        return json.load(f)[0]['API_KEY']

def refresh_token(api_key):
    response = requests.post(
        'https://cvat.mami2.moe/api/token/refresh/',
    headers={
        'Content-Type': 'application/json'
    },
    json={
        'refresh': f'{api_key}'
    })

    return response.json()['access']

def get_project_info(project_names, token):
    response = requests.get(
        'https://cvat.mami2.moe/api/projects/',
    headers={
        'Authorization': f'Bearer {token}'
    })

    res = [(r['id'], r['task_number']) for r in response.json()['results'] if r['title'] in project_names]
    return res


def get_annotators(project_info, token):
    annotators = {}
    for info in project_info:
        response = requests.get(
            'https://cvat.mami2.moe/api/tasks/',
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

def get_username_annotations(task_ids, token):
    result = {}
    for id in task_ids:
        response = requests.get(
            f'https://cvat.mami2.moe/api/tasks/{id}/annotations/',
            headers={
                'Authorization': f'Bearer {token}'
            },
            params={
                'fields': 'all'
            }
        )

        for annotation in response.json():
            username = annotation['created_username']
            result[username] = result.get(username, 0) + 1

    return result

def pretty_print_leaderboard(annotators, token):
    leaderboard = []

    for uid, score in annotators.items():
        response = requests.get(
            f'https://cvat.mami2.moe/api/users/{uid}/',
            headers={
                'Authorization': f'Bearer {token}'
            }
        )

        leaderboard.append({'email': response.json()['email'], 'score': score})

    leaderboard.sort(key=lambda x: x['score'], reverse=True)

    print(f"{'Rank':<5} {'Email':40} {'Score':>5}")
    print('-' * 60)

    for i, entry in enumerate(leaderboard, start=1):
        print(f"{i:<5} {entry['email']:40} {entry['score']:>5}")
    print('-' * 60)
    print(f"{'Total':<46} {sum(annotators.values()):>5}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--projects', nargs='+', type=str)
    project_names = parser.parse_args().projects

    api_key = load_api_key()
    token = refresh_token(api_key)
    project_info = get_project_info(project_names, token)
    annotators = get_annotators(project_info, token)
    pretty_print_leaderboard(annotators, token)

if __name__ == '__main__':
    main()