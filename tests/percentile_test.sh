#!/bin/bash


OK_TESTS=0
FAIL_TESTS=0
CONTENTTYPE='content-type: application/json'
FORMAT=' %{http_code} %{content_type}'
SITE='http://127.0.0.1:8080/imports'
FILE1='percentile/good_data_send1.json'
FILE2='percentile/good_data_send3.json'
FILE3='percentile/good_data_send10.json'

FILE1_E='percentile/good_data_expect1.json'
FILE2_E='percentile/good_data_expect3.json'
FILE3_E='percentile/good_data_expect10.json'


# @params:
#   $1: Файл с json даными для отправки
#   $2: Файо с json данными для сравнения
test_add_citizen()
{
    site=$SITE
    echo "Отправка данных о жителях на $site..."
    tmp=$(curl -X POST $site -d @$1 -H "$CONTENTTYPE" -w "$FORMAT" -s)
    read -r -a array <<< "$tmp"
    json=${array[0]}

    if [[ ${array[1]} -ne 201 ]]; then
        echo -e "[\e[31m FAIL \e[0m] Неверный http-code ответа"
        let FAIL_TESTS+=1 
        return 1
    elif [[ ${array[2]} != 'application/json' ]]; then
        echo -e "[\e[31m FAIL \e[0m] Неверный content-type ответа"
        let FAIL_TESTS+=1 
        return 1
    else
        import_id=$(python3 python_fun/get_import_id.py $json)
        echo -e "[\e[32m OK \e[0m] Полученный import_id: $import_id"
    fi


    site='http://127.0.0.1:8080/imports/'$import_id'/towns/stat/percentile/age'
    echo "Получение персентиля с $site"
    tmp=$(curl $site -w "$FORMAT" -s)
    read -r -a array <<< "$tmp"
    json=${array[0]}

    if [[ ${array[1]} -ne 200 ]]; then
        echo -e "[\e[31m FAIL \e[0m] Неверный http-code ответа"
        let FAIL_TESTS+=1 
        return 1
    elif [[ ${array[2]} != 'application/json' ]]; then
        echo -e "[\e[31m FAIL \e[0m] Неверный content-type ответа"
        let FAIL_TESTS+=1 
        return 1
    else
        python3 python_fun/check_data.py $json $2
        if [[ $? -ne 0 ]]; then
            echo -e "[\e[31m FAIL \e[0m] Данные не совпадают"
            let FAIL_TESTS+=1
            return 1
        else
            echo -e "[\e[32m OK \e[0m] Данные совпадают"
            let OK_TESTS+=1 
        fi
    fi
}


show_results()
{
    echo "Результаты тестирования percentile:"
    echo -e "    - \e[32m Пройдено: \e[0m  $OK_TESTS"
    echo -e "    - \e[31m Провалено: \e[0m  $FAIL_TESTS"
}


test_add_citizen $FILE1 $FILE1_E
test_add_citizen $FILE2 $FILE2_E
test_add_citizen $FILE3 $FILE3_E
show_results
