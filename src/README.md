
پروژه شبیه‌سازی توئیتر

#### نیازمندی ها

* Django
* djangorestframework
* markdown
* django-filter
* djangorestframework_simplejwt
* django-redis
* PyJWT
* psycopg2
* gunicorn

###### شرح پروژه
در حال حاضر پروژه دارای امکانات زیر است:
* تعریف کاربر و دریافت توکن برای انجام عملیات بعدی
* لاگین کاربر با نام کاربری و رمز عبور و دریافت توکن برای انجام عملیات بعدی
* ایجاد توئیت
* ویرایش توئیت توسط ایجاد کننده آن
* حذف توئیت توسط ایجاد کننده آن
* امکان قرار دادن کامنت روی توئیت ها
* دریافت لیست توئیت های یک کاربر
* دریافت لیست کامنت های یک توئیت
* دریافت لیست همه توئیت ها براساس زمان آخرین تغییر
* امکان دریافت توکن توسط کاربر جهت دسترسی دادن به افراد و برنامه های ثالث

#### نحوه اجرا 
برای اجرای پروژه دستورهای زیر را در مسیر root پروژه اجرا کنید.
docker-compose build
docker-compose run web python manage.py makemigrations tweets
docker-compose run web python manage.py makemigrations accounts
docker-compose run web python manage.py migrate
docker-compose up