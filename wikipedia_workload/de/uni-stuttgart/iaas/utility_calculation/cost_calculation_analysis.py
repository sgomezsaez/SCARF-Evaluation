import cost_calculation as cc
import constants as cs
import pandas as pd
import math

def createFileList(results_path, scenario_list, scenario_file):
    fileList = []
    for i in scenario_list:
        fileList.append(results_path + i[0] + '/' + scenario_file)
    return fileList




def calculate_cost_scenario(experiment_scenario, summary_file_path):

    df = pd.read_csv(summary_file_path, delimiter=',')
    total_bytes_GB = df[cs.HOUR_SUMMARY_SUM_BYTES_TRANSFERRED].sum() / math.pow(2,30)
    total_duration_hours = df[cs.HOUR_SUMMARY_TIMESTAMP_DURATION].sum() / 3600

    print "Scenario: %s - Bytes Transferred: %f Duration = %f" %(experiment_scenario, total_bytes_GB, total_duration_hours)

    if experiment_scenario == 'T1':
        vm_frontend = cc.calculate_price_aws_vm(cs.AWS_EC2_VM_M4_LARGE, 1, total_duration_hours, 1, 10, total_bytes_GB)
        vm_backend = cc.calculate_price_aws_vm_internal(cs.AWS_EC2_VM_M4_LARGE, 1, total_duration_hours, 1, 100, total_bytes_GB)
        return vm_frontend + vm_backend
    if experiment_scenario == 'T2':
        vm_full_stack = cc.calculate_price_aws_vm(cs.AWS_EC2_VM_M4_XLARGE, 1, total_duration_hours, 1, 100, total_bytes_GB)
        return vm_full_stack
    if experiment_scenario == 'T3':
        vm_frontend = cc.calculate_price_aws_vm(cs.AWS_EC2_VM_M4_LARGE, 1, total_duration_hours, 1, 10, total_bytes_GB)
        rds_backend = cc.calculate_price_aws_rds(cs.AWS_RDS_M4_LARGE, 1, total_duration_hours, 1, 100, 0)
        return vm_frontend + rds_backend
    if experiment_scenario == 'T4':
        rds_backend = cc.calculate_price_aws_rds(cs.AWS_RDS_M4_LARGE, 1, total_duration_hours, 1, 100, 0)
        vm_frontend = cc.calculate_price_aws_beanstalk(cs.AWS_EC2_VM_T2_SMALL, 2, total_duration_hours, 1, 20, total_bytes_GB, 1)
        return vm_frontend + rds_backend
    if experiment_scenario == 'T5':
        rds_backend = cc.calculate_price_aws_rds(cs.AWS_RDS_M4_LARGE, 1, total_duration_hours, 1, 100, 0)
        cluster_frontend = cc.calculate_price_aws_ecs(cs.AWS_EC2_VM_T2_SMALL, 2, total_duration_hours, 1, 20, total_bytes_GB, 1)
        return cluster_frontend + rds_backend
    if experiment_scenario == 'T6':
        vm_frontend = cc.calculate_price_azure_vm(cs.AZURE_VM_DS2, 1, total_duration_hours, 1, 10, total_bytes_GB)
        vm_backend = cc.calculate_price_azure_vm(cs.AZURE_VM_DS2, 1, total_duration_hours, 1, 100, 0)
        return vm_frontend + vm_backend
    if experiment_scenario == 'T7':
        vm_full_stack = cc.calculate_price_azure_vm(cs.AZURE_VM_DS3, 1, total_duration_hours, 1, 100, total_bytes_GB)
        return vm_full_stack
    if experiment_scenario == 'T8':
        cluster_frontend = cc.calculate_price_azure_container(cs.AZURE_VM_DS2, cs.AZURE_VM_DS1, 2, total_duration_hours, 1, 10, total_bytes_GB)
        vm_backend = cc.calculate_price_azure_vm(cs.AZURE_VM_DS2, 1, total_duration_hours, 1, 20, 0)
        return cluster_frontend + vm_backend


def calculate_cost_scenarios():
    file_list = createFileList(cs.EXP_RESULTS_DATA_PATH, cs.EXP_RESULTS_DATA_SCENARIOS, cs.SUMMARY_HOURLY_RESULTS_OUTPUT_FILE_NAME + '.csv')
    scenario_count = 0
    scenario_costs = []

    for i in file_list:
       scenario_costs.append([cs.EXP_RESULTS_DATA_SCENARIOS[scenario_count][0], calculate_cost_scenario(cs.EXP_RESULTS_DATA_SCENARIOS[scenario_count][0], i)])
       scenario_count += 1

    return scenario_costs


#print calculate_cost_scenarios()