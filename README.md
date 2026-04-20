# Детекция номеров на изображениях и автоматическое переименование файлов

Приложение для автоматического переименования фотографий по номеру,
обнаруженному на изображении с помощью модели детекции (YOLO).

## Возможности

- Полностью локальная работа (без интернета)
- Обработка папки с изображениями
- Поддержка JPEG и RAW
- Детекция ROI (YOLO)
- Детекция цифр (YOLO)
- Автоматическое переименование файлов:
  - дополнение номера до 4 разрядов (`7 → 0007`)
  - обработка дубликатов (`0025.jpg`, `0025_1.jpg`, ...)
  - номер не найден или низкая уверенность — префикс `!_`
- Генерация CSV-отчёта

---

## Как это работает

Приложение использует многоступенчатый pipeline обработки изображения:

1. **ROI Detection**
   - поиск области с номером

2. **Preprocessing**
   - подготовка изображения
   - нормализация
   - обрезка ROI (области с табличкой)

3. **Digits Detection**
   - детекция отдельных цифр

4. **Post-processing**
   - сборка номера
   - фильтрация
   - сортировка цифр
   - формирование итогового номера

7. **Renaming**
   - генерация нового имени файла
   - обработка конфликтов

---



## Установка

### Требования

Python 3.10 or 3.11
Интернет требуется только при установке зависимостей (~200 MB)

### Клонирование репозитория
```bash
git clone https://github.com/Selimankina/sefer_project

cd sefer 
```
### Установка и активация окружения, установка зависимостей
```bash
python3.10 -m venv .venv

Mac/Linux:
source .venv/bin/activate

Windows:
.venv\Scripts\activate 

cd sefer_project
pip install -r requirements.txt
```
### Загрузка моделей
```bash
cd sefer_project

mkdir -p models

curl -L -o models/roi_detector.pt \
https://github.com/Selimankina/sefer_project/releases/tag/v1.0/roi_detector.pt

curl -L -o models/digit_detector.pt \
https://github.com/Selimankina/sefer_project/releases/tag/v1.0/digit_detector.pt
```
## Запуск
```bash
python main.py <path_to_folder>
```
Пример:
```bash
python main.py data/input
```
## Результат

Файлы переименовываются в исходной папке.

Создаётся CSV-отчёт.

