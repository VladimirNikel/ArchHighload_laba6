# Архитектура высоконагруженных система. ДЗ №6
## Создание системы мониторинга на подобии ***VictoriaMetrics***


## Цель:
Необходимо:
> 1. Реализовать свою систему мониторинга (лучше всего *VicroriaMetrics*);
> 1. Развернуть её на сервере, где располагаются части задания №5;
> 1. Показать ***что*** и ***как*** запрашивается в нашей системе мониторинга;
> 1. А также, где в коде можно добавить алертинг.  


## Инструкция по установке:
1. Скачать/стянуть репозиторий 
1. Перейти в папку репозитория
1. На сервере/серверах убедиться, что docker-контейнеры подняты, если нет, то проделать следующие пункты:
    1. Выполнить команду `docker build -t <название образа> -f dockerfile . `, мною для работы используется исходный образ ubuntu. Поэтому для создания образов использую команды:
        * `docker build -t ubuntu/archhightload_laba6_1 -f dockerfile1 .`
        * `docker build -t ubuntu/archhightload_laba6_2 -f dockerfile2 .`
    1. Выполнить команду `docker run -it --name <название контейнера> -p 0.0.0.0:<порт>:8000 ubuntu/archhightload_laba2` для создания docker-контейнера из docker-образа. В рамках задания были выполнены команды:
        * `docker run -td --name laba6_1_archHL --restart on-failure -p 0.0.0.0:5020:8000 ubuntu/archhightload_laba6_1`
        * `docker run -td --name laba6_2_archHL --restart on-failure -p 0.0.0.0:5030:8000 ubuntu/archhightload_laba6_2`
1. На третьем сервере необходимо установить Nginx (инструкция приложена) и прописать в конфигурационном файле `/etc/nginx/nginx.config` как в приложенном к репозиторию одноименном файле.
1. Потом выполнить команду перезапуска Nginx'а: `nginx -s reload`
1. Далее воспользуйтесь либо браузером по [адресу](http://127.0.0.1:80) `http://127.0.0.1:80/` либо воспользуйтесь терминалом:
  - `curl http://127.0.0.1:80/v1/current/?city=Moscow` - чтобы узнать текущую температуру в городе Moscow (можно использовать и другие города, хы)
  - `curl "http://127.0.0.1:80/v1/forecast/?city=Moscow&timestamp=3h"` - чтобы узнать прогноз погоды в интересующем Вас городе и используя *timestamp*:
    * `1h` - чтобы увидеть прогноз погоды на 1 час вперед
    * `3h` - чтобы увидеть прогноз погоды на 3 часа вперед
    * `tomorrow` - чтобы увидеть прогноз погоды на завтра в это же время
    * `yesterday` - чтобы увидеть какая погода была вчера в это же время






## Обновления:

В результате работы кода получится примерно следующее:
```bash
nikel@Aspire-A717-71G:~/dev/University/ArchHighload/6 laba$ python3 monitor.py 
Введите логин: Nikel
Введите пароль: 
Введите количество секунд, через которое будут опрашиваться сервера: 45
Начал работать в 02:57:36 03.11.2020
{'server_path': '127.0.0.1:8000', 'date_utc': '2020.11.02 23:58:21', 'status': 'unavailable'}
{'server_path': '194.61.2.84:5020', 'date_utc': '2020.11.02 23:58:21', 'status': 'available', 'data': '{"status_auth": "ok", "id_service": "1", "count_visit_root": 2, "count_dispays_current_weather": 1, "count_requests_to_OWM": 5, "avr": {"root_page": 1.7881393432617188e-06, "current": 0.23424744606018066, "forecast": 0.23913037776947021}}'}
{'server_path': '194.61.2.84:5030', 'date_utc': '2020.11.02 23:58:21', 'status': 'available', 'data': '{"status_auth": "ok", "id_service": "2", "count_visit_root": 4, "count_dispays_current_weather": 2, "count_requests_to_OWM": 2, "avr": {"root_page": 2.2649765014648438e-06, "current": 0.24375951290130615, "forecast": 0.24423933029174805}}'}
{'server_path': '127.0.0.1:8000', 'date_utc': '2020.11.02 23:59:06', 'status': 'available', 'data': '{"status_auth": "ok", "id_service": "0", "count_visit_root": 1, "count_dispays_current_weather": 1, "count_requests_to_OWM": 3, "avr": {"root_page": 1.9073486328125e-06, "current": 0.8310353755950928, "forecast": 0.5098166465759277}}'}
{'server_path': '194.61.2.84:5020', 'date_utc': '2020.11.02 23:59:06', 'status': 'available', 'data': '{"status_auth": "ok", "id_service": "1", "count_visit_root": 2, "count_dispays_current_weather": 0, "count_requests_to_OWM": 2, "avr": {"root_page": 2.2649765014648438e-06, "current": 0.0, "forecast": 0.2474595308303833}}'}
{'server_path': '194.61.2.84:5030', 'date_utc': '2020.11.02 23:59:06', 'status': 'available', 'data': '{"status_auth": "ok", "id_service": "2", "count_visit_root": 1, "count_dispays_current_weather": 1, "count_requests_to_OWM": 3, "avr": {"root_page": 2.2649765014648438e-06, "current": 0.19890618324279785, "forecast": 0.28251147270202637}}'}
^C

Что ж, до встречи...
Осталось дождаться ответа от количества потоков:  1
{'server_path': '127.0.0.1:8000', 'date_utc': '2020.11.02 23:59:51', 'status': 'available', 'data': '{"status_auth": "ok", "id_service": "0", "count_visit_root": 0, "count_dispays_current_weather": 0, "count_requests_to_OWM": 0, "avr": {"root_page": 0.0, "current": 0.0, "forecast": 0.534808874130249}}'}
{'server_path': '194.61.2.84:5020', 'date_utc': '2020.11.02 23:59:51', 'status': 'available', 'data': '{"status_auth": "ok", "id_service": "1", "count_visit_root": 0, "count_dispays_current_weather": 0, "count_requests_to_OWM": 0, "avr": {"root_page": 2.1457672119140625e-06, "current": 0.0, "forecast": 0.33891844749450684}}'}
{'server_path': '194.61.2.84:5030', 'date_utc': '2020.11.02 23:59:51', 'status': 'available', 'data': '{"status_auth": "ok", "id_service": "2", "count_visit_root": 0, "count_dispays_current_weather": 0, "count_requests_to_OWM": 0, "avr": {"root_page": 2.1457672119140625e-06, "current": 0.26261353492736816, "forecast": 0.3184547424316406}}'}
```

Как видно из представленного ответа монитора, в коде прописана обработка доступности сервера (если сервер приуныл, мы в статусе видим это `{'server_path': '127.0.0.1:8000', 'date_utc': '2020.11.02 23:58:21', 'status': 'unavailable'}`).

Также, можно заметить что локальный сервер "подтормаживает" на фоне удаленных серверов, расположенных где-то там, где скорость интернета куда выше, чем раздающийся с мобильного телефона трафик...


## Инструментарий:
- GIT (устанавливается командой `sudo apt install git -y`)
- Docker (устанавливается командой `sudo apt install -y docker-ce`) [дополнительная инструкция](https://losst.ru/ustanovka-docker-na-ubuntu-16-04)
- Nginx (устанавливается командой `sudo apt install nginx`) [дополнительная инструкция](https://losst.ru/ustanovka-nginx-ubuntu-16-04)