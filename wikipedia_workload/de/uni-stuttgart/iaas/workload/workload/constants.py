WIKISTATS_URL = "https://dumps.wikimedia.org/other/pagecounts-raw"
WIKISTATS_PAGECOUNTS = "pagecounts"
WIKISTATS_PROJECTCOUNT = "projectcounts"

WIKISTATS_FILTER_VALUES = ["en"]

WIKISTATS_FILE_SCALED_100_SUFFIX = '_scaled_factor100Scaling'
# Wikistats Unique Devices Properties
WIKISTATS_UNIQUE_DEVICES_URL = "https://dumps.wikimedia.org/other/unique_devices/2016/2016-01/"

WIKISTATS_UNIQUE_DEVICES_TIMESTAMP = 'timestamp'
WIKISTATS_UNIQUE_DEVICES_EN_WIKI = 'en.wikipedia.org'
WIKISTATS_UNIQUE_DEVICES_EN_WIKI_MOBILE = 'en.m.wikipedia.org'
WIKISTATS_UNIQUE_DEVICES_EN_WIKI_TOTAL = 'en.wikipedia.org.total'
WIKISTATS_TOTAL_DAILY_VISITS = 'en.wikipedia.org.daily_visits'
WIKISTATS_TOTAL_NEW_USERS = 'en.wikipedia.org.newUsers'
WIKISTATS_DAILY_DONATIONS = 'en.wikipedia.org.donations'


WIKISTATS_UNIQUE_DEVICES_COL_LIST = [WIKISTATS_UNIQUE_DEVICES_TIMESTAMP, WIKISTATS_UNIQUE_DEVICES_EN_WIKI_MOBILE,
                                     WIKISTATS_UNIQUE_DEVICES_EN_WIKI, WIKISTATS_UNIQUE_DEVICES_EN_WIKI_TOTAL,
                                     WIKISTATS_TOTAL_DAILY_VISITS, WIKISTATS_TOTAL_NEW_USERS,
                                     WIKISTATS_DAILY_DONATIONS]



WIKISTATS_UNIQUE_DEVICES_FILE_PATH = '/home/ubuntu/SCARF-Evaluation/wikipedia_workload/data/unique_users_monthly.csv'

# Wikistats HTTP Retrieval properties

#WIKISTATS_BEGIN_YEAR = 2015
WIKISTATS_BEGIN_YEAR = 2016
WIKISTATS_END_YEAR = 2016

#WIKISTATS_BEGIN_MONTH = 07
WIKISTATS_BEGIN_MONTH = 01
WIKISTATS_END_MONTH = 01

#WIKISTATS_BEGIN_DAY = 21
WIKISTATS_BEGIN_DAY = 01
WIKISTATS_END_DAY = 31

WIKISTATS_HOURS = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]


# Wikistats file properties
WIKISTATS_COL_PROJECT = 'col_project'
WIKISTATS_COL_PAGE = 'col_page'
WIKISTATS_COL_REQUESTS = 'col_requests'
WIKISTATS_COL_SIZE = 'col_size'

WIKISTATS_COLUMNS = [WIKISTATS_COL_PROJECT, WIKISTATS_COL_PAGE, WIKISTATS_COL_REQUESTS, WIKISTATS_COL_SIZE]

WIKISTATS_COL_TIMESTAMP = 'timestamp'

WIKISTATS_DELIMITER = ' '

wikibooks_del = ".b"
wiktionary_del = ".d"
wikimedia_del = ".m"
wikipedia_mobile_del = ".mw"
wikinews_del = ".n"
wikiquote_del = ".q"
wikisource_del = ".s"
wikiversity_del = ".v"
mediawiki_del = ".w"

