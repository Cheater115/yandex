#!/bin/bash


OK_TESTS=0
FAIL_TESTS=0
SITE="http://127.0.0.1:8080/imports"
CONTENTTYPE='content-type: application/json'
CITIZEN_ID1=1
CITIZEN_ID2=2
CITIZEN_ID3=3

# @params:
#   $1: Сообщение(что за тест)
#   $2: Код ответа, который ожидается
#   $3: Файл с json даными
#   $4: Сайт
curl_code()
{
    echo "Тест: $1"

    S=$4
    M="PATCH"
    CT='content-type: application/json'

    tmp=$(curl --request $M $S -d $3 -H "$CT" -s -o /dev/null -w "%{http_code}")

    if [[ $tmp -eq $2 ]]; then
        echo -e "[\e[32m OK \e[0m] Ожидалось: $2, получили: $tmp"
        let OK_TESTS+=1
    else
        echo -e "[\e[31m FAIL \e[0m] Ожидалось: $2, получили: $tmp"
        let FAIL_TESTS+=1
    fi
}


show_results()
{
    echo "Результаты тестирования PATCH:"
    echo -e "    - \e[32m Пройдено: \e[0m  $OK_TESTS"
    echo -e "    - \e[31m Провалено: \e[0m  $FAIL_TESTS"
}


site=$SITE
echo "Отправка данных о жителях на $site..."
tmp=$(curl -X POST $site -d @patch/good_data.json -H "$CONTENTTYPE" -w "$FORMAT" -s)
read -r -a array <<< "$tmp"
json=${array[0]}
import_id=$(python3 python_fun/get_import_id.py $json)

echo
echo "---=== Плохие данные ===---"
echo
site="$SITE/$import_id/citizens/$CITIZEN_ID1"
curl_code "Ошибка в JSON" 400 @patch/error_in_json.json $site
curl_code "Лишнее поле у жителя" 400 @patch/extra_field.json $site
curl_code "Пустой запрос" 400 @patch/empty.json $site
curl_code "'citizen_id' попытка изменить" 400 @patch/citizen_id_change.json $site
curl_code "'name' пустая строка" 400 @patch/name_empty_string.json $site
curl_code "'birth_date' не правильная дата" 400 @patch/birth_date_not_right.json $site
curl_code "'gender' не male, не female" 400 @patch/gender_not_right.json $site
curl_code "'relatives' не существующий citizen_id" 400 @patch/relatives_not_citizen_id.json $site
curl_code "'relatives' не уникальные" 400 @patch/relatives_not_unique.json $site


echo
echo "---=== Хорошие данные ===---"
echo

CT='content-type: application/json'
tmp=$(curl --request PATCH $site -d @patch/good_patch_data.json -H "$CT" -s)
echo "Сверим вернувшийся результат с ожидаемым:"
python3 python_fun/check_data.py $tmp patch/good_patch_expect.json
if [[ $? -ne 0 ]]; then
    echo -e "[\e[31m FAIL \e[0m] Данные не совпадают"
    let FAIL_TESTS+=1
else
    echo -e "[\e[32m OK \e[0m] Данные совпадают"
    let OK_TESTS+=1 
fi

site=$SITE/$import_id/citizens
tmp=$(curl $site "$CT" -s)
echo "Сверим симметричность изменения родственников:"
python3 python_fun/check_data.py $tmp patch/good_data_expect.json
if [[ $? -ne 0 ]]; then
    echo -e "[\e[31m FAIL \e[0m] Данные не совпадают"
    let FAIL_TESTS+=1
    return 1
else
    echo -e "[\e[32m OK \e[0m] Данные совпадают"
    let OK_TESTS+=1 
fi

show_results
