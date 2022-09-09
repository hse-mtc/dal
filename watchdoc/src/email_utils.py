import email.header
from email.mime.text import MIMEText

from config import EMAIL_HOST_USER, EMAIL_FROM_NAME


def create_message(to, link):
    mec_link = "https://www.hse.ru/org/hse/ouk/mil/"

    message = MIMEText(
        _text="<p>Здравствуйте!</p>\n"
        
        "<p>Вы заполнили форму для поступления в ВУЦ.</p>\n"
        
        "<p>Автоматически сгенерированные документы, которые понадобятся Вам на"
        f" различных этапах отбора, находятся по ссылке: {link} </p>\n"
        
        "Имейте в виду, что:\n"
              
        "<ul>\n"
              
        "<li>Папка с документами может не сразу отобразить содержимое – "
        "в такой ситуации следует подождать несколько минут.</li>\n"
        
        "<li>Все места, где нужно указать номер и название военно-учебной "
        "специальности, намеренно оставлены пустыми. Это сделано для того, "
        "чтобы Вы могли заполнить их карандашом и позже исправить.</li>\n"
        
        "<li>В случае, если военный комиссариат откажется принимать подписанную"
        " версию направления, Вам необходимо посетить ВУЦ с неподписанной "
        " версией, чтобы на документ поставили все необходимые печати и "
        "подписали от руки.</li>\n"
        
        "<li>Во втором пункте медкарты необходимо указать фактический адрес "
        "проживания, который в форме не собирается, – заполните его "
        "самостоятельно.</li>\n"
        
        "</ul>\n\n"
              
        "<p>Вся важная информация о поступлении публикуется на официальной "
        f" странице ВУЦ на сайте ВШЭ: {mec_link}</p>"
              
        "<p>Успехов на медкомиссии и отборочных испытаниях!</p>",
        _subtype="html",
    )

    message["to"] = to
    from_header = email.header.Header(EMAIL_FROM_NAME, "ascii")
    from_header.append(f"<{EMAIL_HOST_USER}>")
    message["from"] = from_header
    message["subject"] = "Поступление в Военный учебный центр"
    return message.as_string()
