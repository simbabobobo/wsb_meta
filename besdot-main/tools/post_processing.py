"""
Tool to analyse the output csv from optimization
"""

import os
import copy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Attention! The elec_list and heat_list use the name from topology
# matrix, for different scenario the name for each component may change.
# Need to check for every scenario or fix the component name in topology.
elec_comp_list = ['heat_pump', 'pv', 'bat', 'e_grid', 'e_boi', 'e_cns',
                  'chp']
heat_comp_list = ['heat_pump', 'therm_cns', 'water_tes', 'solar_coll',
                  'boi', 'e_boi', 'chp']
elec_sink_tuple = ('heat_pump', 'bat', 'e_grid', 'e_boi')
heat_sink_tuple = 'water_tes'
#plt.rcParams['axes.unicode_minus']=False

# base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# opt_output_path = os.path.join(base_path, 'data', 'opt_output')


def find_element(output_df):
    """find all elements in dataframe, the variables with same name but
    different time step would be stored in a list"""
    output_df['var_pre'] = output_df['var'].map(lambda x: x.split('[')[0])
    all_elements = output_df['var_pre'].tolist()
    element_list = list(set(all_elements))  # delete duplicate elements

    elements_dict = {}
    for element in element_list:
        element_df = output_df.loc[output_df['var_pre'] == element]
        values = element_df['value'].tolist()
        elements_dict[element] = values

    return elements_dict


def find_size(csv_file):
    """
    Search for the results of each component in csv file.
    """
    output_df = pd.read_csv(csv_file)
    elements_dict = find_element(output_df)
    size_dict = {}
    for element in elements_dict:
        if len(elements_dict[element]) == 1:
            if 'size' in element and not np.isnan(elements_dict[element][0]):
                size_dict[element] = elements_dict[element][0]
                print('The size of', element, 'is', size_dict[element])
            if 'volume' in element and not np.isnan(
                    elements_dict[element][0]):
                size_dict[element] = elements_dict[element][0]
                print('The volume of', element, 'is', size_dict[element])


def sum_flow(csv_file, flow_name):
    """
    Calculate the sum of a specific energy flow in result file.
    """
    output_df = pd.read_csv(csv_file)
    elements_dict = find_element(output_df)
    flow_list = elements_dict[flow_name]
    print(sum(flow_list))


def find_max_timestep(csv_file, profile_name):
    """Search the maximal value of a profile and return the timestep of the
    maximal value. This function could be used to analysis the situation,
    how the peak demand is filled.
    Using find_element().keys() to find the name of the wanted profile"""
    output_df = pd.read_csv(csv_file)
    elements_dict = find_element(output_df)
    profile = elements_dict[profile_name]
    max_value = max(profile)
    index_max = profile.index(max(profile))

    return max_value, index_max


def save_timeseries(csv_file):
    """Take the time series from output file and save them as an individual
    csv file, to reduce the analysis time cost."""
    output_df = pd.read_csv(csv_file)
    elements_dict = find_element(output_df)
    new_df = pd.DataFrame()

    for item in elements_dict.keys():
        if len(elements_dict[item]) > 1:
            new_df = pd.DataFrame(index=range(len(elements_dict[item])))
            break

    for item in elements_dict.keys():
        if len(elements_dict[item]) > 1:
            new_df[item] = elements_dict[item]

    # print(new_df)
    output_path = os.path.split(csv_file)
    timeseries_path = os.path.join(output_path[0], 'timeseries.csv')
    new_df.to_csv(timeseries_path)


def plot_all(csv_file, time_interval, save_path=None):
    """

    Args:
        csv_file:
        time_interval: list, first element is the beginning time for plot and
        second element is the end time for plot
    """
    output_df = pd.read_csv(csv_file)
    elements_dict = find_element(output_df)
    size_dict = {}
    for element in elements_dict:
        if len(elements_dict[element]) == 1:
            if 'size' in element and not np.isnan(elements_dict[element][0]):
                size_dict[element] = elements_dict[element][0]
                print('The size of', element, 'is', size_dict[element])
        else:
            if sum(elements_dict[element]) > 0.001 or sum(elements_dict[
                                                              element]) < 0.001:
                plot_single(element,
                            elements_dict[element][time_interval[0]:
                                                   time_interval[1]],
                            save_path)


