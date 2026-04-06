# Todo Telegram App Backend

Backend для системы управления задачами с интеграцией Telegram Web App.

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Настройте переменные окружения в файле `.env`:
```
DATABASE_URL=sqlite+aiosqlite:///./todo.db
SECRET_KEY=your-secret-key-change-in-production
UPLOAD_DIR=./uploads
STATIC_DIR=./static
```

3. Запустите сервер:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

- `POST /api/auth` - Авторизация/регистрация пользователя
- `GET /api/tasks` - Получить список задач
- `POST /api/tasks` - Создать задачу
- `PUT /api/tasks/{task_id}/status` - Обновить статус задачи
- `POST /api/photos/upload` - Загрузить фото
- `GET /api/photos` - Получить список фото

## Структура проекта

```
todo-backend/
├── app/
│   ├── api/          # API роуты
│   ├── core/         # Конфигурация
│   ├── models/       # Модели данных
│   ├── schemas/      # Pydantic схемы
│   └── services/     # Бизнес логика
├── static/           # Статические файлы
├── uploads/          # Загруженные фото
├── main.py           # Точка входа
└── requirements.txt  # Зависимости
```

## Интеграция с фронтендом

Фронтенд должен отправлять данные пользователя Telegram через форму:
- telegram_id
- phone
- full_name
- department (опционально)

Фото пользователей сохраняются в папке `/uploads/{user_id}/`
