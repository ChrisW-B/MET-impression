import requests
import random

departments = ['9', '12', '21']
objects_query = 'https://collectionapi.metmuseum.org/public/collection/v1/objects?departmentIds' + \
    '|'.join(departments)

object_query = 'https://collectionapi.metmuseum.org/public/collection/v1/objects/'


def query_object(object_id):
    query_url = object_query + str(object_id)
    print(query_url)
    object_request = requests.get(url=query_url)
    object_data = object_request.json()
    return object_data


def get_random_art():
    art_list_request = requests.get(url=objects_query)
    object_data = art_list_request.json()
    object_ids = object_data['objectIDs']

    random_entry = random.choice(object_ids)
    selected_object = query_object(random_entry)
    while (not selected_object['primaryImage']):
        random_entry = random.choice(object_ids)
        selected_object = query_object(random_entry)
    return selected_object['primaryImage']


def main():
    art = get_random_art()
    print(art)


if __name__ == '__main__':
    main()
