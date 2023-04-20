# apiQR
Это микросервис для генирации qr-кодов на оплату в банках по реквизитам получателя.
На текущий момент работает на `qr-api.xlombard.ru:48855`
Пример генерации:
`http://qr-api.xlombard.ru:48855/v1/?token=6F9619FF-8B86-D011-B42D-00CF4FC964FF&Name=ООО+Ломбард+автомобильный+«Залог+24»&PersonalAcc=40702810403000036124&BankName=ПАО+"ПРОМСВЯЗЬБАНК"&PayeeINN=5254492098&KPP=770345001&BIC=042202803&CorrespAcc=30101810700000000803&Sum=50000&Purpose=Оплата+по+договору+№ЛА+№000567%2C+Кирбашян+Валерий+Ашотович&size=500`
Пример получения:
`http://qr-api.xlombard.ru:48855/result/6F9619FF-8B86-D0/2023-04-20/5f2bd98c-df9d-11ed-95c5-5cb901fe8117.png`

## Этапы установки

1. Загрузите и установите Apache 2.4 в папку C:/Apache24 (https://www.apachelounge.com/download/)

2. Установить Microsoft C++ Build Tools(https://visualstudio.microsoft.com/visual-cpp-build-tools/)

3. Установить `Python` (создавать виртуальное окружение не нужно)

4. Установить `Django==3.2`, `djangorestframework==3.12.4`,`Pillow`, `qrcode`, `uuid`, `modwsgi` (файл `requirements.bat`)

5. В терминале выполнить `mod_wsgi-express module-config`, после скопировать полученные данные и изменить `httpd.conf.template`.
Так же изменить `WSGIScriptAlias` на путь к `wsgi.py`.
`WSGIPythonPath` на путь расположения `manage.py`.
`<Directory "D:/apiQR/apiQR/apiQR/">` изменить на путь расположения `wsgi.py`.
`ServerName 192.145.97.71:48855` изменить на соотвествующие данные.
В `Apache24/conf/httpd.conf` изменить `Listen 48855` на нужный порт.
Полученный конфиг `httpd.conf.template` вставить(заменить) в конце файла `Apache24/conf/httpd.conf`.
В файле `Apache24/conf/httpd.conf` заменить:
<Directory />
    Options FollowSymLinks
    AllowOverride None
    Order deny,allow
    Deny from all
</Directory>

на

<Directory />
    Options Indexes FollowSymLinks Includes ExecCGI
    AllowOverride All
    Require all granted
</Directory>

Дописать в конец
Alias "/result" "D:/apiQR/result/"
<Directory "D:/apiQR/result/">
    AllowOverride All
    Require all granted
</Directory>
указав путь к папке расположения сохранения qr кодов.

7. В `apiQR/apiQR/settings.py` заменить `PATH_DIR_QR` на желаемый путь сохранения qr кодов.

## Примеры и требования запросов
### Запрос на создание
`domen/v1?params`
Возможны следующие параметры:
1. `Name` - Наименование получателя платежа (Обязательно)
2. `PersonalAcc` - Номер счета получателя платежа (Обязательно)
3. `BankName` - Наименование банка получателя платежа (Обязательно)
4. `BIC` - БИК (Обязательно)
5. `CorrespAcc` - Номер кор. счета банка получателя платежа (Обязательно)
6. `Sum` - Сумма платежа, в копейках
7. `Purpose` - Наименование платежа (назначение)
8. `PayeeINN` - ИНН получателя платежа
9. `PayerINN` - ИНН плательщика
10. `KPP` - КПП получателя платежа
11. `size` - размер qr кода, в пикселях (по умолчанию 800)
12. `folder` - папка сохранения qr кода, относительно папки `token`

Все qr коды сохраняются в папку `result/token/folder(при указании)/date/`.

Ответ запроса - путь к сохраненному qr коду.

`Примеры:`
1. `domen/v1?token=6F9619FF-8B86-D011-B42D-00CF4FC964FF&Name=ООО+Ломбард+автомобильный+«Залог+24»&PersonalAcc=40702810403000036124&BankName=ПАО+"ПРОМСВЯЗЬБАНК"&PayeeINN=5254492098&KPP=770345001&BIC=042202803&CorrespAcc=30101810700000000803&Sum=50000&Purpose=Оплата+по+договору+№ЛА+№000567%2C+Кирбашян+Валерий+Ашотович&size=200&folder=asd`

### Запрос на получение
`domen/{путь к qr переданный в ответ на запрос создания}`

`Примеры:`
1. `domen/result/7A9619FF-8B86-D0/2023-03-19/913db945-c64e-11ed-9a80-5cb901fe8117.png`
2. `domen/result/7A9619FF-8B86-D0/test_folder/2023-03-19/913db945-c64e-11ed-9a80-5cb901fe8118.png`