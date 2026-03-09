#!/bin/bash
set -e

REPO_NAME=$1
REPO_URL=$2
COMMIT_SHA=$3

git clone "$REPO_URL" "/repositories/$REPO_NAME"
cd "/repositories/$REPO_NAME"
git reset --hard "$COMMIT_SHA"
```

4. Нажми **Commit changes**

---

Потом создай ещё один файл:

1. **Add file** → **Create new file**
2. Имя файла: `builder/requirements.txt`
3. Вставь:
```
runpod
