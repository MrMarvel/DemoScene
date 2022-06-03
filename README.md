# DemoScene
Пародия на дему-сцену

## Первый запуск
Запустить в консоли python setup.py install для установки пакета.
> `py -m demoscene-mrmarvel` Запустить приложение

## Документация
Для генерации документации по проекту в консоли ввести в папке проекта:
> `sphinx-apidoc -f -o ./docs/source ./src src -T -l -a`

Далее нужно выполнить следующую команду:
> `.docs/make.bat html`

## Зависимости
| Modules        | Version |
|----------------|:-------:|
| cursor         |         |
| numpy          |         |
| windows-curses |         |
| fps-limiter    |         |