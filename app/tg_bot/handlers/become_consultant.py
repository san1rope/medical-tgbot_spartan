from typing import Union

from aiogram import Router, F, types, enums
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.tg_bot.config import Config
from app.tg_bot.keyboards.inline import InlineMarkups as Im, CustomCallback
from app.tg_bot.misc.models import ConsultantForm
from app.tg_bot.misc.states import ConsultantRegistration
from app.tg_bot.misc.utils import Utils as Ut

router = Router()


@router.message(F.chat.type == enums.ChatType.PRIVATE, Command("become_consultant"))
@router.callback_query(F.data == "become_consultant")
async def cmd_become_consultant(message: Union[types.Message, types.CallbackQuery], state: FSMContext):
    uid = message.from_user.id
    Config.logger.info(f"Handler called. {cmd_become_consultant.__name__}. user_id={uid}")

    if isinstance(message, types.CallbackQuery):
        await message.answer()

    text = [
        "<b>👨‍⚕️ Стать консультантом</b>",
        "\n<b>Вы можете помогать другим пользователям, отвечая на их вопросы в своей области.</b>",
        "<b>Чтобы подать заявку на роль консультанта, пожалуйста, заполните короткую анкету ниже.</b>",
        "\n<b>ℹ️ Что-бы вернуться, нажмите кнопку Назад</b>",
        "\n<b>Напишите свое имя</b>"
    ]
    await Ut.send_step_message(state=state, text="\n".join(text), markup=await Im.back(callback_data="back_to_menu"))
    await state.set_state(ConsultantRegistration.Name)


@router.message(ConsultantRegistration.Name)
@router.callback_query(F.data == "back_to_cons_name")
async def write_name(message: Union[types.Message, types.CallbackQuery], state: FSMContext):
    uid = message.from_user.id
    Config.logger.info(f"Handler called. {write_name.__name__}. user_id={uid}")

    if isinstance(message, types.CallbackQuery):
        await message.answer()

    else:
        name = message.text.strip()
        if len(name) < 3:
            msg = await message.answer(text="<b>🔴 Имя не может быть меньше 3 символов!</b>")
            await Ut.add_msg_to_delete(state=state, msg_id=msg.message_id)
            return

        try:
            await state.update_data(c_form=ConsultantForm(name=name).model_dump())

        except ValueError:
            msg = await message.answer(text="<b>🔴 Неверный формат имени!</b>")
            await Ut.add_msg_to_delete(state=state, msg_id=msg.message_id)
            return

    text = [
        "<b>👨‍⚕️ Стать консультантом</b>",
        "\n<b>Дальше вам нужно рассказать о себе (образование, опыт)</b>",
        "\n<b>ℹ️ Пожалуйста, опишите ваш профессиональный путь. Эта информация поможет владельцу бота подтвердить вашу квалификацию.</b>",
    ]
    await Ut.send_step_message(state=state, text="\n".join(text), markup=await Im.back(callback_data="become_consultant"))

    await state.set_state(ConsultantRegistration.AboutYourself)


@router.message(ConsultantRegistration.AboutYourself)
@router.callback_query(F.data == "back_to_about_yourself")
async def write_about_yourself(message: Union[types.Message, types.CallbackQuery], state: FSMContext):
    uid = message.from_user.id
    Config.logger.info(f"Handler called. {write_about_yourself.__name__}. user_id={uid}")

    if isinstance(message, types.CallbackQuery):
        await message.answer()

    else:
        about_yourself = message.text.strip()
        if len(about_yourself) < 50:
            msg = await message.answer(text="<b>🔴 Текст должен быть не менее 50 символов!</b>")
            await Ut.add_msg_to_delete(state=state, msg_id=msg.message_id)
            return

        c_form = ConsultantForm(**(await state.get_value("c_form")))

        try:
            c_form.about_yourself = about_yourself
            await state.update_data(c_form=c_form.model_dump())

        except ValueError:
            msg = await message.answer(text="<b>🔴 Неверный формат имени!</b>")
            await Ut.add_msg_to_delete(state=state, msg_id=msg.message_id)
            return

    text = [
        "<b>👨‍⚕️ Стать консультантом</b>",
        "\n<b>🌍 Выберите вашу страну проживания</b>",
        "<b>Пожалуйста, выберите страну из списка ниже.</b>",
        "\n<b>⬇️ Используйте кнопки под сообщением</b>"
    ]
    await Ut.send_step_message(
        state=state, text="\n".join(text), markup=await Im.continents(cont_cd="bc_cons_cont", back_cd="back_to_cons_name"))

    await state.set_state(ConsultantRegistration.Country)