def plot_single(name, profile, plot_path=None):
    """
    name: the name for a variable in optimization model and results.
    profile: already taken fom the result dictionary and the time steps are
    taken into account as well.
    plot_path: the folder address for all plots, it should be the same folder
    for model and optimization results.
    """
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    ax.plot(profile, linewidth=2, color='r', linestyle='-')
    ax.set_title('Profile of ' + name)
    ax.set_xlabel('Hours [h]')
    if 'mass' in name:
        ax.set_ylabel('Mass [KG/H]', fontsize=12)
    elif 'temp' in name:
        ax.set_ylabel('Temperature [°C]', fontsize=12)
    elif 'pmv' in name:
        ax.set_ylabel('PMV', fontsize=12)
    else:
        ax.set_ylabel('Power [KW]', fontsize=12)

    if 'pmv' in name:
        ax.set_xlim(xmin=0)
        ax.set_ylim(ymin=-3, ymax=3)
    else:
        ax.set_xlim(xmin=0)
        ax.set_ylim(ymin=0, ymax=max(profile) * 1.2)
    plt.grid()

    if plot_path is not None:
        plt.savefig(os.path.join(plot_path, name+'.png'))
    else:
        plt.show()
    plt.close()


def plot_double_24h(csv_file, comp_name1, comp_name2):
    plot_output = os.path.join(opt_output_path, 'plot', 'profile of ' +
                               comp_name1)
    df = pd.read_csv(csv_file)
    data1 = df[df['var'].str.contains(comp_name1 + '_' + comp_name2 + '_temp')]
    data1 = data1.reset_index(drop=True)
    profile_temp = data1['value']
    data2 = df[df['var'].str.contains(comp_name2 + '_' + comp_name1 + '_temp')]
    data2 = data2.reset_index(drop=True)
    profile_return_temp = data2['value']
    data3 = df[(df['var'].str.contains('input_')) & (df['var'].str.contains(
        comp_name1))]
    data3 = data3.reset_index(drop=True)
    profile_inputpower = data3['value']
    data4 = df[(df['var'].str.contains('output_')) & (df['var'].str.contains(
        comp_name1))]
    data4 = data4.reset_index(drop=True)
    profile_outputpower = data4['value']
    fig = plt.figure(figsize=(6.5, 5.5))
    ax = fig.add_subplot(111)
    ax.plot(profile_inputpower, '-', label='input')
    ax.plot(profile_outputpower, '-', label='output')
    ax2 = ax.twinx()
    ax2.plot(profile_temp, '-r', label=comp_name1 + '_' + comp_name2 + '_temp')
    ax2.plot(profile_return_temp, '-g', label=comp_name2 + '_' + comp_name1 +
                                              '_temp')
    ax.legend(loc='center left', bbox_to_anchor=(0, 1.07), ncol=1)
    ax.grid()
    ax.set_xlabel("Time (h)")
    ax.set_title('Profile of ' + comp_name1, fontsize=9)
    ax.set_ylabel(r"Power (KW)")
    ax2.set_ylabel(r"Temperature ($^\circ$C)")
    ax.set_xlim(xmax=len(profile_temp))
    ax2.legend(loc='upper right', bbox_to_anchor=(1.1, 1.15), ncol=1)
    plt.savefig(plot_output)


