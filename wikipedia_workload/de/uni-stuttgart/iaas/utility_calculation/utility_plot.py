import utility_calculation as utility
import matplotlib.pyplot as plt
import numpy as np
import constants as cs
import itertools

def flip(items, ncol):
    return itertools.chain(*[items[i::ncol] for i in range(ncol)])

def bar_plot_utility(scenario_list, x_labels, plot_title, plot_output_file):
    utility_model = utility.calculate_utility_distributions()
    utility_cost = utility.calculate_utility_distributions_cost()
    utility_availability = utility.calculate_utility_distributions_availability()

    print "Utility Model"
    print utility_model
    print "Utility Cost"
    print utility_cost

    scenario_patterns = [ "/" , "\\" , "|" , "-" , "+" , "x", "o", "O", ".", "*" ]
    scenario_count = 0

    # Creating Plot
    fig1 = plt.figure(figsize=(7, 6))
    plt.suptitle(plot_title, fontsize=20)
    ax1 = fig1.add_subplot(111)

    # Create X Axis
    x_axis_list = []
    for i in x_labels:
        x_axis_list.append(i[0])

    width = 0.45

    x_axis_num = np.arange(1, len(x_axis_list) + 1)
    rects1 = ax1.bar(x_axis_num, [i[1] for i in utility_model], width, color='grey', hatch='++', label='Utility Model - Profitability', edgecolor='black', alpha=0.95)
    rects2 = ax1.bar(x_axis_num + width, [i[1] for i in utility_cost], width, color='grey', hatch='xx', label='Utility Model - Cost', edgecolor='black', alpha=0.95)
    #rects2 = ax1.bar(x_axis_num + width + width, [i[1] for i in utility_availability], width, color='grey', hatch='..', label='Utility Model - Availability', edgecolor='black', alpha=0.95)

    ax1.set_ylabel('utility (U\$)', fontsize=15)
    ax1.set_title(plot_title, fontsize=15)
    ax1.set_xticks(x_axis_num + width)
    ax1.set_xticklabels(x_axis_list, fontsize=15)
    ax1.grid(True)
    ax1.set_ylim([0,500])

    handles, labels = ax1.get_legend_handles_labels()
    plt.legend(flip(handles, 2), flip(labels, 2), bbox_to_anchor=(0.5, 1.05), loc=9, ncol=2, prop={'size':15})

    fig1.savefig(plot_output_file, format='pdf')

outputFile = cs.PLOT_RESULTS_DATA_PATH + cs.PLOT_UTILITY_COMPARISON_FILE
bar_plot_utility(cs.EXP_RESULTS_DATA_SCENARIOS, cs.EXP_RESULTS_DATA_SCENARIOS_LABELS, ' ', outputFile)