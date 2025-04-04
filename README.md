# Moskovskiy.chess
Very good chess by greatest Kirill Moskovskiy TRPO24-1
# Шахматный симулятор и шашки: объектно-ориентированная версия

Этот проект представляет собой консольное приложение на Python, которое позволяет играть как в шахматы, так и в шашки. Приложение включает такие возможности, как история ходов с функциями отмены (undo) и повтора (redo), подсказки для возможных ходов, анализ угроз, а также сохранение и загрузка партий. Кроме того, поддерживаются уникальные шахматные фигуры: Волшебник, Дракон и Стрелок.

## Содержание репозитория

- **chesss.py** – основной файл с кодом, содержащий реализацию логики игры, доски, фигур и игрового процесса.
- **documentation.txt** – подробная документация проекта.
- **requirements.txt** – список зависимостей (пустой, используются только стандартные библиотеки Python).
- **README.md** – данный файл.

## Описание проекта

### Основной функционал

- **Режим игры в шахматы:**  
  Игра на стандартной доске 8×8. Игроки вводят ходы в стандартной шахматной нотации (например, `e2 e4`), а программа проверяет корректность ходов согласно правилам шахмат.

- **Режим игры в шашки:**  
  Поддержка шашек реализована через параметр `game_type` доски и отдельные классы для обычных шашек и дамок.

- **История ходов:**  
  Все ходы сохраняются, что позволяет отменять (`back`) и повторять (`next`) ходы.

- **Подсказки:**  
  Команда `hint <позиция>` (например, `hint e2`) отображает все возможные ходы для фигуры на указанной клетке с визуальной подсветкой.

- **Анализ угроз:**  
  Команда `threats <позиция>` (например, `threats e4`) показывает, какие фигуры противника могут атаковать данную клетку.

- **Сохранение и загрузка партии:**  
  Команды `save <имя_файла>` и `load <имя_файла>` позволяют сохранять историю ходов в файл и загружать партии.

### Дополнительные возможности

- **Уникальные шахматные фигуры:**
  - **Волшебник (w/W):** Комбинирует ходы коня и короля.
  - **Дракон (d/D):** Сочетает ходы ладьи и коня.
  - **Стрелок (a/A):** Ходит как слон или «выстреливает» диагонально на две клетки, атакуя фигуры противника.

- **Фигуры для шашек:**
  - **Шашка (Checker):** Ходит по диагонали вперёд, захватывая фигуры прыжком.
  - **Дамка (KingChecker):** Ходит по диагонали в любом направлении, захватывая фигуры прыжком.

## Установка и запуск

### Требования

- Python версии 3.6 или выше.
- Дополнительных библиотек не требуется, используется только стандартная библиотека Python.

### Как запустить игру

1. Склонируйте или скачайте репозиторий.
2. Откройте терминал в директории проекта.
3. Запустите игру командой:

   ```bash
   python chesss.py
При появлении запроса выберите режим игры:

Введите 1 для игры в шахматы.

Введите 2 для игры в шашки.

Следуйте инструкциям, выводимым на экран. Примеры команд:

Ход: e2 e4

Отмена хода: back

Повтор хода: next

Подсказка: hint e2

Анализ угроз: threats e4

Сохранение партии: save game.txt

Загрузка партии: load game.txt

Выход: exit