def plot_double(csv_file, comp_name1, comp_name2, time_step, inputenergy,
                outputenergy):
    #plot_output = os.path.join(opt_output_path, 'plot', 'profile of ' +
    #                           comp_name1)
    df = pd.read_csv(csv_file)
    #data1 = df[df['var'].str.contains(comp_name1 + '_' + comp_name2 + '_temp')]
    #data1 = data1.reset_index(drop=True)
    #profile_temp = data1['value']
    profile_temp_original, profile_return_temp_original, \
    profile_inputpower_original, profile_outputpower_original = \
        get_info_for_figu(csv_file, comp_name1, comp_name2, time_step,
                          inputenergy, outputenergy)
    for i in range(1, len(profile_temp_original)+1):
        if i < len(profile_temp_original)+1:
            plot_output = os.path.join(opt_output_path, 'plot', 'profile of ' +
                                       comp_name1 + ' day ' + str(i))
            profile_temp = profile_temp_original[i-1]
            profile_return_temp = profile_return_temp_original[i-1]
            profile_inputpower = profile_inputpower_original[i-1]
            profile_outputpower = profile_outputpower_original[i-1]
            fig = plt.figure(figsize=(6.5, 5.5))
            ax = fig.add_subplot(111)
            ax.plot(profile_inputpower, '-', label='input')
            ax.plot(profile_outputpower, '--', label='output')
            ax2 = ax.twinx()
            ax2.plot(profile_temp, '-r',
                     label=comp_name1 + '_' + comp_name2 + '_temp')
            ax2.plot(profile_return_temp, '-g',
                     label=comp_name2 + '_' + comp_name1 +
                           '_temp')
            ax.legend(loc='center left', bbox_to_anchor=(0, 1.07), ncol=1)
            ax.grid()
            ax.set_xlabel("Time (h)")
            ax.set_title('Profile of ' + comp_name1 + ' day ' + str(i),
                         fontsize=9)
            ax.set_ylabel(r"Power (KW)")
            ax2.set_ylabel(r"Temperature ($^\circ$C)")
            ax.set_xlim(xmax=24)
            ax2.legend(loc='upper right', bbox_to_anchor=(1.1, 1.15), ncol=1)
            plt.savefig(plot_output)
            i = i + 1


def get_info_for_figu(csv_file, comp_name1, comp_name2, time_step,
                             inputenergy, outputenergy):
    df = pd.read_csv(csv_file)
    name1 = comp_name1 + '_' + comp_name2 + '_temp[1]'
    name2 = comp_name2 + '_' + comp_name1 + '_temp[1]'
    name3 = 'input_' + inputenergy + '_' + comp_name1 + '[1]'
    name4 = 'output_' + outputenergy + '_' + comp_name1 + '[1]'
    part = int(8760/time_step)
    temp = []
    return_temp = []
    input_power = []
    output_power = []
    pa = []
    pa_co = 1
    for i in range(1, 313):
        if pa_co != part:
            pa.append(df["value"][df[df["var"] == str(name1[:-2] + str(i)+"]")].
                      index].to_list()[0])
            pa_co += 1
        else:
            pa_co = 1
            pa.append(df["value"][df[df["var"] == str(name1[:-2] + str(i)+"]")].
                      index].to_list()[0])
            temp.append(pa)
            pa = []
    for i in range(1, 313):
        if pa_co != part:
            pa.append(
                df["value"][df[df["var"] == str(name2[:-2] + str(i) + "]")].
                index].to_list()[0])
            pa_co += 1
        else:
            pa_co = 1
            pa.append(
                df["value"][df[df["var"] == str(name2[:-2] + str(i) + "]")].
                index].to_list()[0])
            return_temp.append(pa)
            pa = []
    for i in range(1, 313):
        if pa_co != part:
            pa.append(
                df["value"][df[df["var"] == str(name3[:-2] + str(i) + "]")].
                index].to_list()[0])
            pa_co += 1
        else:
            pa_co = 1
            pa.append(
                df["value"][df[df["var"] == str(name3[:-2] + str(i) + "]")].
                index].to_list()[0])
            input_power.append(pa)
            pa = []
    for i in range(1, 313):
        if pa_co != part:
            pa.append(
                df["value"][df[df["var"] == str(name4[:-2] + str(i) + "]")].
                index].to_list()[0])
            pa_co += 1
        else:
            pa_co = 1
            pa.append(
                df["value"][df[df["var"] == str(name4[:-2] + str(i) + "]")].
                index].to_list()[0])
            output_power.append(pa)
            pa = []
    return temp, return_temp, input_power, output_power


