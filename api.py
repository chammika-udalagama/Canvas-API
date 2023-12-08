import requests
from comms import CComm


class CAPI:
    api_url = "https://canvas.nus.edu.sg"

    dummy = 0
    GET_ALL_MY_COURSES = dummy
    dummy += 1
    GET_MY_COURSE_INFO = dummy
    dummy += 1
    CREATE_NEW_QUIZ = dummy
    dummy += 1
    GET_ALL_QUIZ_INFO = dummy
    dummy += 1
    DELETE_QUIZ = dummy

    def __init__(self, api_token) -> None:
        self.headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json',
        }

        self.comm = CComm(parent_name='CAPI')

        # Setup as a dictionary with
        # 'Action': api_call_cmd
        self.actions = {}
        self.actions[CAPI.GET_ALL_MY_COURSES] = ''

    def rqst(self, action, item_id=None):
        cmd = f'{self.api_url}/api/v1/courses/'
        cmd += self.actions[action]

        if action in [CAPI.DELETE_QUIZ]:
            cmd += f'/{item_id}'

        self.comm.print(cmd)
        return cmd

    def ask(self, action):

        response = requests.get(
            self.rqst(action),
            headers=self.headers
        )

        if response.status_code == 200:
            return response
        else:
            print(f'ERROR: {response.status_code} - {response.text}')
            return None

    def do(self, action, json_data=None):

        response = requests.post(
            self.rqst(action),
            headers=self.headers,
            json=json_data
        )

        if response.status_code == 200:
            return response
        else:
            print(f'ERROR: {response.status_code} - {response.text}')
            return None

    def delete(self, action, item_id):

        response = requests.delete(
            self.rqst(action, item_id=item_id),
            headers=self.headers,
        )

        if response.status_code == 200:
            return response
        else:
            print(f'ERROR: {response.status_code} - {response.text}')
            return None