# Data local path
DATA_LOCAL_PATH = "/home/ubuntu/SCARF-Evaluation/wikipedia_workload/data/"
DATA_LOCAL_FILE_FILTERED = "_filtered"
DATA_LOCAL_FILE_MONTHLY = "_monthly"
DATA_LOCAL_FILE_HOURLY_SUMMARY = "_hourly_summary"
DATA_LOCAL_FILE_SCALED = "_scaled"
DATA_LOCAL_FILE_NO_CLEAN = "_no_clean"



# Figures Path
FIGURES_LOCAL_PATH = "/home/ubuntu/SCARF-Evaluation/"

# Threads Config
THREAD_NUMBER = 24

# Workload Summary COL
WORKLOAD_SUMMARY_COL_PROJECT = 'project'
WORKLOAD_SUMMARY_COL_PAGE = 'page'
WORKLOAD_SUMMARY_COL_TOTAL_REQUESTS = 'total_number_reqs'
WORKLOAD_SUMMARY_COL_BYTES_PER_REQUEST = 'bytes_per_req'
WORKLOAD_SUMMARY_COL_TOTAL_BYTES = 'total_bytes'
WORKLOAD_SUMMARY_COL_INIT_DATE = 'init_date'
WORKLOAD_SUMMARY_COL_END_DATE = 'end_date'
WORKLOAD_SUMMARY_COL_FREQUENCY = 'hourly_frequency'

WORKLOAD_SUMMARY_STAT_TIMESTAMP = 'timestamp'
WORKLOAD_SUMMARY_STAT_COUNT_REQ = 'count_req'
WORKLOAD_SUMMARY_STAT_COUNT_BYTES = 'count_bytes'
WORKLOAD_SUMMARY_STAT_MEAN_REQ = 'mean_req'
WORKLOAD_SUMMARY_STAT_MEAN_BYTES = 'mean_bytes'
WORKLOAD_SUMMARY_STAT_STD_REQ = 'std_req'
WORKLOAD_SUMMARY_STAT_STD_BYTES = 'std_bytes'
WORKLOAD_SUMMARY_STAT_MAX_REQ = 'max_req'
WORKLOAD_SUMMARY_STAT_MAX_BYTES = 'max_bytes'
WORKLOAD_SUMMARY_STAT_SUM_REQ = 'sum_req'
WORKLOAD_SUMMARY_STAT_SUM_BYTES = 'sum_bytes'

WORKLOAD_SUMMARY_COL = [WORKLOAD_SUMMARY_COL_PROJECT, WORKLOAD_SUMMARY_COL_PAGE, WORKLOAD_SUMMARY_COL_TOTAL_REQUESTS,
                        WORKLOAD_SUMMARY_COL_BYTES_PER_REQUEST, WORKLOAD_SUMMARY_COL_TOTAL_BYTES,
                        WORKLOAD_SUMMARY_COL_INIT_DATE, WORKLOAD_SUMMARY_COL_END_DATE, WORKLOAD_SUMMARY_COL_FREQUENCY]

font = {

        'size'   : 8}

# Generated Workload Config
GENERATED_WORKLOAD_COL_TIMESTAMP = 'timestamp'
GENERATED_WORKLOAD_COL_SUM_REQS = 'sum_req'
GENERATED_WORKLOAD_COL_DAILY_PROPORTION_REQS = 'daily_proportion_reqs'
GENERATED_WORKLOAD_COL_HOURLY_CONCURRENT_USERS = 'hourly_concurrent_users'

# Generated Workload Files
WIKISTATS_GENERATED_WORKLOAD_PREFIX = "workload_generated-"
WIKISTATS_COL_PROJECT = 'col_project'
WIKISTATS_COL_PAGE = 'col_page'
WIKISTATS_COL_REQUESTS = 'col_requests'
WIKISTATS_COL_SIZE = 'col_size'
WIKISTATS_COL_DELAY = 'col_delay'

# Load Test Properties

