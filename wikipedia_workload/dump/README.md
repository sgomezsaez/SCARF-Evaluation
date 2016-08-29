1. Configure MediaWiki using the Web GUI configuration guide

	- Note: Check that the character set of the mediawiki database is utf8 (MYSQL: use <wiki_db>; show variables like "character_set_database";)

2. Download MWDumper from https://phabricator.wikimedia.org/diffusion/MWDU/ and Build using mvn clean package 

3. Disable Log Output in Mysql Server to improve performance:
	- MYSQL: SET sql_log_bin = 0
	- MYSQL: SET GLOBAL general_log = 'OFF';

4. Select and Download Dump from https://en.wikipedia.org/wiki/Wikipedia:Database_download#English-language_Wikipedia

5. Import Dump (based on https://www.mediawiki.org/wiki/Manual:MWDumper. See https://www.mediawiki.org/wiki/Manual_talk:MWDumper#MWDumper_error for typical errors)

	* Prerequisite
		- MYSQL: DELETE FROM page; DELETE FROM text; DELETE FROM revision;
		- Execute PHP Script in the MediaWiki Maintenance Directory: php rebuildall.php
	
	* Import Dump

		set -e && java -jar mwdumper-1.25.jar --format=sql:1.5 --filter=latest <path_to_dump_file>.xml.bz2 | mysql -f -u<user> -p<password> -h <host> --default-character-set=utf8 <wiki_db_name>
