import requests
from comms import CComm


class CAPI:
    API_URL = "https://canvas.nus.edu.sg"
    GET_ALL_MY_COURSES = 0
    GET_MY_COURSE_INFO = 1
    CREATE_NEW_QUIZ = 2
    ADD_QUESTIONS_TO_QUIZ = 3
    GET_ALL_QUIZ_INFO = 4
    DELETE_QUIZ = 5

    def __init__(self, api_token) -> None:
        self.api_token = api_token
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json',
        }
        self.comm = CComm(parent_name='CAPI')
        self.actions = {}
        self.actions[CAPI.GET_ALL_MY_COURSES] = ''

    def rqst(self, action, item_id=None):
        cmd = f'{self.API_URL}/api/v1/courses/'
        cmd += self.actions[action]
        if action in [CAPI.DELETE_QUIZ]:
            cmd += f'/{item_id}'
        self.comm.print(cmd)
        return cmd

    @staticmethod
    def check_status(response):
        if response.status_code == 200:
            return response
        else:
            print(f'ERROR: {response.status_code} - {response.text}')
            return None

    def ask(self, action):
        response = requests.get(
            self.rqst(action),
            headers=self.headers
        )
        return self.check_status(response)

    def do(self, action, json_data=None):
        response = requests.post(
            self.rqst(action),
            headers=self.headers,
            json=json_data
        )
        return self.check_status(response)

    def delete(self, action, item_id):
        response = requests.delete(
            self.rqst(action, item_id=item_id),
            headers=self.headers,
        )
        return self.check_status(response)
