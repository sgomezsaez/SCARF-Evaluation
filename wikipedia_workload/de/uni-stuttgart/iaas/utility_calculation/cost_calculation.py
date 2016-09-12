import constants as cs

def calculate_price_aws_vm (vm_type, num_vms, usage_duration_hours, num_months, storage_size, data_transfer):

    # VM Price
    vm_price_per_hour = 0

    if vm_type == cs.AWS_EC2_VM_T2_SMALL:
        vm_price_per_hour = cs.AWS_EC2_VM_T2_SMALL_PRICE * num_vms
    elif vm_type == cs.AWS_EC2_VM_M4_LARGE:
        vm_price_per_hour = cs.AWS_EC2_VM_M4_LARGE_PRICE * num_vms
    elif vm_type == cs.AWS_EC2_VM_M4_XLARGE:
        vm_price_per_hour = cs.AWS_EC2_VM_M4_XLARGE_PRICE * num_vms
    else:
        vm_price_per_hour = 0

    vm_price = vm_price_per_hour * usage_duration_hours

    # Storage Price per GB Month
    storage_price = num_vms * cs.AWS_EC2_STORAGE_GB_MONTH_PRICE * storage_size * num_months

    # Data Transfer
    if data_transfer > 0:
        data_transfer_egress = float(data_transfer) - cs.AWS_EC2_DATA_TRANSFER_FREE_GB
        data_transfer_price = cs.AWS_EC2_DATA_TRANSFER_GB_PRICE * data_transfer_egress
    else:
        data_transfer_price = 0

    return vm_price + storage_price + data_transfer_price

def calculate_price_aws_vm_internal (vm_type, num_vms, usage_duration_hours, num_months, storage_size, data_transfer):

    # VM Price
    vm_price_per_hour = 0

    if vm_type == cs.AWS_EC2_VM_T2_SMALL:
        vm_price_per_hour = cs.AWS_EC2_VM_T2_SMALL_PRICE * num_vms
    elif vm_type == cs.AWS_EC2_VM_M4_LARGE:
        vm_price_per_hour = cs.AWS_EC2_VM_M4_LARGE_PRICE * num_vms
    elif vm_type == cs.AWS_EC2_VM_M4_XLARGE:
        vm_price_per_hour = cs.AWS_EC2_VM_M4_XLARGE_PRICE * num_vms
    else:
        vm_price_per_hour = 0

    vm_price = vm_price_per_hour * usage_duration_hours

    # Storage Price per GB Month
    storage_price = num_vms * cs.AWS_EC2_STORAGE_GB_MONTH_PRICE * storage_size * num_months

    return vm_price + storage_price

def calculate_price_aws_rds (rds_type, num_rds, usage_duration_hours, num_months, storage_size, data_transfer_out):
    rds_price_per_hour = 0

    if rds_type == cs.AWS_RDS_M4_LARGE:
        rds_price_per_hour = cs.AWS_RDS_DB_M4_LARGE_PRICE * num_rds

    rds_price = rds_price_per_hour * num_rds * usage_duration_hours

    storage_price = cs.AWS_RDS_STORAGE_GB_MONTH_PRICE * storage_size * num_months

    if data_transfer_out > 0:
        data_transfer_egress = float(data_transfer_out) - cs.AWS_RDS_DATA_TRANSFER_FREE_GB
        data_transfer_price = cs.AWS_RDS_DATA_TRANSFER_GB_PRICE * data_transfer_egress
    else:
        data_transfer_price = 0


    return rds_price + storage_price + data_transfer_price

def calculate_price_aws_beanstalk (vm_type, num_vms, usage_duration_hours, num_months, storage_size, data_transfer, num_elb):

    # VM Price
    vm_price_per_hour = 0

    vm_price = calculate_price_aws_vm(vm_type, num_vms, usage_duration_hours, num_months, storage_size, data_transfer)

    # Load Balancing Price
    elb_price = num_elb * (cs.AWS_LB_PRICE * usage_duration_hours + data_transfer * cs.AWS_LB_DATA_TRANSFER_GB_PRICE)


    return vm_price + elb_price

def calculate_price_aws_ecs (vm_type, num_vms, usage_duration_hours, num_months, storage_size, data_transfer, num_elb):

    # VM Price
    vm_price_per_hour = 0

    vm_price = calculate_price_aws_vm(vm_type, num_vms, usage_duration_hours, num_months, storage_size, data_transfer)

    # Load Balancing Price
    elb_price = num_elb * (cs.AWS_LB_PRICE * usage_duration_hours + data_transfer * cs.AWS_LB_DATA_TRANSFER_GB_PRICE)


    return vm_price + elb_price

def calculate_price_azure_vm (vm_type, num_vms, usage_duration_hours, num_months, storage_size, data_transfer):

    # VM Price
    vm_price_per_hour = 0

    if vm_type == cs.AZURE_VM_DS1:
        vm_price_per_hour = cs.AZURE_VM_DS1_PRICE * num_vms
    elif vm_type == cs.AZURE_VM_DS2:
        vm_price_per_hour = cs.AZURE_VM_DS2_PRICE * num_vms
    elif vm_type == cs.AZURE_VM_DS3:
        vm_price_per_hour = cs.AZURE_VM_DS3_PRICE * num_vms
    else:
        vm_price_per_hour = 0

    vm_price = vm_price_per_hour * usage_duration_hours

    # Data Transfer
    if data_transfer > 0:
        data_transfer_egress = float(data_transfer) - cs.AZURE_DATA_TRANSFER_FREE_GB
        data_transfer_price = cs.AZURE_EC2_DATA_TRANSFER_GB_PRICE * data_transfer_egress
    else:
        data_transfer_price = 0


    return vm_price + data_transfer_price

def calculate_price_azure_container (vm_type_master, vm_type_agents, num_vms_agents, usage_duration_hours, num_months, storage_size, data_transfer):

    # VM Price
    vm_price_master_per_hour = 0

    if vm_type_master == cs.AZURE_VM_DS1:
        vm_price_master_per_hour = cs.AZURE_VM_DS1_PRICE * 1
    elif vm_type_master == cs.AZURE_VM_DS2:
        vm_price_master_per_hour = cs.AZURE_VM_DS2_PRICE * 1
    elif vm_type_master == cs.AZURE_VM_DS3:
        vm_price_master_per_hour = cs.AZURE_VM_DS3_PRICE * 1
    else:
        vm_price_master_per_hour = 0

    vm_price_master = vm_price_master_per_hour * usage_duration_hours

    vm_price_agent_per_hour = 0

    if vm_type_agents == cs.AZURE_VM_DS1:
        vm_price_agent_per_hour = cs.AZURE_VM_DS1_PRICE * num_vms_agents
    elif vm_type_agents == cs.AZURE_VM_DS2:
        vm_price_agent_per_hour = cs.AZURE_VM_DS2_PRICE * num_vms_agents
    elif vm_type_agents == cs.AZURE_VM_DS3:
        vm_price_agent_per_hour = cs.AZURE_VM_DS3_PRICE * num_vms_agents
    else:
        vm_price_agent_per_hour = 0

    vm_price_agents = vm_price_master_per_hour * usage_duration_hours

    # Data Transfer
    if data_transfer > 0:
        data_transfer_egress = float(data_transfer) - cs.AZURE_DATA_TRANSFER_FREE_GB
        data_transfer_price = cs.AZURE_EC2_DATA_TRANSFER_GB_PRICE * data_transfer_egress
    else:
        data_transfer_price = 0

    return vm_price_master + vm_price_agents + data_transfer_price