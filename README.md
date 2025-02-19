# Содержание
1. [Установка виртуального окружения](#установка-виртуального-окружения)
2. [Запуск в контейнере](#запуск-в-docker)
3. [Запуск линтеров](#запуск-линтеров)
### Установка виртуального окружения
#### В проекте используется [менеджер пакетов uv](https://docs.astral.sh/uv/)
#### Для создания, активации и установки зависимостей вводим команды:

```bash
uv venv --python 3.12
```
(для unix систем)
```bash
source .venv/bin/activate
```
(для win)
```bash
.venv\Scripts\activate.bat
``` 

```bash
uv sync
```
### Запуск в docker
#### В проекте на текущий момент реализован деплой средствами docker compose. Это уже все преднастроено для запуска на локале разработчика. Для запуска достаточно ввести команду находять в корне приложения
```bash
docker compose up --build
```
#### При запуске автоматически поднимется база и контейнер с API и будет доступен по адресу `localhost:8000/schema/swagger#`.

### Запуск линтеров
- [Установка taskFile](https://taskfile.dev/installation/)
- после установки вызываем линтеры командой `task lint`

