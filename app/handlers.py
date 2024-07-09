from datetime import datetime

from typing import Any
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery 
from aiogram.filters import Filter, Command

from app.state import Form
import app.tools as tools
from app.jsons import * 
from config import JSON_FILE_NAME_WITH_TASKS, JSON_FILE_NAME_WITH_USERS


router = Router()
data_chat_id = {}

@router.message(Command('start'))
async def start_command(message: Message) -> None:
    await message.reply('<b>Симулятор фарма 1-й части про профилю</b>', parse_mode="HTML")

@router.message(Command('solve'))
async def solve_command(message: Message, state: FSMContext) -> None:
    users = load_data(JSON_FILE_NAME_WITH_USERS)
    if str(message.from_user.id) in users:
        task_number, task_value = tools.random_task_without_answer(JSON_FILE_NAME_WITH_TASKS, str(users[str(message.from_user.id)]))
        await state.update_data(user_task_num=users[str(message.from_user.id)], task_number=task_number)
        await message.reply(f'<b>Задание №{users[str(message.from_user.id)]} #{task_number} \n{task_value["link"]}</b>', parse_mode="HTML")
        await state.set_state(Form.waiting_for_set_answer)
    else:
        await message.reply('<b>Для начала установите номер задания в /set_task</b>', parse_mode="HTML")
    
@router.message(Command('set_task'))
async def set_task_command(message: Message, state: FSMContext) -> None:
    await message.reply('<b>Отправте номер задания</b>', parse_mode="HTML")
    await state.set_state(Form.waiting_for_set_number)

@router.message(Command('rimmed_task'))
async def rimmed_count_command(message: Message) -> None:
    rimmed_tasks, all_tasks = tools.task_rimmed_count(JSON_FILE_NAME_WITH_TASKS)
    await message.reply(f'<i>Заданий осталось <b>{rimmed_tasks}/{all_tasks}</b></i>', parse_mode="HTML")

@router.message(Form.waiting_for_set_number)
async def set_number(message: Message, state: FSMContext) -> None:
    try:
        if 1 <= int(message.text) <= 12:
            users = load_data(JSON_FILE_NAME_WITH_USERS)
            users[str(message.from_user.id)] = int(message.text)
            dump_data(JSON_FILE_NAME_WITH_USERS, users)
            await message.reply(f'<b>Задача №{message.text} установлена, как рашемая в данный момент</b>', parse_mode="HTML")
        else:
            raise ValueError('Task index out of range')
    except (ValueError):
        await message.reply('<b>Отправте номер задания в правильном формате</b>', parse_mode="HTML")
        await state.set_state(Form.waiting_for_set_number)

@router.message(Form.waiting_for_set_answer)
async def set_answer(message: Message, state: FSMContext) -> None:
    txt = message.text.replace(',', '.')
    try:
        if float(txt):
            context_data = await state.get_data()
            tasks = load_data(JSON_FILE_NAME_WITH_TASKS)
            tasks[str(context_data.get('user_task_num'))][context_data.get('task_number')]['answer'] = txt
            dump_data(JSON_FILE_NAME_WITH_TASKS, tasks)
            task_number, task_value = tools.random_task_without_answer(JSON_FILE_NAME_WITH_TASKS, str(context_data.get('user_task_num')))
            await state.update_data(task_number=task_number)
            await message.reply(f'<b>Отлично, ответ сохранен, теперь следующее здание \n\nЗадание №{context_data.get("user_task_num")} #{task_number} \n{task_value["link"]}</b>', parse_mode="HTML")
            await state.set_state(Form.waiting_for_set_answer)
    except (ValueError):
        await message.reply('<b>Укажите ответ в числовом формате</b>', parse_mode="HTML")
        await state.set_state(Form.waiting_for_set_answer)