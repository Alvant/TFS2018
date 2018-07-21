Опишите коротко

* все команды, которые вы выполняли в процессе подготовки д/з
* все опции uwsgi, которые задавались при запуске приложения
* все конфигурационные опции из конфиг. файла former.ini
* что делает каждая строчка кода webrunner.py

---

### Команды

Запустить веб-сервер в связке с приложением webrunner.py

```bash
uwsgi
  --plugins=python
  --http-socket=0.0.0.0:80
  --wsgi-file /opt/webcode/former/process/webrunner.py
  --static-map /form=/opt/webcode/former/form/index.html
  --processes=5
  --master
  --pidfile=/tmp/formdig.pid
  --vacuum
  --max-requests=5000
```

Добавить супервизора в список программ, загружаемых при старте системы. Запустить супервизора.
```bash
systemctl enable supervisor
systemctl start supervisor
```

Посмотреть статус супервизора. Остановить процесс former, который под супервизором. Запустить former.
```bash
supervisorctl status
supervisorctl stop former
supervisorctl start former
```

### Опции uwsgi

* `--plugins=python` — использовать uWSGI плагин python
* `--http-socket=0.0.0.0:80` — сокет, на котором надо слушать по HTTP протоколу (на всех IP, на 80 порту)
* `--wsgi-file /opt/webcode/former/process/webrunner.py` — очевидно, файл с приложением
* `--static-map /form=/opt/webcode/former/form/index.html` — отобразить mountpoint в файл index.html (запрос к /form -> выдаётся файл index.html)
* `--processes=5` — породить 5 процессов для обработки запросов
* `--master` — с мастер-процессом, который будет воскрешать worker-ов, если они будут отваливаться
* `--pidfile=/tmp/formdig.pid` — в файле, видимо, хранится PID процесса uwsgi
* `--vacuum` — удалять файлы/сокеты при завершении процесса
* `--max-requests=5000` — перезагружать worker-ов после такого числа запросов

### Опции из файла former.ini

http://supervisord.org/configuration.html

```bash
[program:former]  # название секции в .ini файле
command=uwsgi     # команда для запуска
    --plugins=python
    --http-socket=0.0.0.0:80
    --wsgi-file /opt/webcode/former/process/webrunner.py
    --static-map /form=/opt/webcode/former/form/index.html
    --processes=5
    --master
    --pidfile=/tmp/former.pid
    --vacuum
    --max-requests=5000
stopsignal=QUIT   # Сигнал чтобы убить процесс
autostart=true    # Запускать вместе с супервизором
startretries=10   # Количество неудачных попыток запустить программу, которые предпримет супервизор, прежде чем бросить этим заниматься
startsecs=0       # Число секунд, которые могут понадобиться программе для запуска (от старта до способности нормально работать). Значение 0 показывает, что времени на разгон не нужно
stopwaitsecs=10   # Число секунд, сколько можно ждать перед посылкой ОС сигнала SIGCHLD процессу supervisord после того, как запущенной программе был послан stopsignal. По истечении времени (если SIGCHLD так и не получен) supervisord пошлёт своему дочернему процессу SIGKILL
stopasgroup=true  # Супервизор шлёт stopsignal всей группе подопечного процесса

stdout_logfile=/var/log/webapps/former_stdout.log
stdout_logfile_maxbytes=60MB  # Максимальный размер log файла. Когда размер становится больше порога — ротация (i.e log rotation https://en.wikipedia.org/wiki/Log_rotation), то есть название файла немного изменяется, и создаётся чистый log файл для продолжения записи
stdout_logfile_backups=4      # Делать столько backup копий log файла при ротации
stdout_capture_maxbytes=4MB   # Max number of bytes written to capture FIFO when process is in “stdout capture mode” (see Capture Mode). 

stderr_logfile=/var/log/webapps/former_stderr.log
stderr_logfile_maxbytes=60MB
stderr_logfile_backups=4
stderr_capture_maxbytes=4MB
```

### Код webrunner.py

```python
#!/usr/bin/python

from cgi import parse_qs

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/plain')])

    wsgi_content = env["wsgi.input"].read(0)
    request_uri_content = env["REQUEST_URI"]
    request_method_content = env["REQUEST_METHOD"]
    d = parse_qs(wsgi_content)
    return [
        "Method: " + request_method_content + "\n" +
        "Get content: " + request_uri_content + "\n" +
        "Post content: " + wsgi_content + "\n"
    ]
```

