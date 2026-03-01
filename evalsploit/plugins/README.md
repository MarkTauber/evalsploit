# Плагины evalsploit

Плагины - это Python-модули в этой папке. При старте evalsploit подгружает все `*.py` (кроме начинающихся с `_`). Каждый плагин регистрирует свою команду и при вызове получает контекст и аргументы.

## Стандарт плагина (ГОСТ)

1. **Один файл** - один модуль, одна команда (имя команды = имя файла без `.py` не обязательно; можно зарегистрировать любое имя).
2. **Импорты:** из `evalsploit.modules.registry` - `register`; из `evalsploit.modules.base` - `Module`.
3. **Регистрация:** декоратор `@register("имя_команды", description="...", usage="...")`. `description` и `usage` опциональны (попадут в `help`).
4. **Класс:** наследуется от `Module`, реализует `run(self, ctx, args) -> Optional[str]`:
   - `ctx` - сессия (ctx.send(php), ctx.config, ctx.pwd, ctx.resolve_path(path) и т.д.).
   - `args` - строка: всё, что пользователь ввёл после имени команды (параметры разбирать самим).
5. **Поведение:** по желанию печатать через `print()`, возвращать `None` или строку. Не падать на исключениях без обработки - лучше вывести сообщение и вернуть `None`.

## Пример минимального плагина

```python
from evalsploit.modules.registry import register
from evalsploit.modules.base import Module

@register("mycmd", description="Краткое описание", usage="mycmd [path]")
class MyCmdModule(Module):
    def run(self, ctx, args):
        path = ctx.resolve_path(args.strip()) if args.strip() else ctx.pwd
        php = "echo getcwd();"  # пример
        print(ctx.send(php))
        return None
```

Файл сохранить как `mycmd.py` в папке `evalsploit/plugins/`. После следующего запуска команда `mycmd` появится в списке и в `help`.
