import pandas as pd
from datetime import datetime

filename = 'Canvas Question Bank.xlsx'


def extract_quiz_info(filename):
    df = pd.read_excel(filename, sheet_name='Quiz Info')

    df.columns = [column.lower().replace(' ', '_') for column in df.columns]

    time_columns = ['unlock_at', 'due_at', 'show_correct_answers_at']
    df[time_columns] = df[time_columns].applymap(datetime.isoformat)

    return df

def expand_question_bank(df):
    df['my_quiz_id'] = df['my_quiz_id'].str.split(',')

    df_expanded = pd.DataFrame(columns=df.columns)

    for index, row in df.iterrows():
        for quiz_id in row['my_quiz_id']:
            new_index = len(df_expanded)
            df_expanded.loc[new_index] = row
            df_expanded.loc[new_index, 'my_quiz_id'] = quiz_id

    return df_expanded

def extract_question_bank(filename):
    df = pd.read_excel(filename, sheet_name='Question Bank')

    columns_to_keep = [
        'My Quiz ID',
        'Question Text',
        'A', 'B', 'C', 'D', 'E',
        'Rationale for Correct Answer']

    df = df[columns_to_keep]
    df.columns = [column.lower().replace(' ', '_') for column in df.columns]

    df = expand_question_bank(df)

    # Create answer list
    answer_columns = ['a', 'b', 'c', 'd', 'e']
    df['a'] = df['a'].apply(lambda cell: {'text': cell, 'weight': 100})

    df[answer_columns[1:]] = df[answer_columns[1:]].applymap(
        lambda cell: {'text': cell, 'weight': 0}
    )

    df['answers'] = df[answer_columns].apply(list, axis=1)
    df.drop(columns=answer_columns, inplace=True)

    df['question_type'] = 'multiple_choice_question'
    df['points_possible'] = 1

    return df


df_quiz_info = extract_quiz_info(filename)
df_question_bank = extract_question_bank(filename)
df_question_bank
