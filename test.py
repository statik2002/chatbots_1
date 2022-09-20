
inf = {
    "status": "found",
    "new_attempts": [
        {
            "submitted_at": "2019-03-28...",
            "is_negative": 'false',
            "lesson_title": "Готовим речь",
            "timestamp": 1455609162.580245
        }
    ],
    "last_attempt_timestamp": 1455609162.580245
}

if inf['status'] == 'found':
    print(inf['new_attempts'][0]['is_negative'])
