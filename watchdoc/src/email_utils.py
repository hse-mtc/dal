import email.header
from email.mime.text import MIMEText

from config import EMAIL_HOST_USER, EMAIL_FROM_NAME


def create_message(to, link):
    mec_link = "https://www.hse.ru/org/hse/ouk/mil/"
    student_centre_link = "https://studentcentre.hse.ru/#contacts"

    message = MIMEText(
        _text="<p>Здравствуйте!</p>\n"
        
        "<p>Вы заполнили форму для поступления в ВУЦ.</p>\n"
        
        "<p>Автоматически сгенерированные документы, которые понадобятся Вам на"
        f" различных этапах отбора, находятся по ссылке: <a href=\"{link}\">{link}</a></p>\n"
        
        "Имейте в виду, что:\n"
              
        "<ul>\n"
              
        "<li>Папка с документами может не сразу отобразить содержимое – "
        "в такой ситуации следует подождать несколько минут.</li>\n"
        
        "<li>Все места, где нужно указать номер и название военно-учебной "
        "специальности, намеренно оставлены пустыми. Это сделано для того, "
        "чтобы Вы могли заполнить их карандашом и позже исправить.</li>\n"
        
        "<li>В случае, если военный комиссариат откажется принимать подписанную"
        " версию направления, Вам необходимо посетить Центр сервиса "
        f"<a href=\"{student_centre_link}\">\"Студент\"</a> (Покровский бульвар, 11) "
        "и получить подписанное направление в военный комиссариат (и самостоятельно "
        "заполнить графы Военному комиссару, ФИО, год рождения и заявление студента) "
        "по образцу, который Вам пришел на почту, или с неподписанной версией прийти в ВУЦ, "
        "чтобы на документ поставили все необходимые печати и подписали от руки.</li>\n"
        
        "<li>Во втором пункте медкарты необходимо указать фактический адрес "
        "проживания, который в форме не собирается, – заполните его "
        "самостоятельно.</li>\n"
              
        "<li>В карточке для выбора физ. упражнения напротив поля «д.р, возраст» "
        "укажите в скобках количество полных лет справа от даты рождения (например, 19 лет). "
        "Далее выберите одно упражнение из каждой категории и "
        "подчеркните его.</li>\n"
        
        "</ul>\n\n"
              
        "<p>Вся важная информация о поступлении публикуется на официальной "
        f" странице ВУЦ на сайте ВШЭ: <a href=\"{mec_link}\">{mec_link}</a></p>"
              
        "<p>Успехов на медкомиссии и отборочных испытаниях!</p>",
        _subtype="html",
    )

    message["to"] = to
    from_header = email.header.Header(EMAIL_FROM_NAME, "ascii")
    from_header.append(f"<{EMAIL_HOST_USER}>")
    message["from"] = from_header
    message["subject"] = "Поступление в Военный учебный центр"
    return message.as_string()
