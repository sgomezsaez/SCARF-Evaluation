WIKISTATS_URL = "https://dumps.wikimedia.org/other/pagecounts-raw"
WIKISTATS_PAGECOUNTS = "pagecounts"
WIKISTATS_PROJECTCOUNT = "projectcounts"

WIKISTATS_FILTER_VALUES = ["en"]

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
DATA_LOCAL_PATH = "/Users/gomezsso/Documents/dissertation_evaluation/SCARF-Evaluation/wikipedia_workload/data/"
DATA_LOCAL_FILE_FILTERED = "_filtered"
DATA_LOCAL_FILE_MONTHLY = "_monthly"
DATA_LOCAL_FILE_HOURLY_SUMMARY = "_hourly_summary"


# Figures Path
FIGURES_LOCAL_PATH = "/Users/gomezsso/Documents/dissertation/Publications/Journal/2016_TOIT/gfx/charts/"

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