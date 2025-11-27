# 🚀 Быстрый старт - пошаговая инструкция

## ⚡ Краткая версия (для опытных)

```powershell
# 1. Активация окружения
cd C:\Users\mjmln\word-of-wisdom\intrusion-detection
.venv\Scripts\Activate.ps1

# 2. Установка зависимостей (если ещё не установлены)
pip install -r requirements.txt

# 3. Поместите test.mp4 в папку data/

# 4. Разметка зоны
python -m src.tools.mark_restricted_zone

# 5. Запуск детекции
python -m src.main
```

---

## 📋 Детальная версия (для новичков)

### ШАГ 1: Откройте PowerShell

Нажмите `Win + X` → выберите "Windows PowerShell" или "Терминал"

### ШАГ 2: Перейдите в папку проекта

```powershell
cd C:\Users\mjmln\word-of-wisdom\intrusion-detection
```

**Проверка**: Вы должны увидеть путь в строке PowerShell

### ШАГ 3: Активируйте виртуальное окружение

```powershell
.venv\Scripts\Activate.ps1
```

**Ожидаемый результат**: В начале строки появится `(.venv)`

**Если ошибка "execution policy":**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Затем снова активируйте окружение.

### ШАГ 4: Установите зависимости

```powershell
pip install -r requirements.txt
```

**Что происходит:**
- Устанавливаются: ultralytics, opencv-python, numpy
- При первом запуске YOLO скачает модель (~6 МБ)
- Время: 2-5 минут

**Проверка установки:**
```powershell
python -c "import ultralytics; print('OK')"
```

### ШАГ 5: Подготовьте тестовое видео

**Вариант A: Через Проводник**
1. Откройте папку: `C:\Users\mjmln\word-of-wisdom\intrusion-detection\data`
2. Скопируйте ваш видеофайл туда
3. Переименуйте в `test.mp4`

**Вариант B: Через PowerShell**
```powershell
# Замените путь на реальный путь к вашему видео
Copy-Item "C:\путь\к\вашему\видео.mp4" -Destination "data\test.mp4"
```

**Проверка:**
```powershell
Test-Path data\test.mp4
```
Должно вернуть `True`

### ШАГ 6: Разметьте запрещённую зону

```powershell
python -m src.tools.mark_restricted_zone
```

**Что делать в открывшемся окне:**

1. **Кликните мышью** по углам зоны, которую хотите отметить
   - Каждый клик = новая точка (зелёный кружок)
   - Точки соединяются жёлтой линией

2. **Сохраните зону**: Нажмите клавишу `s`
   - Зона сохранится в `restricted_zones.json`
   - Окно закроется

3. **Если ошибка**: Нажмите `r` для сброса, начните заново

**Минимум точек**: 3 (для треугольника)

**Проверка сохранения:**
```powershell
Get-Content restricted_zones.json
```
Должен быть JSON с массивом зон.

### ШАГ 7: Запустите систему детекции

```powershell
python -m src.main
```

**Что вы увидите:**

- ✅ Окно с видео
- ✅ Жёлтые линии = границы зон
- ✅ Зелёные прямоугольники = детектированные люди
- ✅ Синие точки = центры детекций
- ✅ Красная надпись "ALARM!" = активная тревога

**Управление:**
- `q` или `ESC` = выход

**Поведение:**
- Тревога загорается, когда человек входит в зону
- Тревога гаснет через 3 секунды после выхода человека

---

## ✅ Чек-лист перед запуском

Отметьте выполненные пункты:

- [ ] PowerShell открыт
- [ ] Перешёл в папку `intrusion-detection`
- [ ] Активировал виртуальное окружение (вижу `(.venv)`)
- [ ] Установил зависимости (`pip install -r requirements.txt`)
- [ ] Поместил `test.mp4` в папку `data/`
- [ ] Разметил зону через `python -m src.tools.mark_restricted_zone`
- [ ] Проверил, что `restricted_zones.json` содержит зону

**Если все пункты отмечены → запускайте `python -m src.main`!**

---

## 🐛 Решение проблем

### Проблема: "Cannot open video"
**Решение**: Проверьте, что файл `data\test.mp4` существует:
```powershell
Test-Path data\test.mp4
```

### Проблема: "No restricted zones defined"
**Решение**: Запустите разметку:
```powershell
python -m src.tools.mark_restricted_zone
```

### Проблема: "ModuleNotFoundError"
**Решение**: Активируйте окружение:
```powershell
.venv\Scripts\Activate.ps1
```

### Проблема: Медленная работа
**Решение**: Это нормально на CPU. Для ускорения нужен GPU с CUDA.

---

## 📚 Дополнительная информация

- **Детальная инструкция**: См. `SETUP_GUIDE.md`
- **Описание проекта**: См. `README.md`
- **Настройка параметров**: Отредактируйте `src/config.py`

---

**Готово! Удачи! 🎉**

