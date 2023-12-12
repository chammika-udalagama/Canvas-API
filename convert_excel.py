import pandas as pd
from datetime import datetime


def extract_quiz_info(filename):
    print(f'Extracting quiz information from Excel file ({filename}).')
    df = pd.read_excel(filename, sheet_name='Quiz Info')
    df.columns = [column.lower().replace(' ', '_') for column in df.columns]
    time_columns = ['unlock_at', 'due_at', 'show_correct_answers_at']
    df[time_columns] = df[time_columns].map(datetime.isoformat)

    df['time_limit'] = df['time_limit'].apply(
        lambda limit: None if limit == 0 else limit)

    quiz_ids = df['my_quiz_label'].unique().tolist()
    print(f'I found the following {len(quiz_ids)} unique quiz ids:')
    for index, quiz_id in enumerate(quiz_ids, start=1):
        print(index, ':', quiz_id)

    # df.set_index('my_quiz_label', inplace=True)

    return df


def expand_question_bank(df):
    df['my_quiz_label'] = df['my_quiz_label'].str.split(',')

    df_expanded = pd.DataFrame(columns=df.columns)

    for index, row in df.iterrows():
        for quiz_id in row['my_quiz_label']:
            new_index = len(df_expanded)
            df_expanded.loc[new_index] = row
            df_expanded.loc[new_index, 'my_quiz_label'] = quiz_id

    return df_expanded


def extract_question_bank(filename):
    df = pd.read_excel(filename, sheet_name='Question Bank')
    df.columns = [column.lower().replace(' ', '_') for column in df.columns]
    df = expand_question_bank(df)

    df.rename(
        columns={'rationale_for_correct_answer': 'correct_comments'}, inplace=True)

    # Create answer list in the format accepted by Canvas
    answer_columns = ['a', 'b', 'c', 'd', 'e']
    df['a'] = df['a'].apply(lambda cell: {'text': cell, 'weight': 100})

    df[answer_columns[1:]] = df[answer_columns[1:]].map(
        lambda cell: {'text': cell, 'weight': 0}
    )

    df['answers'] = df[answer_columns].apply(list, axis=1)
    df.drop(columns=answer_columns, inplace=True)

    df['question_type'] = 'multiple_choice_question'
    df['points_possible'] = 1

    return df

# df_quiz_info = extract_quiz_info(filename)
# df_question_bank = extract_question_bank(filename)
