'''
Usage:
python3 create_tabs.py --project <project_name> --images <number of images per tab> --url <your instance url>
Example:
python3 create_tabs.py --project arvp-test --images 100 --url https://labelstudio.example.test/
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

def get_project_info(url, project, token):
    response = requests.get(
        f'{url}api/projects/',
    headers={
        'Authorization': f'Bearer {token}'
    })

    res = [(r['id'], r['task_number']) for r in response.json()['results'] if r['title'] == project]
    return res[0]

def create_tabs(url, project_id, token, n_tasks, n_images):
    for i in range(0, n_tasks, n_images):
        data = {
            'project': project_id,
            'data': {
                'title': f'{i + 1}-{min(i + n_images, n_tasks)}',
                'filters': {
                    'conjunction': 'or',
                    'items': [{
                        'filter': 'filter:tasks:inner_id',
                        'operator': 'in',
                        'value': {
                            'min': i + 1,
                            'max': i + n_images
                        },
                        'type': 'Number'
                    }]
                },
                'hiddenColumns': {
                    'explore': ["tasks:id", "tasks:annotations_results","tasks:annotations_ids","tasks:predictions_score","tasks:predictions_model_versions","tasks:predictions_results","tasks:file_upload","tasks:storage_filename","tasks:created_at","tasks:updated_at","tasks:updated_by","tasks:avg_lead_time","tasks:draft_exists"],
                    'labeling': ["tasks:id","tasks:inner_id","tasks:completed_at","tasks:cancelled_annotations","tasks:total_predictions","tasks:annotators","tasks:annotations_results","tasks:annotations_ids","tasks:predictions_score","tasks:predictions_model_versions","tasks:predictions_results","tasks:file_upload","tasks:storage_filename","tasks:created_at","tasks:updated_at","tasks:updated_by","tasks:avg_lead_time","tasks:draft_exists"]
                }
            }
        }
        response = requests.post(
            f'{url}api/dm/views/',
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        },
        json=data)

        if response.status_code != 201:
            print(response.status_code)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', nargs=1, type=str, required=True)
    parser.add_argument('--url', nargs=1, type=str, required=True)
    parser.add_argument('--images', nargs=1, type=int, required=True)

    parsed = parser.parse_args()
    project = parsed.project[0]
    images = parsed.images[0]
    url = parsed.url[0]

    if url[-1] != '/':
        url += '/'

    api_key = load_api_key()
    token = refresh_token(url, api_key)  
    project_id, n_tasks = get_project_info(url, project, token)
    create_tabs(url, project_id, token, n_tasks, images)

if __name__ == '__main__':
    main()