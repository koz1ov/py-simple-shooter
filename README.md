# py-simple-shooter

### Задача
Написать простой 3d шутер c ray-casting рендерингом

### Используемые модули
PySDL2 и/или PyGame \
Numpy или что-то другое для математики

### Примерный интерфейс

![Screenshot from 2022-03-22 22-40-02](https://user-images.githubusercontent.com/30055878/159562402-d8b10714-677a-4200-b7e1-9ca9becfe703.png)

### Правила игры
Задача игрока за ограниченное время уничтожить наибольшее количество противников. В конце игры появляется счет с количеством пораженных противников.

### Построенный геймплэй

![](docs/_static/game.gif)

### Зависимости
1. pydantic 
2. pygame

### Использование модуля в директории проекта
```bash
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
python3 -m shooter
```


### Создание дистрибутиа и исходных файлов
```bash
python3 -m venv env
source env/bin/activate
pip3 install -r requirements-dev.txt
doit wheel
```
В папке dist будут лежать whl-дистрибутив и архив с исходниками
### Установка whl-дистрибутива
```bash
python3 -m venv env
source env/bin/activate
pip3 install path/to/shooter-0.0.1-py3-none-any.whl
```

### Интерфейс запуска игры с установленным дистрибутивом в текущее окружение
```bash
python3 -m shooter
```
или
```bash
shooter
```