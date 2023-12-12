#%%
import requests
from datetime import datetime
from constants import API_TOKEN
from canvas import CCanvas
from convert_excel import extract_quiz_info, extract_question_bank

#%%
# canvas = CCanvas(API_TOKEN)
canvas = CCanvas(API_TOKEN, course_id=7471)

ids = canvas.list_quizzes()
for id in ids:
    canvas.delete_quiz(id)

# %%
filename = 'Canvas-Question-Bank.xlsx'
df_quiz_info = extract_quiz_info(filename)
df_question_bank = extract_question_bank(filename)
df_quiz_info

for my_quiz_label in df_quiz_info['my_quiz_label']:
    # my_quiz_label='Quiz_5'

    new_quiz = canvas.create_quiz(df_quiz_info, my_quiz_label)
    new_quiz.add_questions(df_question_bank)
    print("\n")


#%%

# %%
