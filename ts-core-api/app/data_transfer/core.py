
import requests

def start_transfer(target_dcon_url: str, data_to_transfer: dict):
    
    try:
        response = requests.post(target_dcon_url + '/import-end-point', data=data_to_transfer)

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        # Success - no error have been raised.
        return response.json()