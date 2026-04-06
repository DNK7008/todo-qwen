# Todo Telegram Web App

Простое приложение для управления задачами с возможностью загрузки фотоотчетов, разработанное специально для Telegram Web App.

## Функционал

### Основные возможности
- ✅ Создание и управление задачами
- ✅ Отслеживание статусов задач (Ожидает, В работе, Завершено)
- ✅ Загрузка неограниченного количества фотографий к задачам
- ✅ Персональные папки для фото каждого пользователя
- ✅ Фильтрация по отделам
- ✅ Фотогалерея со всеми загруженными изображениями
- ✅ Интеграция с Telegram (авторизация по номеру телефона)

### Роли пользователей
- Все пользователи могут создавать задачи
- Загружать фотоотчеты к задачам
- Менять статусы задач
- Просматривать галерею по отделам

## Технологии

- **Frontend**: React + Vite
- **UI**: Кастомные стили, оптимизированные для мобильных устройств
- **Telegram Integration**: Telegram WebApp SDK
- **State Management**: React Hooks (useState, useEffect)

## Установка и запуск

### Локальная разработка

```bash
# Установка зависимостей
npm install

# Запуск в режиме разработки
npm run dev

# Сборка для продакшена
npm run build
```

### Развертывание в Telegram

1. Создайте бота через @BotFather в Telegram
2. Получите токен бота
3. Настройте Web App URL через @BotFather:
   - `/newapp` → следуйте инструкциям
   - Укажите URL вашего приложения (https://your-domain.com)
4. Добавьте кнопку меню или inline-кнопку для запуска Web App

## Структура проекта

```
todo-telegram-app/
├── src/
│   ├── components/
│   │   ├── TaskList.jsx       # Список задач
│   │   ├── TaskForm.jsx       # Форма создания задачи
│   │   ├── PhotoGallery.jsx   # Галерея фотографий
│   │   └── *.css              # Стили компонентов
│   ├── utils/
│   │   └── telegram.js        # Утилиты Telegram WebApp
│   ├── App.jsx                # Главный компонент
│   ├── App.css                # Глобальные стили
│   ├── main.jsx               # Точка входа
│   └── index.css              # Базовые стили
├── index.html                 # HTML шаблон
├── package.json
└── vite.config.js
```

## Архитектура хранения фото

Фотографии хранятся на сервере в структуре:
```
/uploads/
  /users/
    /{user_id}/
      /photos/
        /task_{task_id}/
          - photo_1.jpg
          - photo_2.jpg
          ...
```

## Следующие шаги (Backend)

Для полноценной работы необходимо реализовать бэкенд:

1. **APIEndpoints**:
   - `POST /api/tasks` - создание задачи
   - `GET /api/tasks` - получение списка задач
   - `PUT /api/tasks/:id/status` - обновление статуса
   - `POST /api/tasks/:id/photos` - загрузка фото
   - `GET /api/users/:id/photos` - получение фото пользователя

2. **База данных**: PostgreSQL с таблицами:
   - users (id, telegram_id, phone, first_name, last_name, department)
   - tasks (id, title, description, status, department, created_by, created_at)
   - photos (id, task_id, user_id, file_path, uploaded_at)

3. **Аутентификация**: Валидация initData от Telegram

## Лицензия

MIT
