# Telegram Todo App - Инструкция по запуску

Приложение для управления задачами с загрузкой фотографий через Telegram Web App.

## 📋 Требования

- Docker (версия 20.10+)
- Docker Compose (версия 2.0+)
- Git

## 🚀 Быстрый старт

### Шаг 1: Клонирование и подготовка

```bash
cd telegram-todo-app
```

### Шаг 2: Настройка переменных окружения

Скопируйте шаблон файла настроек:

```bash
cp .env.example .env
```

**Важно!** Откройте файл `.env` и замените `YOUR_BOT_TOKEN_HERE` на реальный токен вашего Telegram бота:

```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
```

#### Как получить токен бота:
1. Откройте Telegram и найдите бота **@BotFather**
2. Отправьте команду `/newbot`
3. Введите имя и username для бота
4. Скопируйте полученный токен и вставьте в файл `.env`

### Шаг 3: Запуск приложения

Запустите все сервисы одной командой:

```bash
docker-compose up --build
```

Первый запуск может занять 2-5 минут (скачивание образов, сборка контейнеров).

### Шаг 4: Проверка работы

После запуска проверьте доступность сервисов:

- **Фронтенд (Web App)**: http://localhost:3000
- **Бэкенд (API)**: http://localhost:8000
- **Документация API**: http://localhost:8000/docs

## 🔧 Управление приложением

### Остановка приложения

```bash
docker-compose down
```

### Остановка с удалением данных

```bash
docker-compose down -v
```

⚠️ **Внимание**: Эта команда удалит базу данных и все загруженные файлы!

### Перезапуск

```bash
docker-compose restart
```

### Просмотр логов

```bash
# Все логи
docker-compose logs -f

# Лог конкретного сервиса
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### Обновление приложения

Если вы внесли изменения в код:

```bash
docker-compose up --build -d
```

## 📱 Интеграция с Telegram

### Настройка Web App в боте

1. Откройте @BotFather в Telegram
2. Отправьте команду `/mybots`
3. Выберите вашего бота
4. Нажмите **Bot Settings** → **Menu Button** → **Configure Menu Button**
5. Отправьте ссылку на ваш Web App:
   - Для локальной разработки: используйте туннель (ngrok) или деплой на сервер
   - Для продакшена: `https://your-domain.com`

### Пример ссылки для локальной разработки

Используйте ngrok для открытия доступа к фронтенду:

```bash
# В новом терминале
ngrok http 3000
```

Скопируйте полученную HTTPS ссылку и укажите её в настройках бота.

## 🏗 Архитектура проекта

```
telegram-todo-app/
├── frontend/          # React приложение (Telegram Web App)
│   ├── src/
│   │   ├── components/
│   │   ├── utils/
│   │   └── App.jsx
│   └── Dockerfile
├── backend/           # FastAPI сервер
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
│   └── Dockerfile
├── docker-compose.yml # Оркестрация контейнеров
├── .env              # Переменные окружения
├── .env.example      # Шаблон переменных
├── init.sql          # Скрипт инициализации БД
└── README.md         # Этот файл
```

## 💾 Хранение данных

Данные сохраняются в Docker volumes:

- **postgres_data**: база данных PostgreSQL
- **uploads_data**: загруженные фотографии

Пути на хосте (для бэкапа):
```bash
docker volume inspect telegram-todo-app_postgres_data
docker volume inspect telegram-todo-app_uploads_data
```

## 🔐 Безопасность

Перед развертыванием на продакшене:

1. Измените `SECRET_KEY` в файле `.env` на случайную строку
2. Установите сложные пароли для базы данных
3. Используйте HTTPS для подключения к Web App
4. Ограничьте доступ к API только для вашего домена

## 🛠 Разработка

### Запуск в режиме разработки

#### Фронтенд:
```bash
cd frontend
npm install
npm run dev
```

#### Бэкенд:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Тестирование API

Откройте http://localhost:8000/docs для интерактивной документации Swagger UI.

## ❓ Решение проблем

### Контейнер не запускается
```bash
docker-compose logs <имя_сервиса>
```

### Ошибки базы данных
```bash
docker-compose down -v
docker-compose up --build
```

### Порт уже занят
Измените порты в `docker-compose.yml`:
```yaml
ports:
  - "3001:80"  # вместо 3000
```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи: `docker-compose logs -f`
2. Убедитесь, что Docker запущен
3. Проверьте файл `.env` на корректность

---

**Версия**: 1.0.0  
**Лицензия**: MIT
