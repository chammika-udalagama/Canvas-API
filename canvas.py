import requests
import pandas as pd
from constants import API_TOKEN


class CAPI:
    api_url = "https://canvas.nus.edu.sg/"

    def __init__(self, api_token) -> None:
        self.headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        }

    def rqst(self, cmd):
        return f'{self.api_url}/api/v1/courses/{cmd}'

    def ask(self, reqeust_info):

        response = requests.get(
            self.rqst(reqeust_info),
            headers=self.headers
        )

        if response.status_code == 200:
            return response
        else:
            print(f'ERROR: {response.status_code} - {response.text}')
            return None


class CComm:

    def __init__(self, parent_name, verbosity=True) -> None:
        self.parent_name = parent_name
        self.verbosity = verbosity

    def print(self, msg):
        msg = f'{self.parent_name}: {msg}'
        print(msg)


class CCanvas:

    def __init__(self, api_token, course_id=None) -> None:
        self.comm = CComm(parent_name='CCanvas')
        self.api = CAPI(api_token=api_token)

        if course_id is None:
            self.comm.print(
                'Please rerun and specify one of the following course IDs')

            self.my_course_info()
        else:
            

    def my_course_info(self):

        response = self.api.ask('')

        if response is not None:
            courses = response.json()

            # for course in courses:
            #     print(f"{course['name']} (ID: {course['id']})")
            df_course_info = pd.DataFrame(courses)
            print(df_course_info[['name', 'id']])

# %%


canvas = CCanvas(API_TOKEN, course_id=7471)
