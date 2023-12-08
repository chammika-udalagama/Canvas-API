from datetime import datetime
import pandas as pd
from constants import API_TOKEN
from comms import CComm
from api import CAPI


class CCanvas:

    def __init__(self, api_token, course_id=None) -> None:
        self.comm = CComm(parent_name='CCanvas')
        self.api = CAPI(api_token=api_token)

        if course_id is None:
            self.comm.print(
                'Please rerun and specify one of the following course IDs')

            self.get_all_my_courses()
            return None

        self.my_course_id = course_id

        # Add items to API action list
        self.api.actions[CAPI.GET_MY_COURSE_INFO] = f'{self.my_course_id}'
        self.api.actions[CAPI.CREATE_NEW_QUIZ] = f'{self.my_course_id}/quizzes'
        self.api.actions[CAPI.GET_ALL_QUIZ_INFO] = self.api.actions[CAPI.CREATE_NEW_QUIZ]
        self.api.actions[CAPI.DELETE_QUIZ] = self.api.actions[CAPI.CREATE_NEW_QUIZ]

        self.get_my_course_info()

    def get_all_my_courses(self):
        response = self.api.ask(CAPI.GET_ALL_MY_COURSES)
        df = CCanvas.response_to_dataframe(response)
        print(df[['name', 'id']])

    def get_my_course_info(self):
        response = self.api.ask(CAPI.GET_MY_COURSE_INFO)

        if response is not None:
            course_info = response.json()
            msg = '\tInstance bound to course...\n'

            for key in ['name', 'id', 'course_code']:
                msg += f'\t\t{key.title()}: {course_info[key]}' + '\n'

            self.comm.print(msg)

    def create_quiz(self, quiz_info):
        response = self.api.do(CAPI.CREATE_NEW_QUIZ, json_data=quiz_info)
        # df = CCanvas.response_to_dataframe(response)

        if response is not None:
            msg = f"New quiz with id {response.json()['id']} successfully created."
            self.comm.print(msg)

    def delete_quiz(self, quiz_id):
        response = self.api.delete(CAPI.DELETE_QUIZ, item_id=quiz_id)

        if response is not None:
            self.comm.print(f'Quiz {quiz_id} successfuly deleted.')

    def list_quizzes(self):
        response = self.api.ask(CAPI.GET_ALL_QUIZ_INFO)
        df = CCanvas.response_to_dataframe(response)

        if df is not None:
            columns_to_show = ['id', 'title', 'quiz_type']
            print(df[columns_to_show])
            return df['id'].to_list()

    @staticmethod
    def response_to_dataframe(response):
        if response is None:
            return None
        else:
            return pd.DataFrame(response.json())


count = 0

# %%
count += 1
# canvas = CCanvas(API_TOKEN)
canvas = CCanvas(API_TOKEN, course_id=7471)


timing = {
    'start': datetime.strptime('2024-12-12 18:00', '%Y-%m-%d %H:%M'),
    'end': datetime.strptime('2024-12-24 23:00', '%Y-%m-%d %H:%M')
}

quiz_info = {}

quiz_info['quiz'] = {
    'title': f'My API Test Quiz {count}',
    'description': 'Wooooo Haaaa',
    'quiz_type': 'assignment',
    'unlock_at': timing['start'].isoformat(),
    'due_at': timing['end'].isoformat(),
    'published': False,
    'time_limit': None,  # In minutes
    'shuffle_answers': True,
    'allowed_attempts': 1,
    'hide_results': 'until_after_last_attempt'
}

# canvas.delete_quiz(30536)

canvas.create_quiz(quiz_info=quiz_info)
ids = canvas.list_quizzes()

for id in ids:
    canvas.delete_quiz(id)

