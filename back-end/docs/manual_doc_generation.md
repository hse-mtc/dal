# Ручная генерация документов для абитуриентов

## Обзор

Django management command для ручной генерации документов для выбранных абитуриентов через back-end сервис.

## Расположение

```
back-end/src/ams/management/commands/generate_applicant_docs.py
```

## Требования

1. Python 3.10+
2. Установленные зависимости back-end (Pipfile)
3. Настроенные переменные окружения (см. `back-end/.env.example`)
4. Запущенный сервис watchdoc

## Использование

### Запуск из директории back-end

```bash
cd back-end

# Для одного абитуриента
python manage.py generate_applicant_docs --email student@hse.ru

# Для нескольких абитуриентов
python manage.py generate_applicant_docs --email student1@hse.ru --email student2@hse.ru

# Из файла со списком email
python manage.py generate_applicant_docs --emails-file students.txt

# Тестовый запуск (без реальной генерации)
python manage.py generate_applicant_docs --email student@hse.ru --dry-run
```

### Запуск в Docker контейнере

```bash
docker compose -f dev-dc.yaml run back-end python manage.py generate_applicant_docs --email student@hse.ru
```

## Параметры командной строки

| Параметр | Краткий | Описание |
|----------|---------|----------|
| `--email` | `-e` | Email абитуриента (можно указывать несколько раз) |
| `--emails-file` | `-f` | Путь к файлу со списком email (один на строку) |
| `--dry-run` | | Тестовый запуск без реальной генерации документов |

## Формат файла со списком email

Файл должен содержать один email на строку. Строки начинающиеся с `#` считаются комментариями:

```
# Список абитуриентов для генерации документов
student1@hse.ru
student2@hse.ru
# student3@hse.ru - временно отложен
student4@hse.ru
```

## Как это работает

1. Скрипт ищет абитуриентов в базе данных по указанным email
2. Для каждого найденного абитуриента вызывается функция `generate_documents_for_applicant()`
3. Данные абитуриента сериализуются и отправляются POST-запросом на watchdoc сервис (`/applicants/`)
4. Watchdoc генерирует документы и загружает их на Яндекс.Диск
5. Абитуриент получает уведомление на email со ссылкой на документы

## Примеры использования

### Пример 1: Генерация для одного абитуриента

```bash
cd back-end
python manage.py generate_applicant_docs --email ivanov@hse.ru
```

### Пример 2: Массовая генерация из файла

```bash
cd back-end
python manage.py generate_applicant_docs -f new_applicants.txt
```

### Пример 3: Проверка перед генерацией

```bash
cd back-end
python manage.py generate_applicant_docs -e student1@hse.ru -e student2@hse.ru --dry-run
```

## Вывод команды

После выполнения скрипт выводит:
- Список найденных абитуриентов
- Статус генерации для каждого абитуриента (✓ успешно / ✗ ошибка)
- Итоговую статистику: успешно, ошибок, не найдено

```
Starting document generation for 2 applicant(s)...
Found 2 applicant(s) for document generation
Processing: Иванов Иван Иванович (ivanov@hse.ru)...
  ✓ Documents generated successfully
Processing: Петров Пётр Петрович (petrov@hse.ru)...
  ✓ Documents generated successfully

==================================================
Generation complete:
  Successful: 2
  Failed: 0
  Not found: 0
==================================================
```

## Устранение неполадок

### Ошибка: "No applicants found for the specified emails"

Убедитесь, что абитуриенты с указанными email существуют в базе данных.

### Ошибка: "Connection refused" при генерации

Убедитесь, что сервис watchdoc запущен и доступен по адресу, указанному в `WATCHDOC_HOST` и `WATCHDOC_PORT`.

### Ошибка: "YADISK_TOKEN not set"

Установите переменную окружения `YADISK_TOKEN` в настройках watchdoc.
