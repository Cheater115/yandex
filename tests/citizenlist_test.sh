#!/bin/bash


OK_TESTS=0
FAIL_TESTS=0
CONTENTTYPE='content-type: application/json'
FORMAT=' %{http_code} %{content_type}'
SITE='http://127.0.0.1:8080/imports'
FILE1='citizenlist/good_data.json'
FILE2='citizenlist/good_data_3.json'
FILE3='citizenlist/good_data_10.json'


# @params:
#   $1: Файл с json даными
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


    site='http://127.0.0.1:8080/imports/'$import_id'/citizens'
    echo "Получение данных о жителях с $site"
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
        python3 python_fun/check_data.py $json $1
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
    echo "Результаты тестирования отправки/получения данных:"
    echo -e "    - \e[32m Пройдено: \e[0m  $OK_TESTS"
    echo -e "    - \e[31m Провалено: \e[0m  $FAIL_TESTS"
}


test_add_citizen $FILE1
test_add_citizen $FILE2
test_add_citizen $FILE3
show_results
