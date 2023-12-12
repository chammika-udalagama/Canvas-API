from comms import CComm
from api import CAPI
# from datetime import datetime


class CCanvasQuiz:
    def __init__(self,
                 canvas_quiz_id, canvas_course_id,
                 my_quiz_label, api_token) -> None:

        self.comm = CComm(parent_name=f'CCanvasQuiz({canvas_quiz_id})')
        self.api = CAPI(api_token=api_token)

        self.canvas_course_id = canvas_course_id
        self.canvas_quiz_id = canvas_quiz_id
        self.my_quiz_label = my_quiz_label

        # Add items to API action list
        api_message_stem = f'{self.canvas_course_id}/quizzes/{self.canvas_quiz_id}'
        self.api.actions[CAPI.ADD_QUESTIONS_TO_QUIZ] = f'{api_message_stem}/questions'

        msg = f"New quiz with id {canvas_quiz_id}({my_quiz_label}) was successfully created."
        self.comm.print(msg)

    def add_questions(self, df_question_bank):

        # Select relevant questions:
        question_info = self.create_question_list_for_canvas(df_question_bank)

        # question_data = {
        #     "question": {
        #         "question_name": "Multiple Choice Question",
        #         "question_type": "multiple_choice_question",
        #         "points_possible": 1,
        #         "correct_comments": "Correct!",
        #         "incorrect_comments": "Incorrect!",
        #         "answers": [
        #             {"text": "Option A", "weight": 0},
        #             {"text": "Option B", "weight": 0},
        #             {"text": "Option C", "weight": 0},
        #             {"text": "Option D", "weight": 100},
        #             {"text": "Option E", "weight": 0},
        #             # Add more answer choices as needed
        #         ],
        #     }
        # }

        # Add one question at a time
        for index, question in enumerate(question_info, start=1):
            response = self.api.do(CAPI.ADD_QUESTIONS_TO_QUIZ,
                                   json_data=question)

            if response is not None:
                msg = f"{index}: New question successfully added."
                self.comm.print(msg)
            else:
                msg = f"Oops! I encountered a problem!"
                self.comm.print(msg)

    def create_question_list_for_canvas(self, df_question_bank):
        mask = df_question_bank['my_quiz_label'] == self.my_quiz_label
        columns_to_keep = ['question_text', 'correct_comments',
                           'answers', 'question_type', 'points_possible']
        question_info_dict = df_question_bank.loc[mask,
                                                  columns_to_keep].T.to_dict()

        question_info = [{'question': question_info_dict[key]}
                         for key in question_info_dict.keys()]

        return question_info