JAR_LOAD_TEST_PATH = "/home/ubuntu/SCARF-Evaluation/wikipedia_workload/jmeter_loader/DynamicExecuter-1.0-SNAPSHOT.jar"
LOAD_TEST_CONFIG_PATH = "/home/ubuntu/SCARF-Evaluation/wikipedia_workload/jmeter_test_plan/"
LOAD_TEST_ARGUMENTS_FILE = LOAD_TEST_CONFIG_PATH + 'arguments.properties'
LOAD_TEST_CONFIG_FILE = LOAD_TEST_CONFIG_PATH + 'config.properties'

CONFIG_TEST_PLAN_PATH_VAR = 'test_plan_path'
CONFIG_JMETER_PATH_VAR = 'jmeter_home_path'
CONFIG_TEST_PLAN_PATH_VALUE = '/home/ubuntu/SCARF-Evaluation/wikipedia_workload/jmeter_test_plan/MediaWiki_Load_Profile.jmx'
CONFIG_JMETER_PATH_VALUE = '/Users/gomezsso/Applications/apache-jmeter-2.9'

ARGUMENTS_JMETER_SCENARIO_ID_VAR = 'experiment_scenario_id'
ARGUMENTS_JMETER_ROUND_ID_VAR = 'experiment_round'
ARGUMENTS_JMETER_HTTP_HOST_VAR = 'http_host'
ARGUMENTS_JMETER_HTTP_PORT_VAR = 'http_port'
ARGUMENTS_JMETER_HTTP_PATH_VAR = 'http_path'
ARGUMENTS_JMETER_NUMBER_THREADS_VAR = 'number_of_threads'
ARGUMENTS_JMETER_LOOP_PER_THREAD_VAR = 'loop_per_thread_count'
ARGUMENTS_JMETER_THREAD_RAMPUP_VAR = 'thread_ramp_up_period'
ARGUMENTS_JMETER_WORKLOAD_CSV_PATH_VAR = 'workload_csv_file_path'
ARGUMENTS_JMETER_WORKLOAD_CSV_NUM_ROWS_VAR = 'workload_number_of_csv_rows'
ARGUMENTS_JMETER_WORKLOAD_CSV_COL_NAMES_VAR = 'workload_csv_column_names'
ARGUMENTS_JMETER_WORKLOAD_CSV_COL_DELIMITER_VAR = 'workload_csv_column_delimiter'
ARGUMENTS_JMETER_DELAY_BETWEEN_REQUESTS_VAR = 'delay_between_requests'
ARGUMENTS_JMETER_RESULTS_PATH_VAR = 'results_path'

ARGUMENTS_JMETER_SCENARIO_ID_VALUE = '1.1.1'
ARGUMENTS_JMETER_ROUND_ID_VALUE = 'R1'
ARGUMENTS_JMETER_HTTP_HOST_VALUE = 'localhost'
ARGUMENTS_JMETER_HTTP_PORT_VALUE = '80'
ARGUMENTS_JMETER_HTTP_PATH_VALUE = '/w'
ARGUMENTS_JMETER_LOOP_PER_THREAD_VALUE = '1'
ARGUMENTS_JMETER_THREAD_RAMPUP_VALUE = '0'
ARGUMENTS_JMETER_WORKLOAD_CSV_PATH_VALUE = DATA_LOCAL_PATH
ARGUMENTS_JMETER_WORKLOAD_CSV_NUM_ROWS_VALUE = '7704'
ARGUMENTS_JMETER_WORKLOAD_CSV_COL_NAMES_VALUE = 'col_delay,col_page,col_project,col_requests,col_size'
ARGUMENTS_JMETER_WORKLOAD_CSV_COL_DELIMITER_VALUE = ','
ARGUMENTS_JMETER_DELAY_BETWEEN_REQUESTS_VALUE = '1'
ARGUMENTS_JMETER_RESULTS_PATH_VALUE = '/Users/gomezsso/Documents/dissertation_evaluation/SCARF-Evaluation/wikipedia_workload/experiments_results'

