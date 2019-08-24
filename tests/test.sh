#!/bin/bash

SITE1="http://127.0.0.1:8080/imports"
SITE2="http://127.0.0.1:8080/imports/1/citizens"
SITE3="http://127.0.0.1:8080/imports/1/citizens/birthdays"
SITE4="http://127.0.0.1:8080/imports/1/towns/stat/percentile/age"


# ab -n 6 -c 2 -k $SITE2 &
# ab -n 6 -c 2 -k $SITE3 &
# ab -n 6 -c 2 -k $SITE4 &


# ab  -n 1 -c 1 -k\
#     $SITE4&
ab  -n 1 -c 1 -k\
    -p big_data.json -T 'application/json' $SITE1 &
#     $SITE2&
    # $SITE2&
    # $SITE4