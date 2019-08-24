#!/bin/bash


OK_TESTS=0
FAIL_TESTS=0


# @params:
#   $1: Сообщение(что за тест)
#   $2: Код ответа, который ожидается
#   $3: Файл с json даными
curl_code()
{
    echo "Тест: $1"

    S="http://127.0.0.1:8080/imports"
    M="POST"
    CT='content-type: application/json'

    tmp=$(curl -X $M $S -d $3 -H "$CT" -s -o /dev/null -w "%{http_code}")

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
    echo "Результаты тестирования /imports на плохих данных:"
    echo -e "    - \e[32m Пройдено: \e[0m  $OK_TESTS"
    echo -e "    - \e[31m Провалено: \e[0m  $FAIL_TESTS"
}


# тестирование /imports

curl_code "Ошибка в JSON" 400 @imports/error_in_json.json
curl_code "Нет поля 'citizens'" 400 @imports/lose_citizens.json
curl_code "Пропущенно поле у жителя" 400 @imports/lose_field.json
curl_code "Лишнее поле у жителя" 400 @imports/extra_field.json
curl_code "'citizen_id' не уникальный" 400 @imports/citizen_id_not_unique.json
curl_code "'citizen_id' меньше нуля" 400 @imports/citizen_id_lt_0.json
curl_code "'citizen_id' не число" 400 @imports/citizen_id_not_number.json
curl_code "'name' пустая строка" 400 @imports/name_empty_string.json
curl_code "'name' состоит из пробельных символов" 400 @imports/name_whitespace.json
curl_code "'birth_date' не коректный формат" 400 @imports/birth_date_not_correct.json
curl_code "'birth_date' не правильная дата" 400 @imports/birth_date_not_right.json
curl_code "'gender' не male, не female" 400 @imports/gender_not_right.json
curl_code "'relatives' не существующий citizen_id" 400 @imports/relatives_not_citizen_id.json
curl_code "'relatives' не симметричные" 400 @imports/relatives_not_symm.json
curl_code "'relatives' не уникальные" 400 @imports/relatives_not_unique.json
echo

show_results
