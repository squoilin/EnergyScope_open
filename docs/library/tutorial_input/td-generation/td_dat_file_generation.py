import csv
import numpy as np
import pandas as pd

def td_dat_file_generation(time_series, cluster_matrix, nbr_td, out_path):
    """Generate the .dat file for the typical days"""
    eud_params = {'Electricity (%_elec)': 'param electricity_time_series :',
                    'Space Heating (%_sh)': 'param heating_time_series :',
                    'Passanger mobility (%_pass)': 'param mob_pass_time_series :',
                    'Freight mobility (%_freight)': 'param mob_freight_time_series :'}
    # for resources timeseries that have only 1 tech linked to it
    res_params = {'PV': 'PV', 'Wind_onshore': 'WIND_ONSHORE', 'Wind_offshore': 'WIND_OFFSHORE',
                    'Hydro_river': 'HYDRO_RIVER',
                    }
    # for resources timeseries that have several techs linked to it
    res_mult_params = {'Solar': ['DHN_SOLAR', 'DEC_SOLAR']}

    # Redefine the output file from the out_path given #
    out_path ='tutorial_output/'+'ESTD_' + str(nbr_td) + 'TD.dat'

    # READING OUTPUT OF STEP1 #
    td_data = generate_t_h_td(cluster_matrix.reset_index(drop=True).rename(columns={'TypicalDay': 'TD_of_days'}), nbr_td)
    # config['td_data'] = td_data

    # COMPUTING NUMBER OF DAYS REPRESENTED BY EACH TD #
    sorted_td = td_data['td_count'].copy()

    # BUILDING T_H_TD MATRICE #
    # generate T_H_TD
    t_h_td = td_data['t_h_td'].copy()
    # giving the right syntax for AMPL
    t_h_td['par_g'] = '('
    t_h_td['par_d'] = ')'
    t_h_td['comma1'] = ','
    t_h_td['comma2'] = ','
    # giving the right order to the columns
    t_h_td = t_h_td[['par_g', 'H_of_Y', 'comma1', 'H_of_D', 'comma2', 'TD_number', 'par_d']]

    # COMPUTING THE NORM OVER THE YEAR ##
    norm = time_series.sum(axis=0)
    norm.index.rename('Category', inplace=True)
    norm.name = 'Norm'

    # BUILDING TD TIMESERIES #
    # creating df with 2 columns : day of the year | hour in the day
    d_of_h = np.repeat(np.arange(1, 366, 1), 24, axis=0)  # 24 times each day of the year
    h_of_d = np.resize(np.arange(1, 25), 24 * 365)  # 365 times hours from 1 to 24
    day_and_hour = pd.DataFrame(np.vstack((d_of_h, h_of_d)).T, index=np.arange(1, 8761, 1),
                                columns=['D_of_H', 'H_of_D'])
    day_and_hour = day_and_hour.astype('int64')
    time_series = time_series.merge(day_and_hour, left_index=True, right_index=True)

    # selecting time series of TD only
    td_ts = time_series[time_series['D_of_H'].isin(sorted_td['TD_of_days'])]

    # COMPUTING THE NORM_TD OVER THE YEAR FOR CORRECTION #
    # computing the sum of ts over each TD
    agg_td_ts = td_ts.groupby('D_of_H').sum()
    agg_td_ts.reset_index(inplace=True)
    agg_td_ts.drop(columns=['D_of_H', 'H_of_D'], inplace=True)
    # multiplicating each TD by the number of day it represents
    for c in agg_td_ts.columns:
        agg_td_ts[c] = agg_td_ts[c] * sorted_td['#days']
    # sum of new ts over the whole year
    norm_td = agg_td_ts.sum()

    # BUILDING THE DF WITH THE TS OF EACH TD FOR EACH CATEGORY #
    # pivoting TD_ts to obtain a (24,Nbr_TD*Nbr_ts*N_c)
    all_td_ts = td_ts.pivot(index='H_of_D', columns='D_of_H')

    # COMPUTE peak_sh_factor #
    max_sh_td = td_ts.loc[:, 'Space Heating (%_sh)'].max()
    max_sh_all = time_series.loc[:, 'Space Heating (%_sh)'].max()
    peak_sh_factor = max_sh_all / max_sh_td

    # PRINTING #
    # printing description of file
    # header_file = (Path(__file__).parent / 'headers' / 'header_12td.txt')
    # print_header(header_file=header_file, dat_file=out_path)

    # printing sets and parameters
    with open(out_path, mode='a', newline='') as td_file:
        td_writer = csv.writer(td_file, delimiter='\t', quotechar=' ', quoting=csv.QUOTE_MINIMAL)

        # print nbr_tds param
        td_writer.writerow(['param nbr_tds := ' + str(nbr_td)])
        td_writer.writerow([';		'])
        td_writer.writerow(['		'])
        # peak_sh_factor
        td_writer.writerow(['param peak_sh_factor	:=	' + str(peak_sh_factor)])
        td_writer.writerow([';		'])
        td_writer.writerow(['		'])

        # printing T_H_TD param
        td_writer.writerow(['#SETS [Figure 3]		'])
        td_writer.writerow(['set T_H_TD := 		'])

    t_h_td.to_csv(out_path, sep='\t', header=False, index=False, mode='a', quoting=csv.QUOTE_NONE)

    # printing interlude
    with open(out_path, mode='a', newline='') as td_file:
        td_writer = csv.writer(td_file, delimiter='\t', quotechar=' ', quoting=csv.QUOTE_MINIMAL)

        td_writer.writerow([';'])
        td_writer.writerow([''])
        td_writer.writerow(['# -----------------------------'])
        td_writer.writerow(['# PARAMETERS DEPENDING ON NUMBER OF TYPICAL DAYS : '])
        td_writer.writerow(['# -----------------------------'])
        td_writer.writerow([''])

    # printing EUD timeseries param
    for k in eud_params.keys():
        ts = all_td_ts[k]
        ts.columns = np.arange(1, nbr_td + 1)
        ts = ts * norm[k] / norm_td[k]
        ts.fillna(0, inplace=True)

        ts = ampl_syntax(ts, '')
        print_df(eud_params[k], ts, out_path)
        newline(out_path)

    # printing c_p_t param #
    with open(out_path, mode='a', newline='') as td_file:
        td_writer = csv.writer(td_file, delimiter='\t', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        td_writer.writerow(['param c_p_t:='])
        # printing c_p_t part where 1 ts => 1 tech
    for k in res_params.keys():
        ts = all_td_ts[k]
        ts.columns = np.arange(1, nbr_td + 1)
        ts = ts * norm[k] / norm_td[k]
        ts.fillna(0, inplace=True)

        ts = ampl_syntax(ts, '')
        s = '["' + res_params[k] + '",*,*]:'
        ts.to_csv(out_path, sep='\t', mode='a', header=True, index=True, index_label=s, quoting=csv.QUOTE_NONE)
        newline(out_path)

    # printing c_p_t part where 1 ts => more then 1 tech
    for k in res_mult_params.keys():
        for j in res_mult_params[k]:
            ts = all_td_ts[k]
            ts.columns = np.arange(1, nbr_td + 1)
            ts = ts * norm[k] / norm_td[k]
            ts.fillna(0, inplace=True)
            ts = ampl_syntax(ts, '')
            s = '["' + j + '",*,*]:'
            ts.to_csv(out_path, sep='\t', mode='a', header=True, index=True, index_label=s, quoting=csv.QUOTE_NONE)


def generate_t_h_td(td_of_days, nbr_td):
    """Generate t_h_td and td_count dataframes and assign it to each region
    t_h_td is a pd.DataFrame containing 4 columns:
    hour of the year (H_of_Y), hour of the day (H_of_D), typical day representing this day (TD_of_days)
    and the number assigned to this typical day (TD_number)

    td_count is a pd.DataFrame containing 2 columns:
    List of typical days (TD_of_days) and number of days they represent (#days)
    """

    # Reading td_of_days
    # td_of_days = pd.read_csv(config['step1_path'] / 'td_of_days.out', names=['TD_of_days'])

    
    td_of_days['day'] = np.arange(1, 366, 1)  # putting the days of the year beside

    # COMPUTING NUMBER OF DAYS REPRESENTED BY EACH TD AND ASSIGNING A TD NUMBER TO EACH REPRESENTATIVE DAY
    td_count = td_of_days.groupby('TD_of_days').count()
    td_count = td_count.reset_index().rename(columns={'index': 'TD_of_days', 'day': '#days'})
    td_count['TD_number'] = np.arange(1,nbr_td + 1)

    # BUILDING T_H_TD MATRICE
    t_h_td = pd.DataFrame(np.repeat(td_of_days['TD_of_days'].values, 24, axis=0),
                        columns=['TD_of_days'])  # column TD_of_days is each TD repeated 24 times
    map_td = dict(zip(td_count['TD_of_days'],
                    np.arange(1, nbr_td + 1)))  # mapping dictionnary from TD_of_Days to TD number
    t_h_td['TD_number'] = t_h_td['TD_of_days'].map(map_td)
    t_h_td['H_of_D'] = np.resize(np.arange(1, 25), t_h_td.shape[0])  # 365 times hours from 1 to 24
    t_h_td['H_of_Y'] = np.arange(1, 8761)
    return {'td_of_days': td_of_days, 'td_count': td_count, 't_h_td': t_h_td}

def ampl_syntax(df, comment):
    # adds ampl syntax to df
    df2 = df.copy()
    df2.rename(columns={df2.columns[df2.shape[1] - 1]: str(df2.columns[df2.shape[1] - 1]) + ' ' + ':= ' + comment},
            inplace=True)
    return df2

def print_df(name, df, out_path):
    df.to_csv(out_path, sep='\t', mode='a', header=True, index=True, index_label=name, quoting=csv.QUOTE_NONE)

    with open(out_path, mode='a', newline='') as file:
        writer = csv.writer(file, delimiter='\t', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([';'])

def newline(out_path):
    with open(out_path, mode='a', newline='') as file:
        writer = csv.writer(file, delimiter='\t', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([''])
