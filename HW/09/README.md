Конфигурационные [файлы](etc/nginx/conf.d) для серверов test-1 и test-3 и default. Для test-2 такой файл не создавался (nginx для него выдаёт 404 по настройкам в [default.conf](etc/nginx/conf.d/default.conf)), а test-3 — это дополнительный сервер, на котором тестируется lua-модуль (для последнего задания, `curl test-3`).

Подправленный [hosts](etc/hosts) файл (чтобы курлить тесты с лоукалхоста).

Итоговая [ngix конфигурация](etc/nginx/nginx.conf).

Файл [nginx.spec](home/rpmbuild/SPECS/nginx.spec) из каталога nginx rpm пакета.

Как понять, собран ли nginx с модулем VTS? Точно не знаю. Можно сделать `nginx -V` и посмотреть в результате команды на `--add-module` в поисках чего-нибудь-vts. Но это кажется не очень надёжным вариантом. Вместо этого можно ещё протестировать конфиг `nginx -t -c ~/test.conf` с содержимым, например, `events {} http {vhost_traffic_status_zone;}`. Хотя может оказаться, что вместо VTS стоит какой-нибудь другой модуль, который тоже обрабатывает эту директиву...

Для [картинок](img/nginx-vts-exporter.png) добавил дашборд Nginx VTS Exporter в Графану.
