from datetime import datetime
from constants import API_TOKEN
from canvas import CCanvas

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

# for id in ids:
#     canvas.delete_quiz(id)

