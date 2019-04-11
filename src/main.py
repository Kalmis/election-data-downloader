import requests
import json
from pathlib import Path

BASE_URL = r'https://www.vaalikone.fi/eduskunta2019/api/'
CANDIDATES_SUFFIX = r'candidates'
QUESTIONS_SUFFIX = r'questions/hs'

DATA_FOLDER = Path("/data")
REDOWNLOAD = False


def Main():
    candidates = download_candidate_list()
    save_as_json(candidates, "candidates.json")

    questions = download_questions()
    save_as_json(questions, "questions.json")

    for candidate in candidates:
        id = str(candidate['id'])
        print('Downloading {}'.format(id), end='')
        candidate_file = DATA_FOLDER / id
        candidate_file = candidate_file.with_suffix('.json')
        if candidate_file.is_file() and not REDOWNLOAD:
            print(' - Already downloaded')
            continue

        candidate_data = download_candidate(id)
        save_as_json(candidate_data, id + '.json')

        print(' - done')


def download_candidate_list():
    try:
        r = requests.get(BASE_URL + CANDIDATES_SUFFIX)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Error: {}".format(e))
    except Exception as e:
        print("Unknown error: {}".format(e))
        exit()

    return r.json()


def download_questions():
    try:
        r = requests.get(BASE_URL + QUESTIONS_SUFFIX)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Error: {}".format(e))
    except Exception as e:
        print("Unknown error: {}".format(e))
        exit()

    return r.json()


def download_candidate(candidate_id):
    try:
        r = requests.get(BASE_URL + CANDIDATES_SUFFIX + "/" + candidate_id)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Error: {}".format(e))
    except Exception as e:
        print("Unknown error: {}".format(e))
        exit()

    return r.json()


def save_as_json(data, filename):
    try:
        with open(DATA_FOLDER / filename, 'w') as file:
            json.dump(data, file)
    except Exception as e:
        print("Error saving file {} {}".format(filename, e))
        exit()


def file_exists(filename):
    return


if __name__ == '__main__':
    Main()