@router.callback_query(ConsultantRegistration.Country, CustomCallback.filter(F.role == "bc_cons_count_to_continents"))
async def keyboard_back_to_continents(callback: CallbackQuery, callback_data: CustomCallback):
    await callback.answer()
    uid = callback.from_user.id
    Config.logger.info(f"Handler called. {keyboard_back_to_continents.__name__}. user_id={uid}")

    await callback.message.edit_reply_markup(
        reply_markup=await Im.continents(cont_cd="bc_cons_cont", back_cd="back_to_cons_name"))


@router.callback_query(ConsultantRegistration.Country, CustomCallback.filter(F.role == "bc_cons_cont"))
async def keyboard_selected_continent(callback: types.CallbackQuery, state: FSMContext, callback_data: CustomCallback):
    await callback.answer()
    uid = callback.from_user.id
    Config.logger.info(f"Handler called. {keyboard_selected_continent.__name__}. user_id={uid}")

    await state.update_data(selected_continent=callback_data.data)
    await callback.message.edit_reply_markup(
        reply_markup=await Im.countries(
            continent=callback_data.data, page=1, count_cd="bc_cons_count", back_cd="back_to_cons_name")
    )


@router.callback_query(ConsultantRegistration.Country, CustomCallback.filter(F.role == "bc_cons_count_set_page"))
async def keyboard_countries_set_page(callback: types.CallbackQuery, state: FSMContext, callback_data: CustomCallback):
    await callback.answer()
    uid = callback.from_user.id
    Config.logger.info(f"Handler called. {keyboard_countries_set_page.__name__}. user_id={uid}")

    markup = await Im.countries(
        continent=await state.get_value("selected_continent"),
        page=int(callback_data.data), count_cd="bc_cons_count", back_cd="back_to_cons_name"
    )
    if markup is None:
        return

    await callback.message.edit_reply_markup(reply_markup=markup)


@router.callback_query(ConsultantRegistration.Country, CustomCallback.filter(F.role == "bc_cons_count"))
@router.callback_query(F.data == "back_to_locality")
async def select_country(callback: types.CallbackQuery, state: FSMContext, callback_data: CustomCallback):
    await callback.answer()
    uid = callback.from_user.id
    Config.logger.info(f"Handler called. {select_country.__name__}. user_id={uid}")

    if callback_data.data == "0":
        return

    c_form = ConsultantForm(**(await state.get_value("c_form")))
    c_form.country = callback_data.data
    await state.update_data(c_form=c_form)

    text = [
        "<b>👨‍⚕️ Стать консультантом</b>",
        "\n<b>Назвите населенный пункт страны в котором вы проживаете</b>",
        "\n<b>⬇️  Вам нужно его написать</b>"
    ]
    await Ut.send_step_message(state=state, text="\n".join(text), markup=await Im.back(callback_data="back_to_about_yourself"))

    await state.set_state(ConsultantRegistration.Locality)


@router.message(ConsultantRegistration.Locality)
async def write_locality(message: Union[types.Message, types.CallbackQuery], state: FSMContext):
    uid = message.from_user.id
    Config.logger.info(f"Handler called. {write_locality.__name__}. user_id={uid}")

    locality = message.text.strip()
    if len(locality) < 2:
        msg = await message.answer(text="<b>🔴 Название населенного пункта не может быть менее 2 символов!</b>")
        await Ut.add_msg_to_delete(state=state, msg_id=msg.message_id)
        return

    c_form = ConsultantForm(**(await state.get_value("c_form")))

    try:
        c_form.locality = locality
        await state.update_data(c_form=c_form)

    except ValueError:
        msg = await message.answer(text="<b>🔴 Неверный названия населенного пункта!</b>")
        await Ut.add_msg_to_delete(state=state, msg_id=msg.message_id)
        return

    text = [
        "<b>👨‍⚕️ Стать консультантом</b>",
        "\n<b>📧 Введите ваш Email</b>",
        "\n<b>Пожалуйста, напишите ваш адрес электронной почты.</b>",
        "\n<b>ℹ️ Мы отправим на него одноразовый код для подтверждения анкеты.</b>"
    ]
    await Ut.send_step_message(state=state, text="\n".join(text), markup=await Im.back(callback_data="back_to_locality"))

    await state.set_state(ConsultantRegistration.Email)


@router.message(ConsultantRegistration.Email)
async def write_email(message: Union[types.Message, types.CallbackQuery], state: FSMContext):
    uid = message.from_user.id
    Config.logger.info(f"Handler called. {write_email.__name__}. user_id={uid}")

    email = message.text.strip()
    c_form = ConsultantForm(**(await state.get_value("c_form")))
    c_form.email = email
    await state.update_data(c_form=c_form)
