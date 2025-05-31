from aiogram import F, Router, types, Bot
from aiogram.filters.command import CommandStart
from keyboards.admin import admin_command
from database.db import DataBase
from aiogram.fsm.context import FSMContext
from config import ADMIN_ID
from aiogram.fsm.state import State, StatesGroup

class Admin_States(StatesGroup):
    get_userinfo = State()
    give_balance = State()
    get_userinfo_del = State()
    delete_balance = State()
    mailing_text = State()

router = Router()

@router.message(F.text == '/admin')
async def admin_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        await state.clear()
        await message.answer("Добро пожаловать", reply_markup=await admin_command(), parse_mode="HTML")

@router.callback_query(F.data == 'stat')
async def statistics_handler(callback: types.CallbackQuery):
    users_count = await DataBase.get_users_count()
    verified_count = await DataBase.get_verified_users_count()

    statistics_message = (
        f"<b>Статистика бота:</b>\n"
        f"🔹 <b>Общее количество пользователей:</b> <code>{users_count}</code>\n"
        f"🔹 <b>Количество пользователей прошедших верификацию:</b> <code>{verified_count}</code>"
    )
    await callback.message.answer(statistics_message, parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data == 'mailing')
async def mailing_state(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except:
        pass
    await callback.message.answer("Отправьте сообщение")
    await state.set_state(Admin_States.mailing_text)

@router.message(Admin_States.mailing_text)
async def mailing_text_handler(message: types.Message, state: FSMContext, bot: Bot):
    data = await DataBase.get_users()
    good, bad = 0, 0
    for user in data:
        try:
            await bot.send_message(user[1], message.text)
            good += 1
        except:
            bad += 1
    await message.answer(f"Рассылка завершена. Успешно: {good}, Ошибки: {bad}")
    await state.clear()

@router.callback_query(F.data == 'change_ref')
async def change_ref_handler(callback: types.CallbackQuery):
    await callback.message.answer("Введите новую реферальную ссылку")
