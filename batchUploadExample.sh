#!/bin/bash

subdomain=''
email=''
password=''

make virtualenv
source env/bin/activate

if [[ $1 -eq 0 ]] ; then
  path='./packs'
else
  path="$1"
fi

for f in "$path"/*.yaml
do
  echo $f
  ./emojipacks.py -s $subdomain -e $email -p $password -y $f;
done
