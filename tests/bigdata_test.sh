#!/bin/bash


python3 python_fun/generate_big_data.py


SITE1="http://127.0.0.1:8080/imports"
echo "Посылаем большие данные на $SITE1..."
tmp=$(ab -v 2 -n 1 -c 1 -k\
    -p big_data.json -T 'application/json' $SITE1)
echo $tmp | egrep -o "(Time taken for tests: )[0-9]+\.[0-9]+ seconds"
import_id=$(echo $tmp | egrep -o '{"data":{"import_id":[0-9]+' | egrep -o '[0-9]+')


SITE2="$SITE1/$import_id/citizens"
SITE3="$SITE2/birthdays"
SITE4="$SITE1/$import_id/towns/stat/percentile/age"

echo "Запрос GET к $SITE2"
tmp=$(ab -n 1 -c 1 -k $SITE2)
echo $tmp | egrep -o "(Time taken for tests: )[0-9]+\.[0-9]+ seconds"

echo "Запрос GET к $SITE3"
tmp=$(ab -n 1 -c 1 -k $SITE3)
echo $tmp | egrep -o "(Time taken for tests: )[0-9]+\.[0-9]+ seconds"

echo "Запрос GET к $SITE4"
tmp=$(ab -n 1 -c 1 -k $SITE4)
echo $tmp | egrep -o "(Time taken for tests: )[0-9]+\.[0-9]+ seconds"


echo "Одновременные запросы"
a=$(ab -n 6 -c 2 -k $SITE2 &)
b=$(ab -n 6 -c 2 -k $SITE3 &)
c=$(ab -n 6 -c 2 -k $SITE4 &)
echo $a | egrep -o "(Time taken for tests: )[0-9]+\.[0-9]+ seconds"
echo $b | egrep -o "(Time taken for tests: )[0-9]+\.[0-9]+ seconds"
echo $c | egrep -o "(Time taken for tests: )[0-9]+\.[0-9]+ seconds"

rm big_data.json