def get_short_profiles(start_time, time_step, csv_file):
    def combine_items(ori_list):
        new_list = []
        for nr_1 in range(len(ori_list)):
            for nr_2 in range(len(ori_list)):
                if nr_2 != nr_1:
                    new_list.append(ori_list[nr_1] + '_' + ori_list[nr_2])
        return new_list

    elec_list = combine_items(elec_comp_list)
    heat_list = combine_items(heat_comp_list)

    output_df = pd.read_csv(csv_file)
    elements_dict = find_element(output_df)

    short_elec_df = pd.DataFrame()
    short_heat_df = pd.DataFrame()
    for element in elements_dict:
        if len(elements_dict[element]) == 1:
            pass
        else:
            if sum(elements_dict[element][
                   start_time: start_time + time_step]) == 0:
                pass
            else:
                if element in elec_list:
                    short_elec_df.insert(0, element,
                                         elements_dict[element][
                                         start_time: start_time + time_step])
                elif element in heat_list:
                    short_heat_df.insert(0, element,
                                         elements_dict[element][
                                         start_time: start_time + time_step])

    return short_elec_df, short_heat_df


def plot_short_time(start_time, time_step, csv_file, demand_heat, demand_elec):
    """Plot only short time like one day in a graphic"""
    elec_df, heat_df = get_short_profiles(start_time, time_step, csv_file)
    # print(elec_df)
    # print(heat_df)

    demand_heat = demand_heat[start_time: start_time + time_step]
    demand_elec = demand_elec[start_time: start_time + time_step]

    # plot for heat balance
    plot_step_profile(energy_type='heat', demand=demand_heat, profile=heat_df,
                      time_step=time_step)

    # plot for electricity balance
    plot_step_profile(energy_type='elec', demand=demand_elec, profile=elec_df,
                      time_step=time_step)


def plot_step_profile(energy_type, demand, profile, time_step):
    fig = plt.figure(figsize=(6, 5.5))
    ax = fig.add_subplot(1, 1, 1)

    time_steps = range(time_step)
    accumulate_series = pd.Series([0] * time_step)
    x_axis = np.linspace(0, time_step - 1, time_step)

    if energy_type == 'heat':
        sink_tuple = heat_sink_tuple
    elif energy_type == 'elec':
        sink_tuple = elec_sink_tuple
    else:
        sink_tuple = None

    order_heat = 1.5
    for device in profile.columns:
        if not device.endswith(sink_tuple):
            accumulate_series += profile[device]
            ax.step(time_steps, accumulate_series, where="post",
                    label=device, linewidth=2, zorder=order_heat)
            ax.fill_between(x_axis, accumulate_series,
                            step="post", zorder=order_heat)
            order_heat -= 0.1
    for device in profile.columns:
        if device.endswith(sink_tuple):
            last_series_heat = copy.deepcopy(accumulate_series)
            accumulate_series -= profile[device]
            ax.step(time_steps, accumulate_series, where="post",
                    linewidth=0.1, zorder=1.5)
            ax.fill_between(x_axis, last_series_heat, accumulate_series,
                            label=device, step="post", zorder=1.6,
                            hatch='///', alpha=0)
            order_heat -= 0.1
    ax.step(time_steps, demand, where="post", label='Bedarf', linestyle='--',
            linewidth=2, zorder=1.5)

    ax.set_ylabel('Leistung in kW')
    ax.set_xlim(0, 23)
    ax.set_ylim(0, None)
    ax.set_xlabel('Stunde')

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], loc='upper right')
    ax.grid(axis="y", alpha=0.6)
    ax.set_axisbelow(True)
    fig.suptitle(t='hourly profile', fontsize=18)
    plt.show()

    # plot_path = os.path.join(OUTPUTS_PATH, str(datetime.datetime.now(
    #     ).strftime('%Y-%m-%d_%H_%M_%S_')) + day + '.png')

    # plot_path = os.path.join(OUTPUTS_PATH, name + day + '.png')
    # plt.savefig(plot_path)
    # plt.close()


