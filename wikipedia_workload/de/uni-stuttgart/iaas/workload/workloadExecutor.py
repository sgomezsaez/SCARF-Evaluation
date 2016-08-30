import os
from workload import constants as cs
import jprops as jprops
from csvHelper import csvHelper as csvHelper
import pandas as pd
import subprocess


def getDateFromFileName(fileName):
    split1 = fileName.split('-')
    print split1

# Generate the File List & Read Files

pageCountFileList = csvHelper.retrieve_files_time_interval(cs.WIKISTATS_BEGIN_YEAR, cs.WIKISTATS_BEGIN_MONTH,
                                                cs.WIKISTATS_BEGIN_DAY, cs.WIKISTATS_END_YEAR, cs.WIKISTATS_END_MONTH,
                                                   cs.WIKISTATS_END_DAY, cs.WIKISTATS_HOURS, cs.WIKISTATS_PAGECOUNTS)

generatedWorkloadFileList = [(cs.WIKISTATS_GENERATED_WORKLOAD_PREFIX + i + cs.WIKISTATS_FILE_SCALED_100_SUFFIX + '.csv')
                             for i in pageCountFileList]


output_workload_config_file = cs.DATA_LOCAL_PATH + 'workload_hourly_distribution_scaled_factor100.csv'
df_workload_config = pd.read_csv(output_workload_config_file, delimiter=' ')

# For each generated workload file:
# 1) Read the Workload Config Parameters for Each Hour and generate a custom config parameters file
# 2) Execute the jmeter load executer from Sherif
# 3) Save the result

