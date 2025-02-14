- ## Установка виртуального окружения
### В проекте используется [менеджер пакетов uv](https://docs.astral.sh/uv/)
### Для создания, активации и установки зависимостей вводим команды:

`uv venv --python 3.12`

`source .venv/bin/activate ` (для unix систем)

`.venv\Scripts\activate.bat` (для win)

`uv sync`


- ## Запуск линтеров
- [Установка taskFile](https://taskfile.dev/installation/)
- после установки вызываем линтеры командой `task lint`

