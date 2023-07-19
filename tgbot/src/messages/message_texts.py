import textwrap

from keyboards.button_texts import ButtonText


def get_hello_message(fullname, milgroup, post):
    return textwrap.dedent(f"""
            Здравия желаю, {fullname}.
            
            Взвод: {milgroup}.
            Должность: {post}.
            
            Нажмите кнопку "{ButtonText.LIST_MILGROUP.value}", чтобы вывести список студентов Вашего взвода.
        """)