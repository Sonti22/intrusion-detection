# Инструкция по загрузке на GitHub

## Шаг 1: Подготовка проекта

Убедитесь, что все изменения закоммичены:

```powershell
cd C:\Users\mjmln\word-of-wisdom\intrusion-detection
git status
```

Если есть незакоммиченные изменения, добавьте их:

```powershell
git add .
git commit -m "описание изменений"
```

---

## Шаг 2: Создание репозитория на GitHub

### Вариант A: Через веб-интерфейс (рекомендуется для новичков)

1. Откройте https://github.com/new
2. Заполните форму:
   - **Repository name**: `intrusion-detection`
   - **Description**: `Video-based intrusion detection system with YOLO and restricted zone monitoring`
   - **Visibility**: 
     - **Public** - если хотите, чтобы код был открытым
     - **Private** - если хотите скрыть код
   - **НЕ** добавляйте README, .gitignore или LICENSE (они уже есть в проекте)
3. Нажмите **"Create repository"**

### Вариант B: Через GitHub CLI (если установлен)

```powershell
# Авторизоваться (если ещё не авторизованы)
gh auth login

# Создать репозиторий и загрузить код
gh repo create intrusion-detection --public --source=. --remote=origin --push
```

---

## Шаг 3: Подключение к GitHub

После создания репозитория на GitHub, выполните в PowerShell:

```powershell
cd C:\Users\mjmln\word-of-wisdom\intrusion-detection

# Замените YOUR_USERNAME на ваш GitHub username
git remote add origin https://github.com/YOUR_USERNAME/intrusion-detection.git

# Убедитесь, что ветка называется main
git branch -M main

# Загрузить код на GitHub
git push -u origin main
```

**Важно**: Замените `YOUR_USERNAME` на ваш реальный GitHub username!

**Пример**:
```powershell
git remote add origin https://github.com/mjmln/intrusion-detection.git
```

---

## Шаг 4: Авторизация

При первом `git push` GitHub попросит авторизоваться:

### Вариант 1: Personal Access Token (рекомендуется)

1. Перейдите: https://github.com/settings/tokens
2. Нажмите **"Generate new token"** → **"Generate new token (classic)"**
3. Задайте имя: `intrusion-detection-push`
4. Выберите срок действия (например, 90 дней)
5. Отметьте права: **`repo`** (полный доступ к репозиториям)
6. Нажмите **"Generate token"**
7. **Скопируйте токен** (он показывается только один раз!)
8. При `git push` используйте:
   - **Username**: ваш GitHub username
   - **Password**: вставьте скопированный токен

### Вариант 2: GitHub Desktop

Установите GitHub Desktop и используйте его для загрузки:
- https://desktop.github.com/

---

## Шаг 5: Проверка загрузки

После успешной загрузки:

```powershell
# Проверить подключённые remote-репозитории
git remote -v

# Проверить статус
git status

# Просмотреть историю коммитов
git log --oneline
```

Откройте ваш репозиторий в браузере:
```
https://github.com/YOUR_USERNAME/intrusion-detection
```

---

## Шаг 6: Настройка репозитория (опционально)

После загрузки на GitHub:

1. **Добавьте описание и теги**:
   - Откройте репозиторий на GitHub
   - Нажмите ⚙️ (Settings) или ✏️ (Edit) рядом с описанием
   - **Description**: `Video-based intrusion detection system with YOLO`
   - **Topics**: `yolo`, `opencv`, `intrusion-detection`, `computer-vision`, `python`, `video-analysis`, `security`

2. **Добавьте README бейджи** (опционально):
   Отредактируйте `README.md` и добавьте в начало:
   ```markdown
   ![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
   ![YOLO](https://img.shields.io/badge/YOLO-v8-orange.svg)
   ![OpenCV](https://img.shields.io/badge/OpenCV-4.12-green.svg)
   ```

---

## Решение проблем

### Проблема: "remote origin already exists"

**Решение**: Удалите старый remote и добавьте заново:
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/intrusion-detection.git
```

### Проблема: "Authentication failed"

**Решение**: 
- Используйте Personal Access Token вместо пароля
- Убедитесь, что токен имеет права `repo`

### Проблема: "Permission denied"

**Решение**:
- Проверьте, что репозиторий создан на GitHub
- Проверьте правильность username в URL
- Убедитесь, что используете HTTPS, а не SSH

### Проблема: "Large files" (если модель попала в репозиторий)

**Решение**: Модель `yolov8n.pt` должна быть в `.gitignore`. Если она уже закоммичена:
```powershell
git rm --cached yolov8n.pt
git commit -m "chore: remove model from git"
git push
```

---

## Быстрая команда (если репозиторий уже создан)

Если репозиторий уже создан на GitHub, просто выполните:

```powershell
cd C:\Users\mjmln\word-of-wisdom\intrusion-detection
git remote add origin https://github.com/YOUR_USERNAME/intrusion-detection.git
git push -u origin main
```

---

**Готово!** Ваш проект теперь на GitHub 🎉

