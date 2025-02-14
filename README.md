- ## Установка виртуального окружения
### В проекте используется [менеджер пакетов uv](https://docs.astral.sh/uv/)
### Для создания, активации и установки зависимостей вводим команды
```commandline
uv venv --python 3.12

(для unix систем)
source .venv/bin/activate 

(для win)
.venv\Scripts\activate.bat

uv sync
```

- ## Запуск линтеров
- [Установка taskFile](https://taskfile.dev/installation/)
- после установки вызываем линтеры командой
```commandline
task lint
```
