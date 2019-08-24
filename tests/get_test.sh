#!/bin/bash


CONTENTTYPE='content-type: application/json'
FILE='get/good_data_3.json'
FORMAT=' %{http_code} %{content_type}'


SITE='http://127.0.0.1:8080/imports'
tmp=$(curl -X POST $SITE -d @$FILE -H "$CONTENTTYPE" -w "$FORMAT" -s)
read -r -a array <<< "$tmp"
json=${array[0]}


echo "Отправка данных о жителях на $SITE..."
if [[ ${array[1]} -ne 201 ]]; then
    echo -e "[\e[31m FAIL \e[0m] Неверный http-code ответа"
    exit 1
elif [[ ${array[2]} != 'application/json' ]]; then
    echo -e "[\e[31m FAIL \e[0m] Неверный content-type ответа"
    exit 1
else
    import_id=$(python3 get/get_import_id.py $json)
    echo -e "[\e[32m OK \e[0m] Полученный import_id: $import_id"
fi


SITE='http://127.0.0.1:8080/imports/'$import_id'/citizens'
tmp=$(curl $SITE -w "$FORMAT" -s)
read -r -a array <<< "$tmp"
json=${array[0]}


echo "Получение данных о жителях с $SITE"
if [[ ${array[1]} -ne 200 ]]; then
    echo -e "[\e[31m FAIL \e[0m] Неверный http-code ответа"
elif [[ ${array[2]} != 'application/json' ]]; then
    echo -e "[\e[31m FAIL \e[0m] Неверный content-type ответа"
else
    python3 get/check_data.py $json $FILE
    if [[ $? -ne 0 ]]; then
        echo -e "[\e[31m FAIL \e[0m] Данные не совпадают"
    else
        echo -e "[\e[32m OK \e[0m] Данные совпадают"
    fi
fi

