import pandas as pd
from comms import CComm
from api import CAPI


class CCanvasQuiz:
    def __init__(self, quiz_id, api_token) -> None:
        self.comm = CComm(parent_name=f'CCanvasQuiz({quiz_id})')
        self.api = CAPI(api_token=api_token, target_type=CAPI.TARGET_QUIZZES)

        self.my_quiz_id = quiz_id

        # Add items to API action list
        self.api.actions[CAPI.ADD_QUESTIONS_TO_QUIZ] = f'{self.my_quiz_id}/questions'

        msg = f"New quiz with id {quiz_id} successfully created."
        self.comm.print(msg)

        @staticmethod
        def create_question_list_for_canvas(df_question_bank, quiz_id):
            mask = df_question_bank['my_quiz_id'] == quiz_id
            columns_to_keep = ['question_text', 'correct_comments',
                               'answers', 'question_type', 'points_possible']
            question_info_dict = df_question_bank.loc[mask,
                                                      columns_to_keep].T.to_dict()

            question_info = [{'question': question_info_dict[key]}
                             for key in question_info_dict.keys()]

            return question_info


class CCanvas:
    def __init__(self, api_token, course_id=None) -> None:
        self.comm = CComm(parent_name='CCanvas')
        self.api = CAPI(api_token=api_token)

        if course_id is None:
            self.comm.print(
                'Please rerun and specify one of the following course IDs'
            )

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
            new_quiz_id = response.json()['id']
            return CCanvasQuiz(
                quiz_id=new_quiz_id,
                api_token=self.api.api_token)

    def add_quesitions_ti_quiz(self, quiz_id, question_info):
        response = self.api.do(CAPI.CREATE_NEW_QUIZ, json_data=quiz_info)
        # df = CCanvas.response_to_dataframe(response)

        if response is not None:
            msg = f"New quiz with id {response.json()['id']} successfully created."
            self.comm.print(msg)

    def delete_quiz(self, quiz_id):
        response = self.api.delete(CAPI.DELETE_QUIZ, item_id=quiz_id)

        if response is not None:
            self.comm.print(f'Quiz {quiz_id} successfully deleted.')

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
