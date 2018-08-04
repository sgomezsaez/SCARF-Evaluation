import constants as cs
import cost_calculation_analysis as cc
import pandas as pd

def createFileList(results_path, scenario_list, scenario_file):
    fileList = []
    for i in scenario_list:
        fileList.append(results_path + i[0] + '/' + scenario_file)
    return fileList

def calculate_revenue(workload_profiles):
    out_rev = []

    for i in workload_profiles:
        workload_id = i['ID']
        workload_probability = i['Probability']
        workload_error_rate = i['Avg_transaction_error_rate']
        workload_transaction_per_user = i['Avg_transaction_per_users']
        workload_duration = i['Duration']
        workload_revenue_per_user = i['Avg_revenue_per_user']
        workload_num_users = i['Num_users']

        revenue = workload_probability * (((1 - workload_error_rate) * workload_transaction_per_user) *
                                          workload_duration * workload_revenue_per_user * workload_num_users)
        out_rev.append({'ID': workload_id, 'Revenue': float(revenue)})

    return out_rev


def calculate_satisfaction(workload_profiles):
    out_sat = []
    sat = 0

    for i in workload_profiles:
        latency_greater_40s = i['requests_latency_greater_40']
        requests_unsuccessful = i['requests_unsuccessful']
        sat += 1 - (latency_greater_40s + requests_unsuccessful) / i['Total_requests']

        print "Reqs Greater 40s:"
        print latency_greater_40s
        print "Reqs Unsuccessful:"
        print requests_unsuccessful
        print "Satisfaction:"
        print "Total Requests:"
        print i['Total_requests']
        print sat

    sat = sat / len(workload_profiles)
    print "Satisfaction:"
    print sat
    return float(sat)

def calculate_availability(distribution_id):
    return 99.95

def calculate_utility(distribution_id, workload_profiles):

    cost_scenarios = cc.calculate_cost_scenarios()
    cost_distribution = 0.0

    for i in cost_scenarios:
        if i[0] == distribution_id:
            cost_distribution = i[1]

    revenues = calculate_revenue(workload_profiles)
    total_revenue = 0
    for i in revenues:
        total_revenue += i['Revenue']

    utility = total_revenue * calculate_satisfaction(workload_profiles) - cost_distribution

    return [distribution_id, utility]


def calculate_utility_distributions():
    file_list = createFileList(cs.EXP_RESULTS_DATA_PATH, cs.EXP_RESULTS_DATA_SCENARIOS, cs.SUMMARY_HOURLY_RESULTS_OUTPUT_FILE_NAME + '.csv')
    df_workload_distribution = pd.read_csv(cs.WORKLOAD_DISTRIBUTION_DATA, delimiter=' ')
    out = []

    scenario_count = 0
    for i in file_list:
        df_results = pd.read_csv(i, delimiter=',')

        # Probability of workload is set to 1, since we assume a monthly workload
        probability = 1
        # tranaction error rate is the number of failed requests in the experiment
        transaction_error_rate = 1 - (float(df_results[cs.HOUR_SUMMARY_SUM_REQS_SUCCESS].sum()) / float(df_results[cs.HOUR_SUMMARY_SUM_ALL_REQS].sum()))
        # average transactions per user depends on the total number of concurrent users and all the requests
        total_concurrent_users = df_workload_distribution[cs.GENERATED_WORKLOAD_COL_HOURLY_CONCURRENT_USERS].sum()
        total_num_requests = df_results[cs.HOUR_SUMMARY_SUM_ALL_REQS].sum()


        #requests_per_user = total_num_requests / total_concurrent_users

        throughput_month = 1 / ((df_results[cs.HOUR_SUMMARY_AVG_LATENCY] / (1000 * 60 * 60 * 24 * 31)).describe().iloc[1])
        requests_per_user = throughput_month / total_concurrent_users


        time_interval = 1

        cs.WORKLOAD_PROFILE['Avg_transaction_error_rate'] = transaction_error_rate
        cs.WORKLOAD_PROFILE['Avg_transaction_per_users'] = requests_per_user
        cs.WORKLOAD_PROFILE['Duration'] = time_interval
        cs.WORKLOAD_PROFILE['Num_users'] = total_concurrent_users
        cs.WORKLOAD_PROFILE['Sum_req_success'] = float(df_results[cs.HOUR_SUMMARY_SUM_REQS_SUCCESS].sum())
        cs.WORKLOAD_PROFILE['Total_requests'] = float(df_results[cs.HOUR_SUMMARY_SUM_ALL_REQS].sum())

        # Preparing Data for Satisfaction calculation: requests which took longer than 40 seconds or requests that failed
        cs.WORKLOAD_PROFILE['requests_latency_greater_40'] = df_results[cs.HOUR_SUMMARY_SUM_REQS_LATENCY_GREATER_40].sum()
        cs.WORKLOAD_PROFILE['requests_unsuccessful'] = df_results[cs.HOUR_SUMMARY_SUM_RESP_500].sum()

        out.append(calculate_utility(cs.EXP_RESULTS_DATA_SCENARIOS[scenario_count][0], [cs.WORKLOAD_PROFILE]))
        scenario_count += 1


    #return sorted(out,key=lambda l:l[1], reverse=True)
    return out

def calculate_utility_distributions_cost():
    cost_scenarios = cc.calculate_cost_scenarios()

    max_cost = sorted(cost_scenarios,key=lambda l:l[1], reverse=True)[0]

    print cost_scenarios

    cost_scenarios_cost_utility = []
    for i in cost_scenarios:
        cost_scenarios_cost_utility.append([i[0], max_cost[1] - i[1]])

    #return sorted(cost_scenarios_cost_utility,key=lambda l:l[1], reverse=True)
    return cost_scenarios_cost_utility

def calculate_utility_distributions_availability():
    out = []
    for i in cs.EXP_RESULTS_DATA_SCENARIOS:
        out.append([i[0], cs.AWS_AVAILABILITY_SLA])

    #return sorted(out,key=lambda l:l[1], reverse=False)
    return out



#print calculate_utility('T1', cs.WORKLOAD_PROFILES)
#print calculate_utility_distributions()
#print sorted(calculate_utility_distributions(),key=lambda l:l[1], reverse=True)
#print calculate_utility_distributions_cost()
print sorted(calculate_utility_distributions_cost(),key=lambda l:l[1], reverse=True)
#print calculate_utility_distributions_availability()
#print sorted(calculate_utility_distributions_availability(),key=lambda l:l[1], reverse=False)