import requests

from requests.exceptions import HTTPError
from .glom_translator import translator
from app.core.config import translation_config_gen_url, translation_config_repo_url


def translate_data(data, config):
    return translator.translate(data, config)


async def request_translation_config(job):
    config = None

    # Get the translation config from a remote repository
    if translation_config_repo_url:
        config = await __send_config_query(job, translation_config_repo_url)

    # If this no config could be retrived, query a known translation config generator
    if translation_config_gen_url and not config:
        config = await __send_config_query(job, translation_config_gen_url)

    return config


async def __send_config_query(job, url):

    try:
        response = requests.post(url, data=job)

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        # Success - no error have been raised.
        return response.json()
