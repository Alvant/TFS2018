## Задание

Поднять на своей машине DNS-сервер bind, который был бы мастером для зоны "fintechtestzone". При помощи `systemctl` сделать его автоматически поднимающимся при старте системы. Сделать его способным отвечать на запросы извне (чтобы слушал не только на 127.0.0.1, но и на внешнем интерфейсе). Обеспечить прохождение следующих тестов:

```bash
nslookup fintechtestzone. localhost
Name:   fintechtestzone
Address: 127.0.0.1
```

```bash
nslookup -type=txt fintechtestzone. localhost
fintechtestzone text = "Any text"
```

```bash
nslookup -type=ns fintechtestzone. localhost
zonemaster01    nameserver = s-XX.fintech-admin.m1.tinkoff.cloud.
```

Описать последовательность ваших действий (набор команд и правок в конфигах с краткими комментариями).

## Решение

Начинаем с команды

```bash
yum install -y bind bind-utils
```



Далее, редактируем/создаём конфигурационные файлы, и в конце запускаем bind.



**/etc/named.conf**

Добавляем строчки для некоей дополнительной безопасности (скрываем информацию о версии, см. https://wiki.meurisse.org/wiki/Bind)

```bash
options {
    ...
    
    version none;
    hostname none;
    
    ...
}
```

Добавляем блок rate-limit

```bash
options {
    ...
    
    rate-limit {
        responses-per-second 10;
        exempt-clients { 127.0.0.1; ::1; };
    };
    
    ...
}
```

Слушаем не только с localhost, а со всех IP.

IPv6 не занимаемся, слушаем только localhost.

Отключаем возможность рекурсивных запросов (делаем ведь Authoritative DNS server?).

```bash
options {
    ...
    
    listen-on port 53 { any; };
    listen-on-v6 port 53 { ::1; };
    recursion no;
    
    ...
}
```

И в конце добавляем строчку

```bash
include "/etc/named/named.conf.local";
```



**/etc/named/named.conf.local**

Прямое отображение (domain name -> IP), i.e. forward zone 

```bash
zone "fintechtestzone" {
    type master;
    file "/etc/named/zones/db.fintechtestzone"; # zone file path
};
```

Обратное отображение (IP -> domain name), i.e. reverse zone

```bash
zone "180.219.10.in-addr.arpa" {
    type master;
    file "/etc/named/zones/db.10.219.180";  # 10.219.180.12/26 subnet
};
```



**/etc/named/zones**

Папка с файлами зон

```bash
sudo chmod 755 /etc/named # rwxr-xr-x
sudo mkdir /etc/named/zones
```



**/etc/named/zones/db.fintechtestzone**

Файл зоны fintechtestzone.

```bash
$ORIGIN fintech-admin.m1.tinkoff.cloud.
$TTL 1d             ; Time a cache will keep responses

@    IN    SOA    s-01    zonemaster01 (
         2018071800 ; Serial
         12h        ; Refresh: frequency of zone transfer from slave
         15m        ; Retry: delay before slave retries after a zone transfer failure
         4w         ; Expire: time a slave will keep the data in case it cannot contact the master
         1h         ; Negative Cache TTL: time a cache will keep negative responses (NXDOMAIN)
)

; name server - NS record
@       IN    NS      s-01

; name server - A, AAAA, TXT records
s-01    IN    A       10.219.180.2
s-01    IN    AAAA    fe80::6d:4bff:fe11:d108
s-01    IN    TXT     "The hammer of the gods will drive our ships to new lands"
```



**/etc/named/zones/db.10.219.180**

Файл для обратной зоны (reverse zone file).

```bash
$ORIGIN fintech-admin.m1.tinkoff.cloud.
$TTL 1d             ; Time a cache will keep responses

@    IN    SOA    s-01    zonemaster01 (
         2018071800 ; Serial
         12h        ; Refresh: frequency of zone transfer from slave
         15m        ; Retry: delay before slave retries after a zone transfer failure
         4w         ; Expire: time a slave will keep the data in case it cannot contact the master
         1h         ; Negative Cache TTL: time a cache will keep negative responses (NXDOMAIN)
)

; NS record
@     IN    NS      s-01

; PTR record
12    IN    PTR     s-01    ; 10.219.180.12
```



**sudo named-checkconf**

Проверяем синтаксис в named.conf* файлах



**sudo named-checkzone fintechtestzone /etc/named/zones/db.fintechtestzone**

Проверяем файл зоны



**sudo named-checkzone 180.219.10.in-addr.arpa /etc/named/zones/db.10.219.180**

Проверяем файл обратной зоны



**sudo systemctl start named**

Загружаем bind



**sudo systemctl enable named**

Делаем автоматически загружающимся при старте системы



---

Ресурсы

* https://www.digitalocean.com/community/tutorials/how-to-configure-bind-as-a-private-network-dns-server-on-centos-7
* https://wiki.meurisse.org/wiki/Bind
* https://linuxconfig.org/linux-dns-server-bind-configuration