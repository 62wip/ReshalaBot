from random import choice

from app.jsons import load_data


def random_task_without_answer(file_name: str, number: str) -> list[str, str]:
    tasks_by_number = load_data(file_name)
    items_with_null_answer = {key: value for key, value in tasks_by_number[number].items() if value['answer'] is None}
    if not items_with_null_answer:
        return None
    random_key = choice(list(items_with_null_answer.keys()))
    return random_key, items_with_null_answer[random_key]


def task_rimmed_count(file_name: str)-> list[str, str]:
    tasks_by_number = load_data(file_name)
    count_without_answer = sum(1 for task_data in tasks_by_number.values() for answer in task_data.values() if answer["answer"] is None)
    total_tasks = sum(len(task_data) for task_data in tasks_by_number.values())
    return count_without_answer, total_tasks