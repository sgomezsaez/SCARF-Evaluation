#!/bin/bash

set -e 

if [ $# -lt 5 ]
then
	echo " Usage: "
	echo "$0 <path_to_dump_file> <db_user> <db_pssw> <db_host> <wiki_db_name>"
else

	DUMP_FILE=$1
	DB_USER=$2
	DB_PSSW=$3
	DB_HOST=$4
	WIKI_DB_NAME=$5

	java -jar mwdumper-1.25.jar --format=sql:1.5 --filter=latest $DUMP_FILE | mysql -f -u$DB_USER -p$DB_PSSW -h $DB_HOST --default-character-set=utf8 $WIKI_DB_NAME
fi 
