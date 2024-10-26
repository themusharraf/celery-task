# Celery Tasks
## celery yordamida vaqti oʻzgartiriladigan tasklarni qanday yozish haqida tushuntiraman.
Mana, celery yordamida vaqti oʻzgartiriladigan tasklarni qanday yozish haqida tushuntiraman.

### 1. Celery konfiguratsiyasini tayyorlash: Avval celeryni o‘rnatamiz:

```bash
pip install celery
pip install "celery[beat]"
pip install celery redis
```
Celery broker URL ni tekshiring: tasks.py faylingizda broker URL to'g'ri yozilganligiga ishonch hosil qiling:

```python
app = Celery('tasks', broker='redis://localhost:6379/0')

```
Keyin, loyiha uchun celery ilovasini yaratamiz, masalan, tasks.py faylida quyidagi kodni yozamiz:
```python
from celery import Celery
from datetime import timedelta
from celery.schedules import schedule


app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')


@app.task
def print_message():
    print("Salom, Musharraf")


app.conf.beat_schedule = {
    'print-every-3-seconds': {
        'task': 'tasks.print_message',
        'schedule': schedule(run_every=timedelta(seconds=3)),  # Har 3 soniyada bajariladi
    },
}

app.conf.timezone = 'Asia/Tashkent'

```
Bu yerda Celery dasturini yaratdik, broker sifatida redisni belgiladik. print_message esa vaqti oʻzgarib boruvchi oddiy task boʻlib, hozirgi vaqtni konsolga chiqaradi.

### 2. Celery worker ishini boshlash: Bu komanda yordamida worker'ni ishga tushiramiz:

```bash
celery -A tasks worker --loglevel=info

```

### 3.Celery Beatni ishga tushirish:

```bash

celery -A tasks beat --loglevel=info
````
Shunday qilib, print_message taskimiz har 5 daqiqada bajariladi. Bu usul bilan celery yordamida kerakli vaqtda yoki periodik interval bilan tasklarni bajarishimiz mumkin.


### Task holatini tekshirish
Task holatini tekshirish uchun `AsyncResult` yordamida task holatini kuzatishingiz mumkin:

```python
from celery.result import AsyncResult

# Tasdiqlash uchun task_id
task_id = "d45990fe-c5a3-4d26-a528-d005f92e7de6"

# Task natijasi
result = AsyncResult(task_id)
print("Status:", result.status)  # holati
print("Result:", result.result)  # natijasi, task tugagan bo'lsa natija chiqadi
```
### Worker loglariga qarab ko'rish
Agar celeryni --loglevel=info bilan ishga tushirgan bo'lsangiz, task bajarilgandan keyin worker logida taskning natijasini ko'rishingiz mumkin.

### Task natijalarini Redis’da saqlash
Agar task natijalarini Redis’da saqlamoqchi bo‘lsangiz, celery konfiguratsiyasiga backendni qo‘shishingiz mumkin:

```python
app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
```
Bu bilan, Celery avtomatik ravishda Redis’da task natijasini saqlaydi va uni `AsyncResult` orqali olish mumkin bo'ladi.


Redis’ni Docker orqali olish va ishga tushirish juda oddiy. Quyidagi qadamlarni bajaring:

Redis image’ni olish:

bash
Copy code
docker pull redis
Bu buyruq Docker Hub’dan Redis image’ni yuklab oladi.

Redis konteynerini ishga tushirish:

Oddiy Redis serverni ishlatish uchun quyidagi buyruqdan foydalaning:

bash
Copy code
docker run --name my-redis -d redis
Bu yerda:

--name my-redis – konteyner nomini my-redis deb belgilaydi.
-d – konteynerni “detached” rejimda (fonda) ishlatadi.
Redis server uchun maxsus portni ochish (masalan, 6379):

Agar konteyneringizni serveringizga yoki mahalliy tarmoqqa ulashni xohlasangiz, Redis portini ochishingiz mumkin:

bash
Copy code
docker run --name my-redis -p 6379:6379 -d redis
Bu Redis serverini mahalliy 6379-port orqali ochadi va u orqali redis-cli yoki boshqa Redis mijozi bilan ulanish mumkin bo‘ladi.

Redis bilan ulanish:

Konteyner ichida Redis bilan ulanish uchun quyidagi buyruqdan foydalanishingiz mumkin:

```bash
docker exec -it my-redis redis-cli
```
Bu sizni Redis CLI ichiga olib kiradi, va bu yerdan Redis buyruqlarini yuborishingiz mumkin.

Redis’ni Docker orqali ishlatish shunday sodda!