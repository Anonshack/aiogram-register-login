import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.filters import Text  # Text filtrini shunday import qiling
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from buttons import keyboard, check
from form import Login, Facebook, Form, DataUser
from root import TOKEN, CHAT_ID

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# Start komandasi
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer_photo(
        photo="https://onlinedegrees.sandiego.edu/wp-content/uploads/2023/05/6-careers-you-can-get-with-python.jpg",
        caption=f"Assalomu alekum, kanalga obuna buling! {message.from_user.full_name}",
        reply_markup=check)


# Callback query handler
@dp.callback_query(Text(equals='submit'))
async def callback_submit(call: CallbackQuery):
    user_status = await bot.get_chat_member(chat_id=CHAT_ID, user_id=call.from_user.id)
    if user_status.status != "left":
        await bot.send_message(call.from_user.id, "✅")
        await call.message.answer("Login or Register", reply_markup=keyboard)
    else:
        await bot.send_message(call.from_user.id, text="Siz kanalga obuna bulmagansiz!", reply_markup=check)
        text = "Kanalga obuna bo'lmagansiz ⚠️"
        await call.answer(text, show_alert=True)


# Reg message handler
@dp.message()
async def reg(message: Message, state: FSMContext):
    if message.text == "Register":
        await state.set_state(Form.name)
        await message.answer("Enter name")
    elif message.text == "Login":
        await state.set_state(Login.username)
        await message.answer("Enter username: ")
    elif message.text == "Ariz yuborish":
        await state.set_state(Facebook.fullname)
        await message.answer("Enter fullname: ")


# Form states handlers
@dp.message(Form.name)
async def usernames(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.username)
    await message.answer("Enter username")


@dp.message(Form.username)
async def passwords(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(Form.password)
    await message.answer("Enter password")


@dp.message(Form.password)
async def finish(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await state.set_state(Form.finish)
    data = await state.get_data()
    await state.clear()
    await message.answer("You have successfully registered")

    name = data.get("name", "Unknown")
    username = data.get("username", "Unknown")
    password = data.get("password", "Unknown")

    DataUser["username"] = username
    DataUser["password"] = password

    matn = f"🧑‍💻 Name: {name}\n⚡️ Username: {username}\n🔐 Password: {password}"
    btn = [
        [types.KeyboardButton(text="Ariz yuborish")]
    ]
    key = types.ReplyKeyboardMarkup(keyboard=btn, resize_keyboard=True)
    await message.answer(text=matn, reply_markup=key)


# Login states handlers
@dp.message(Login.username)
async def login(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(Login.password)
    await message.answer("Enter password: ")


@dp.message(Login.password)
async def finish_login(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await state.set_state(Login.finish)
    userdata = await state.get_data()
    await state.clear()

    username = userdata.get("username", "Unknown")
    password = userdata.get("password", "Unknown")

    if username == DataUser["username"] and password == DataUser["password"]:
        btn = [
            [types.KeyboardButton(text="Ariz yuborish")]
        ]
        key = types.ReplyKeyboardMarkup(keyboard=btn, resize_keyboard=True)
        await message.answer("You have successfully logged in ✅", reply_markup=key)
    else:
        await message.answer("Invalid username or password ⁉️")


# Facebook states handlers
@dp.message(Facebook.fullname)
async def facebook(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await state.set_state(Facebook.phone)
    await message.answer("Enter your phone: ")


@dp.message(Facebook.phone)
async def facebook_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(Facebook.address)
    await message.answer("Enter your address: ")


@dp.message(Facebook.address)
async def facebook_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(Facebook.child)
    await message.answer("Your child's fullname: ")


@dp.message(Facebook.child)
async def facebook_child(message: Message, state: FSMContext):
    await state.update_data(child=message.text)
    await state.set_state(Facebook.sinf)
    await message.answer("Child's class: ")


@dp.message(Facebook.sinf)
async def facebook_class(message: Message, state: FSMContext):
    await state.update_data(sinf=message.text)
    await state.set_state(Facebook.finish)
    data = await state.get_data()
    await state.clear()
    await message.answer("Ariza qabul qilindi!")

    fullname = data.get("fullname", "Unknown")
    phone = data.get("phone", "Unknown")
    address = data.get("address", "Unknown")
    child = data.get("child", "Unknown")
    sinf = data.get("sinf", "Unknown")

    await message.answer(
        f"⚡️Fullname: {fullname}\n📞Phone: {phone}\n🗺Address: {address}\n👩Child: {child}\n🙎‍♂️Class: {sinf}")
    await bot.send_message(chat_id=CHAT_ID,
                           text=f"⚡️Fullname: {fullname}\n📞Phone: {phone}\n🗺Address: {address}\n👩Child: {child}\n🙎‍♂️Class: {sinf}")


#qudratbekh
async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