count_workload_file_list = 0
for index,row in df_workload_config.iterrows():

    config_properties = {cs.CONFIG_TEST_PLAN_PATH_VAR: cs.CONFIG_TEST_PLAN_PATH_VALUE,
                         cs.CONFIG_JMETER_PATH_VAR: cs.CONFIG_JMETER_PATH_VALUE}

    scenario_id_value = pageCountFileList[count_workload_file_list].split('-')[1] + '-' + \
                        pageCountFileList[count_workload_file_list].split('-')[2]


    ##### Approach using the Dynamic Load Tester - Sherif
    argument_properties = {cs.ARGUMENTS_JMETER_SCENARIO_ID_VAR: scenario_id_value,
                           cs.ARGUMENTS_JMETER_ROUND_ID_VAR: cs.ARGUMENTS_JMETER_ROUND_ID_VALUE,
                           cs.ARGUMENTS_JMETER_HTTP_HOST_VAR: cs.ARGUMENTS_JMETER_HTTP_HOST_VALUE,
                           cs.ARGUMENTS_JMETER_HTTP_PORT_VAR: cs.ARGUMENTS_JMETER_HTTP_PORT_VALUE,
                           cs.ARGUMENTS_JMETER_HTTP_PATH_VAR: cs.ARGUMENTS_JMETER_HTTP_PATH_VALUE,
                           cs.ARGUMENTS_JMETER_DELAY_BETWEEN_REQUESTS_VAR : cs.ARGUMENTS_JMETER_DELAY_BETWEEN_REQUESTS_VALUE,
                           cs.ARGUMENTS_JMETER_WORKLOAD_CSV_COL_NAMES_VAR: cs.ARGUMENTS_JMETER_WORKLOAD_CSV_COL_NAMES_VALUE,
                           cs.ARGUMENTS_JMETER_RESULTS_PATH_VAR: cs.ARGUMENTS_JMETER_RESULTS_PATH_VALUE,
                           cs.ARGUMENTS_JMETER_WORKLOAD_CSV_COL_DELIMITER_VAR: cs.ARGUMENTS_JMETER_WORKLOAD_CSV_COL_DELIMITER_VALUE
                           }

    print "Processing File: " + generatedWorkloadFileList[count_workload_file_list]


    concurrent_users = str(int(row[cs.GENERATED_WORKLOAD_COL_HOURLY_CONCURRENT_USERS]))
    thread_loop = cs.ARGUMENTS_JMETER_LOOP_PER_THREAD_VALUE
    thread_rampup = cs.ARGUMENTS_JMETER_THREAD_RAMPUP_VALUE
    workload_file_path = cs.ARGUMENTS_JMETER_WORKLOAD_CSV_PATH_VALUE + generatedWorkloadFileList[count_workload_file_list]
    workload_file_num_csv_rows = str(len(pd.read_csv(cs.DATA_LOCAL_PATH + generatedWorkloadFileList[count_workload_file_list], delimiter=' ')))
    hourly_sum_requests = str(int(row[cs.GENERATED_WORKLOAD_COL_SUM_REQS]))

    argument_properties[cs.ARGUMENTS_JMETER_NUMBER_THREADS_VAR] = concurrent_users
    argument_properties[cs.ARGUMENTS_JMETER_LOOP_PER_THREAD_VAR] = thread_loop
    argument_properties[cs.ARGUMENTS_JMETER_THREAD_RAMPUP_VAR] = thread_rampup
    argument_properties[cs.ARGUMENTS_JMETER_WORKLOAD_CSV_PATH_VAR] = workload_file_path
    argument_properties[cs.ARGUMENTS_JMETER_WORKLOAD_CSV_NUM_ROWS_VAR] = workload_file_num_csv_rows

    with open(cs.LOAD_TEST_CONFIG_FILE, 'w+') as fp:
      jprops.store_properties(fp, config_properties)

    with open(cs.LOAD_TEST_ARGUMENTS_FILE, 'w+') as fp:
      jprops.store_properties(fp, argument_properties)

    config_properties_file_path = cs.LOAD_TEST_CONFIG_FILE
    arguments_properties_file_path = cs.LOAD_TEST_ARGUMENTS_FILE

    #subprocess.call(['java', '-jar', cs.JAR_LOAD_TEST_PATH, config_properties_file_path, arguments_properties_file_path])

    ##### Alternative Approach using directly the JMeter JAR


    jmeter_test_plan = cs.CONFIG_TEST_PLAN_PATH_VALUE

    # Creating directory for the scenario results

    if not os.path.exists(cs.ARGUMENTS_JMETER_RESULTS_PATH_VALUE + '/' + cs.ARGUMENTS_JMETER_SCENARIO_ID_VALUE):
        os.makedirs(cs.ARGUMENTS_JMETER_RESULTS_PATH_VALUE + '/' + cs.ARGUMENTS_JMETER_SCENARIO_ID_VALUE)

    jmeter_results_file_path = cs.ARGUMENTS_JMETER_RESULTS_PATH_VALUE + '/' + cs.ARGUMENTS_JMETER_SCENARIO_ID_VALUE + \
                               '/' + scenario_id_value + "_" + cs.ARGUMENTS_JMETER_ROUND_ID_VALUE + ".jtl"

    print scenario_id_value
    print jmeter_results_file_path
    config_variables = ['-J' + cs.ARGUMENTS_JMETER_HTTP_HOST_VAR + '=' + cs.ARGUMENTS_JMETER_HTTP_HOST_VALUE,
                        '-J' + cs.ARGUMENTS_JMETER_HTTP_PORT_VAR + '=' + cs.ARGUMENTS_JMETER_HTTP_PORT_VALUE,
                        '-J' + cs.ARGUMENTS_JMETER_HTTP_PATH_VAR + '=' + cs.ARGUMENTS_JMETER_HTTP_PATH_VALUE,
                        '-J' + cs.ARGUMENTS_JMETER_NUMBER_THREADS_VAR + '=' + concurrent_users,
                        '-J' + cs.ARGUMENTS_JMETER_LOOP_PER_THREAD_VAR + '=' + thread_loop,
                        '-J' + cs.ARGUMENTS_JMETER_THREAD_RAMPUP_VAR + '=' + thread_rampup,
                        '-J' + cs.ARGUMENTS_JMETER_WORKLOAD_CSV_PATH_VAR + '=' + workload_file_path,
                        '-J' + cs.ARGUMENTS_JMETER_WORKLOAD_CSV_NUM_ROWS_VAR + '=' + workload_file_num_csv_rows,
                        '-J' + cs.ARGUMENTS_JMETER_DELAY_BETWEEN_REQUESTS_VAR + '=' + cs.ARGUMENTS_JMETER_DELAY_BETWEEN_REQUESTS_VALUE,
                        '-J' + cs.ARGUMENTS_JMETER_ROUND_ID_VAR + '=' + cs.ARGUMENTS_JMETER_ROUND_ID_VALUE,
                        '-J' + cs.ARGUMENTS_JMETER_SCENARIO_ID_VAR + '=' + scenario_id_value,
                        '-J' + cs.ARGUMENTS_JMETER_WORKLOAD_CSV_COL_NAMES_VAR + "=" + cs.ARGUMENTS_JMETER_WORKLOAD_CSV_COL_NAMES_VALUE,
                        '-J' + cs.ARGUMENTS_JMETER_WORKLOAD_CSV_COL_DELIMITER_VAR + "=" + cs.ARGUMENTS_JMETER_WORKLOAD_CSV_COL_DELIMITER_VALUE]


    jmeter_jar_path = [cs.CONFIG_JMETER_PATH_VALUE + '/bin/ApacheJMeter.jar']
    env = dict(os.environ)
    env['JAVA_OPTS'] = '-Xmx8192m -Xms1024m'

    print env
    #subprocess.call(['java', '-jar'] + jmeter_jar_path + ['-n'] + config_variables + ['-t', jmeter_test_plan, '-l', jmeter_results_file_path])



    count_workload_file_list += 1
    break



# Aggregate the summary report files
# 1) Be able to process the results for each day. The output generated file must follow the same file naming property as the generated load
# 2) Extract Statistics, e.g. mean response time, mean number of errors

#with open('resources/arguments.properties.template') as fp:
#  properties = jprops.load_properties(fp)

#x = {'y': '1', 'z': '2'}
#with open('out.properties', 'w') as fp:
#  jprops.store_properties(fp, x)

#print properties