def plot_temp(name, profile):
    plot_output = os.path.join(opt_output_path, 'plot', 'Profile of ' + name)
    fig, ax = plt.subplots(figsize=(14, 14))
    #ax = fig.add_subplot(111)
    ax.plot(profile, linewidth=2, color='r', marker='o', linestyle='dashed')
    ax.set_title('Profile of ' + name, fontsize=24)
    ax.set_xlabel('Hours [h]', fontsize=24)
    if 'mass' in name:
        ax.set_ylabel('mass [KG/H]', fontsize=12)
    elif 'temp' in name:
        ax.set_ylabel('temperature [°]', fontsize=24)
    else:
        ax.set_ylabel('power [KW]', fontsize=12)

    ax.set_xlim(xmin=0)
    ax.set_ylim(ymin=0, ymax=max(profile)*1.2)

    plt.xticks([0, 2161, 4345, 6553, 8017],
               [r'$1.Jar.$', r'$1.Apr.$', r'$1.Jul.$', r'$1.Oct.$',
                r'$1.Dec.$'], fontsize=29)
    plt.yticks(fontsize=29)

    plt.grid()

    #plt.show()
    plt.savefig(plot_output)
    plt.close()


if __name__ == '__main__':
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    opt_output_path = os.path.join(base_path, 'data', 'opt_output')
    opt_output_0 = os.path.join(opt_output_path, 'project_3_0', 'result.csv')
    opt_output_1 = os.path.join(opt_output_path, 'project_3_1', 'result.csv')
    opt_output_2 = os.path.join(opt_output_path, 'project_3_3', 'result.csv')

    #############################################################
    # Search and get values
    #############################################################
    # output_df_0 = pd.read_csv(opt_output_0)
    # all_elements_0 = find_element(output_df_0)
    # opt_output_1 = pd.read_csv(opt_output_0)
    # opt_output_1 = find_element(opt_output_1)
    # print(all_elements)

    find_size(opt_output_0)
    print("====")
    find_size(opt_output_2)

    # find_max_timestep(opt_output, 'input_heat_therm_cns')

    # save_timeseries(opt_output)

    #############################################################
    # Plots
    #############################################################
    # if os.path.exists(os.path.join(opt_output_path, 'project_1')):
    #     pass
    # else:
    #     os.mkdir(os.path.join(opt_output_path, 'project_1'))
    # plot_all(opt_output, [624, 672],
    #          save_path=os.path.join(opt_output_path, 'project_1'))

    # plot_output = os.path.join(opt_output_path, 'plot')
    #
    # demand_input = os.path.join(base_path, 'data', 'denmark_energy_hub',
    #                             'energyprofile(kwh).csv')
    # demand_df = pd.read_csv(demand_input)
    # commercial_heat = demand_df['commercial heat'].astype('float64').values
    # resident_heat = demand_df['residential heat'].astype('float64').values
    # total_heat = commercial_heat + resident_heat
    # total_elec = demand_df['total electricity'].astype('float64').values
    #
    # # plot_all(opt_output)
    # plot_short_time(start_time=0, time_step=24, csv_file=opt_output,
    #                 demand_heat=total_heat, demand_elec=total_elec)

    # no_loss_result_file = os.path.join(base_path, 'data', 'opt_output',
    #                                    'project_28_no_loss_result.csv')
    # with_loss_result_file = os.path.join(base_path, 'data', 'opt_output',
    #                                      'project_28_with_loss_result.csv')
    # print('The size of project without loss:')
    # find_size(no_loss_result_file)
    # print('The size of porject with loss:')
    # find_size(with_loss_result_file)
    #
    # print('#################')
    #
    # print('The total input energy in battery without loss:')
    # sum_flow(no_loss_result_file, 'input_elec_bat')
    # print('The total output energy in battery without loss:')
    # sum_flow(no_loss_result_file, 'output_elec_bat')
    # print('The total input energy in battery with loss:')
    # sum_flow(with_loss_result_file, 'input_elec_bat')
    # print('The total output energy in battery with loss:')
    # sum_flow(with_loss_result_file, 'output_elec_bat')
