###snapshot-version: 0.1.4
###model-start
set PERIODS;
set SECTORS;
set END_USES_INPUT;
set END_USES_CATEGORIES;
set END_USES_TYPES_OF_CATEGORY{END_USES_CATEGORIES};
set RESOURCES;
set BIOMASS within RESOURCES;
set EXPORT within RESOURCES;
set END_USES_TYPES =  setof {i in END_USES_CATEGORIES, j in
   END_USES_TYPES_OF_CATEGORY[i]} j;
set TECHNOLOGIES_OF_END_USES_TYPE{END_USES_TYPES};
set STORAGE_TECH;
set STORAGE_ALL;
set INFRASTRUCTURE;
set INTERMIDIATE_RESOURCES within RESOURCES;
set RENEW within RESOURCES;
set BIO_PRODUCT;
set CO2_CATEGORY;
set TECHNOLOGIES_OF_CC;
set TECHNOLOGIES_OF_CCS;
set TECHNOLOGIES_OF_CCU;
set TECHNOLOGIES_OF_CCUS = TECHNOLOGIES_OF_CC union TECHNOLOGIES_OF_CCS
   union TECHNOLOGIES_OF_CCU;
set TECHNOLOGIES_OF_PRIVATEMOB_ALL_DISTANCES;
set MODELS_OF_TECHNOLOGIES_OF_PRIVATEMOB_ALL_DISTANCES{
  TECHNOLOGIES_OF_PRIVATEMOB_ALL_DISTANCES};
set LAYERS = RESOURCES diff EXPORT union END_USES_TYPES;
set TECHNOLOGIES =  setof {i in END_USES_TYPES, j in
   TECHNOLOGIES_OF_END_USES_TYPE[i]} j union STORAGE_TECH union
  INFRASTRUCTURE union TECHNOLOGIES_OF_CCUS union
  TECHNOLOGIES_OF_PRIVATEMOB_ALL_DISTANCES;
set TECHNOLOGIES_OF_END_USES_CATEGORY{i in END_USES_CATEGORIES}  within
  TECHNOLOGIES =  setof {j in  END_USES_TYPES_OF_CATEGORY[i], k in
   TECHNOLOGIES_OF_END_USES_TYPE[j]} k;
set ELECTRICITY_LAYERS within LAYERS;
set NG_LAYERS within LAYERS;
set H2_LAYERS within LAYERS;
set GRIDS_OF_LAYERS{ELECTRICITY_LAYERS union NG_LAYERS union H2_LAYERS};
set GRIDS;
set INFRASTRUCTURE_ELEC_GRID;
set INFRASTRUCTURE_GAS_GRID;
set INFRASTRUCTURE_ELEC_STORAGE;
set INFRASTRUCTURE_GAS_STORAGE;
set COGEN within TECHNOLOGIES;
set BOILERS within TECHNOLOGIES;
set BUSES within TECHNOLOGIES;
set INTERMITTENT_TECHNOLOGIES;
param end_uses_demand_year{END_USES_INPUT, SECTORS}  >= 0 default 0;
param end_uses_input{i in END_USES_INPUT}  = sum{s in SECTORS}
  end_uses_demand_year[i,s];
param i_rate > 0;
param share_mobility_public_min >= 0 <= 1;
param share_mobility_public_max >= 0 <= 1;
param share_freight_train_min >= 0 <= 1;
param share_freight_train_max >= 0 <= 1;
param share_heat_dhn_min >= 0 <= 1;
param share_heat_dhn_max >= 0 <= 1;
param t_op{PERIODS};
param total_time = sum{t in PERIODS} t_op[t];
param lighting_month{PERIODS}  >= 0 <= 1;
param heating_month{PERIODS}  >= 0 <= 1;
param layers_in_out{RESOURCES union TECHNOLOGIES diff STORAGE_TECH, LAYERS
   union CO2_CATEGORY union  {'HEAT_WASTE'}}  default 0;
param ref_size{TECHNOLOGIES}  >= 0 default 0.001;
param c_inv{TECHNOLOGIES}  >= 0 default 1e-06;
param c_maint{TECHNOLOGIES}  >= 0 default 0;
param lifetime{TECHNOLOGIES}  >= 0 default 20;
param f_max{TECHNOLOGIES}  >= 0 default 3e+05;
param f_min{TECHNOLOGIES}  >= 0 default 0;
param fmax_perc{TECHNOLOGIES}  >= 0 <= 1 default 1;
param fmin_perc{TECHNOLOGIES}  >= 0 <= 1 default 0;
param c_p_t{TECHNOLOGIES, PERIODS}  >= 0 <= 1 default 1;
param c_p{TECHNOLOGIES}  >= 0 <= 1 default 1;
param tau{i in TECHNOLOGIES}  = i_rate*(1 + i_rate)^lifetime[i]/((1 +
  i_rate)^lifetime[i] - 1);
param gwp_constr{TECHNOLOGIES}  >= 0 default 0;
param trl{TECHNOLOGIES}  >= 0 default 9;
param c_op{RESOURCES, PERIODS}  >= 0 default 1e-06;
param avail{RESOURCES}  >= 0 default 0;
param carbon_content{RESOURCES union CO2_CATEGORY}  >= 0 default 0.07;
param gwp_e{RESOURCES, PERIODS}  >= 0 default 0;
param f_grid_ext{GRIDS}  default 0;
param l_grid_ext{GRIDS}  default 0;
param n_stations{GRIDS}  default 1;
param l_grid_ref{g in GRIDS}  = l_grid_ext[g]/n_stations[g];
param k_security{GRIDS}  default 0;
param storage_eff_in{STORAGE_TECH, LAYERS}  >= 0 <= 1 default 0;
param storage_eff_out{STORAGE_TECH, LAYERS}  >= 0 <= 1 default 0;
param loss_coeff{END_USES_TYPES}  >= 0 default 0;
param peak_dhn_factor >= 0;
param co2_limit default 1e+08;
param co2_limit_max default 0;
param sng_min default 0;
param renew default 0;
param trl_min default 1;
param trl_max default 9;
param bio_ratio default 0;
var End_Uses{LAYERS, PERIODS}  >= 0;
var F_Mult{TECHNOLOGIES}  >= 0;
var F_Mult_t{RESOURCES union TECHNOLOGIES, PERIODS}  >= 0;
var C_inv{TECHNOLOGIES}  >= 0;
var C_maint{TECHNOLOGIES}  >= 0;
var C_op{RESOURCES}  >= 0;
var Storage_In{i in STORAGE_TECH, LAYERS, PERIODS}  >= 0;
var Storage_Out{i in STORAGE_TECH, LAYERS, PERIODS}  >= 0;
var Share_Mobility_Public >= share_mobility_public_min
     <= share_mobility_public_max;
var Share_Freight_Train >= share_freight_train_min
     <= share_freight_train_max;
var Share_Heat_Dhn >= share_heat_dhn_min
     <= share_heat_dhn_max;
var Y_Solar_Backup{TECHNOLOGIES}  binary;
var Losses{END_USES_TYPES, PERIODS}  >= 0;
var GWP_constr{TECHNOLOGIES}  >= 0;
var TotalGWP;
var TotalCost >= 0;
var Monthly_Prod{TECHNOLOGIES, PERIODS};
var Annual_Prod{TECHNOLOGIES diff STORAGE_TECH};
var STO{STORAGE_TECH, PERIODS};
var GWP{CO2_CATEGORY, PERIODS};
var Total_emission{PERIODS};
var STO_NG_LEVEL{PERIODS}  >= 0;
var STO_CO2_LEVEL{PERIODS}  >= 0;
var STO_H2_LEVEL{PERIODS}  >= 0;
var C_inv_grid_help{GRIDS}  >= 0;
subject to end_uses_t{l in LAYERS, t in PERIODS} : End_Uses[l,t] ==  if l
   == 'ELECTRICITY_LV' then end_uses_input[l]/total_time + end_uses_input[
  'LIGHTING']*lighting_month[t]/t_op[t] + Losses[l,t] else  if l ==
  'ELECTRICITY_MV' then end_uses_input[l]/total_time + Losses[l,t] else
   if l == 'ELECTRICITY_HV' then end_uses_input[l]/total_time + Losses[l,t]
   else  if l == 'ELECTRICITY_EHV' then end_uses_input[l]/total_time +
  Losses[l,t] else  if l == 'HEAT_LOW_T_DHN' then (end_uses_input[
  'HEAT_LOW_T_HW']/total_time + end_uses_input['HEAT_LOW_T_SH']*
  heating_month[t]/t_op[t])*Share_Heat_Dhn + Losses[l,t] else  if l ==
  'HEAT_LOW_T_DECEN' then (end_uses_input['HEAT_LOW_T_HW']/total_time +
  end_uses_input['HEAT_LOW_T_SH']*heating_month[t]/t_op[t])*(1 -
  Share_Heat_Dhn) else  if l == 'MOB_PUBLIC_LOCAL' then end_uses_input[
  'MOBILITY_PASSENGER_LOCAL']/total_time*Share_Mobility_Public else  if l
   == 'MOB_PUBLIC_LONGD' then end_uses_input['MOBILITY_PASSENGER_LONGD']/
  total_time*Share_Mobility_Public else  if l == 'MOB_PRIVATE_LOCAL' then
  end_uses_input['MOBILITY_PASSENGER_LOCAL']/total_time*(1 -
  Share_Mobility_Public) else  if l == 'MOB_PRIVATE_LONGD' then
  end_uses_input['MOBILITY_PASSENGER_LONGD']/total_time*(1 -
  Share_Mobility_Public) else  if l == 'MOB_FREIGHT_RAIL' then
  end_uses_input['MOBILITY_FREIGHT']/total_time*Share_Freight_Train else
   if l == 'MOB_FREIGHT_ROAD' then end_uses_input['MOBILITY_FREIGHT']/
  total_time*(1 - Share_Freight_Train) else  if l == 'HEAT_HIGH_T' then
  end_uses_input[l]/total_time else  if l == 'MOB_AVIATION' then
  end_uses_input['MOBILITY_AVIATION']/total_time;
subject to layer_balance{l in LAYERS union CO2_CATEGORY diff  {'H2_S',
  'NG_S', 'CO2_CS', 'HEAT_WASTE', 'ELEC_S', 'DIESEL_S', 'GASOLINE_S'},
  t in PERIODS} : 0 ==  if l == 'CO2_A' || l == 'CO2_S' then sum{i in
  RESOURCES union TECHNOLOGIES diff STORAGE_TECH} layers_in_out[i,l]*
  F_Mult_t[i,t] - GWP[l,t] else  if l == 'CO2_E' then sum{i in RESOURCES
   union TECHNOLOGIES diff STORAGE_TECH} layers_in_out[i,l]*F_Mult_t[i,t] -
  GWP[l,t] + 1/total_time*(sum{k in TECHNOLOGIES} GWP_constr[k]) else  if l
   == 'CO2_EE' then sum{i in RESOURCES} F_Mult_t[i,t]*gwp_e[i,t] - GWP[l,t]
   else  if l == 'CO2_C' then sum{i in RESOURCES union TECHNOLOGIES diff
  STORAGE_TECH} layers_in_out[i,l]*F_Mult_t[i,t] else sum{i in RESOURCES
   union TECHNOLOGIES diff STORAGE_TECH} layers_in_out[i,l]*F_Mult_t[i,t] +
  sum{j in STORAGE_TECH} (Storage_Out[j,l,t] - Storage_In[j,l,t]) -
  End_Uses[l,t];
subject to co2_caputrable{t in PERIODS} : GWP['CO2_A',t] >= 0;
subject to co2_imp{t in PERIODS} : GWP['CO2_EE',t] >= 0;
subject to f_mult_prevention{i in TECHNOLOGIES} : F_Mult[i] <= 1e+06*(sum
  {t in PERIODS} F_Mult_t[i,t]);
subject to size_limit{i in TECHNOLOGIES} : f_min[i] <= F_Mult[i] <= f_max[i];
subject to capacity_factor_t{i in TECHNOLOGIES diff  {'H2_STO', 'NG_STO',
  'CO2_STO', 'ELEC_STO', 'GASO_STO', 'DIE_STO'}, t in PERIODS} : F_Mult_t[i,t]
   <= F_Mult[i]*c_p_t[i,t];
subject to capacity_factor_Sto_ng{i in  {'NG_STO'}, t in PERIODS} :
  STO_NG_LEVEL[t] <= F_Mult[i];
subject to capacity_factor_Sto_co2{i in  {'CO2_STO'}, t in PERIODS} :
  STO_CO2_LEVEL[t] <= F_Mult[i];
subject to capacity_factor_Sto_h2{i in  {'H2_STO'}, t in PERIODS} :
  STO_H2_LEVEL[t] <= F_Mult[i];
subject to capacity_factor{i in TECHNOLOGIES} : sum{t in PERIODS} F_Mult_t[i,t
  ]*t_op[t] <= F_Mult[i]*c_p[i]*total_time;
var X_Solar_Backup_Aux{( TECHNOLOGIES_OF_END_USES_TYPE['HEAT_LOW_T_DECEN'])
   diff  {'DEC_SOLAR'}, t in PERIODS}  >= 0;
subject to op_strategy_decen_1_linear{i in ( TECHNOLOGIES_OF_END_USES_TYPE[
  'HEAT_LOW_T_DECEN']) diff  {'DEC_SOLAR'}, t in PERIODS} : F_Mult_t[i,t] +
  X_Solar_Backup_Aux[i,t] >= sum{t2 in PERIODS} F_Mult_t[i,t2]*t_op[t2]*((
  end_uses_input['HEAT_LOW_T_HW']/total_time + end_uses_input[
  'HEAT_LOW_T_SH']*heating_month[t]/t_op[t])/(end_uses_input[
  'HEAT_LOW_T_HW'] + end_uses_input['HEAT_LOW_T_SH']));
subject to op_strategy_decen_1_linear_1{i in (
   TECHNOLOGIES_OF_END_USES_TYPE['HEAT_LOW_T_DECEN']) diff  {'DEC_SOLAR'},
  t in PERIODS} : X_Solar_Backup_Aux[i,t] <= f_max['DEC_SOLAR']*
  Y_Solar_Backup[i];
subject to op_strategy_decen_1_linear_2{i in (
   TECHNOLOGIES_OF_END_USES_TYPE['HEAT_LOW_T_DECEN']) diff  {'DEC_SOLAR'},
  t in PERIODS} : X_Solar_Backup_Aux[i,t] <= F_Mult_t['DEC_SOLAR',t];
subject to op_strategy_decen_1_linear_3{i in (
   TECHNOLOGIES_OF_END_USES_TYPE['HEAT_LOW_T_DECEN']) diff  {'DEC_SOLAR'},
  t in PERIODS} : X_Solar_Backup_Aux[i,t] >= F_Mult_t['DEC_SOLAR',t] - (1 -
  Y_Solar_Backup[i])*f_max['DEC_SOLAR'];
subject to op_strategy_decen_2: sum{i in TECHNOLOGIES} Y_Solar_Backup[i]
   <= 1;
subject to resource_availability{i in RESOURCES} : sum{t in PERIODS}
  F_Mult_t[i,t]*t_op[t] <= avail[i];
subject to storage_layer_in{i in STORAGE_TECH, l in LAYERS, t in PERIODS} :
  Storage_In[i,l,t]*(ceil(storage_eff_in[i,l]) - 1) == 0;
subject to storage_layer_out{i in STORAGE_TECH, l in LAYERS, t in PERIODS} :
  Storage_Out[i,l,t]*(ceil(storage_eff_out[i,l]) - 1) == 0;
var Y_Sto_In{STORAGE_TECH, PERIODS}  binary;
var Y_Sto_Out{STORAGE_TECH, PERIODS}  binary;
subject to storage_no_transfer_1{i in STORAGE_TECH, t in PERIODS} : (sum
  {l in LAYERS: storage_eff_in[i,l] > 0} Storage_In[i,l,t]*storage_eff_in[i,l]
  )*t_op[t]/f_max[i] <= Y_Sto_In[i,t];
subject to storage_no_transfer_2{i in STORAGE_TECH, t in PERIODS} : (sum
  {l in LAYERS: storage_eff_out[i,l] > 0} Storage_Out[i,l,t]/
  storage_eff_out[i,l])*t_op[t]/f_max[i] <= Y_Sto_Out[i,t];
subject to storage_no_transfer_3{i in STORAGE_TECH, t in PERIODS} :
  Y_Sto_In[i,t] + Y_Sto_Out[i,t] <= 1;
subject to storage_level{i in STORAGE_TECH, t in PERIODS} : F_Mult_t[i,t]
   ==  if t == 1 then F_Mult_t[i,card(PERIODS)] + (sum{l in LAYERS:
  storage_eff_in[i,l] > 0} Storage_In[i,l,t]*storage_eff_in[i,l] - sum
  {l in LAYERS: storage_eff_out[i,l] > 0} Storage_Out[i,l,t]/
  storage_eff_out[i,l])*t_op[t] else F_Mult_t[i,t - 1] + (sum{l in LAYERS:
  storage_eff_in[i,l] > 0} Storage_In[i,l,t]*storage_eff_in[i,l] - sum
  {l in LAYERS: storage_eff_out[i,l] > 0} Storage_Out[i,l,t]/
  storage_eff_out[i,l])*t_op[t];
subject to network_losses{i in END_USES_TYPES, t in PERIODS} : Losses[i,t]
   == (sum{j in RESOURCES union TECHNOLOGIES diff STORAGE_TECH diff (
  INFRASTRUCTURE_ELEC_GRID union INFRASTRUCTURE_GAS_GRID): layers_in_out[j,i]
   > 0} layers_in_out[j,i]*F_Mult_t[j,t])*loss_coeff[i];
subject to f_max_perc{i in END_USES_TYPES, j in
   TECHNOLOGIES_OF_END_USES_TYPE[i]} : sum{t in PERIODS} F_Mult_t[j,t]*
  t_op[t] <= fmax_perc[j]*(sum{j2 in  TECHNOLOGIES_OF_END_USES_TYPE[i],
  t2 in PERIODS} F_Mult_t[j2,t2]*t_op[t2]);
subject to f_min_perc{i in END_USES_TYPES, j in
   TECHNOLOGIES_OF_END_USES_TYPE[i]} : sum{t in PERIODS} F_Mult_t[j,t]*
  t_op[t] >= fmin_perc[j]*(sum{j2 in  TECHNOLOGIES_OF_END_USES_TYPE[i],
  t2 in PERIODS} F_Mult_t[j2,t2]*t_op[t2]);
subject to storage_level_hydro_dams: F_Mult['HYDRO_STORAGE']*(f_max[
  'NEW_HYDRO_DAM'] - f_min['NEW_HYDRO_DAM']) <= f_min['HYDRO_STORAGE'] + (
  f_max['HYDRO_STORAGE'] - f_min['HYDRO_STORAGE'])*(F_Mult['NEW_HYDRO_DAM'] -
  f_min['NEW_HYDRO_DAM']);
subject to hydro_dams_shift{t in PERIODS} : Storage_In['HYDRO_STORAGE',
  'ELECTRICITY_HV',t] <= F_Mult_t['HYDRO_DAM',t] + F_Mult_t['NEW_HYDRO_DAM',t];
subject to extra_dhn: F_Mult['DHN'] == sum{j in (
   TECHNOLOGIES_OF_END_USES_TYPE['HEAT_LOW_T_DHN']) diff  {'DHN_RENOVATION'}}
  F_Mult[j];
var Max_Heat_Demand_DHN >= 0;
subject to max_dhn_heat_demand{t in PERIODS} : Max_Heat_Demand_DHN >=
  End_Uses['HEAT_LOW_T_DHN',t];
subject to peak_dhn: sum{j in  TECHNOLOGIES_OF_END_USES_TYPE[
  'HEAT_LOW_T_DHN']} F_Mult[j] >= peak_dhn_factor*Max_Heat_Demand_DHN;
subject to op_strategy_mob_private{i in (
   TECHNOLOGIES_OF_END_USES_CATEGORY['MOBILITY_PASSENGER_LONGD']) union (
   TECHNOLOGIES_OF_END_USES_CATEGORY['MOBILITY_PASSENGER_LOCAL']) union (
   TECHNOLOGIES_OF_END_USES_CATEGORY['MOBILITY_FREIGHT']), t in PERIODS} :
  F_Mult_t[i,t] >= sum{t2 in PERIODS} F_Mult_t[i,t2]*t_op[t2]/total_time;
subject to privatemob_use_pertech1{j in
  TECHNOLOGIES_OF_PRIVATEMOB_ALL_DISTANCES, t in PERIODS} : F_Mult_t[j,t]
   == sum{i in  MODELS_OF_TECHNOLOGIES_OF_PRIVATEMOB_ALL_DISTANCES[j]}
  F_Mult_t[i,t];
subject to grid_power1{t in PERIODS, g in GRIDS} : F_Mult[g] >= F_Mult_t[g,t];
subject to grid_power2{t in PERIODS, l in ELECTRICITY_LAYERS union
  H2_LAYERS union NG_LAYERS, g in  GRIDS_OF_LAYERS[l]} : F_Mult_t[g,t] >= sum
  {j in TECHNOLOGIES diff STORAGE_TECH: layers_in_out[j,l] > 0} F_Mult_t[j,t]*
  layers_in_out[j,l] + F_Mult_t[l,t];
subject to renw_penetratino: sum{i in RENEW, t in PERIODS} F_Mult_t[i,t]*
  t_op[t] >= renew*(sum{ii in RESOURCES diff BIO_PRODUCT, tt in PERIODS}
  F_Mult_t[ii,tt]*t_op[tt]);
subject to investment_cost_calc_1{i in TECHNOLOGIES diff
  TECHNOLOGIES_OF_CCUS diff  {'DHN_RENOVATION', 'DEC_RENOVATION'} diff
  GRIDS} : C_inv[i] == c_inv[i]*F_Mult[i];
subject to investment_cost_calc_2{i in TECHNOLOGIES_OF_CCUS} : C_inv[i] ==
  c_inv[i]*(sum{t in PERIODS} F_Mult_t[i,t]*t_op[t]);
subject to investment_cost_calc_3: C_inv['DHN_RENOVATION'] == c_inv[
  'DHN_RENOVATION']*(sum{t in PERIODS} F_Mult_t['DHN_RENOVATION',t]*t_op[t]);
subject to investment_cost_calc_4{i in GRIDS} : C_inv[i] == (F_Mult[i] -
  f_grid_ext[i])*c_inv[i]*l_grid_ext[i]*k_security[i]/n_stations[i] +
  C_inv_grid_help[i];
subject to op_strategy_renovation{t in PERIODS} : F_Mult_t['DHN_RENOVATION',t]
   >= sum{t2 in PERIODS} F_Mult_t['DHN_RENOVATION',t2]*t_op[t2]/total_time;
subject to investment_cost_calc_5: C_inv['DEC_RENOVATION'] == c_inv[
  'DEC_RENOVATION']*(sum{t in PERIODS} F_Mult_t['DEC_RENOVATION',t]*t_op[t]);
subject to op_strategy_renovation_2{t in PERIODS} : F_Mult_t[
  'DEC_RENOVATION',t] >= sum{t2 in PERIODS} F_Mult_t['DEC_RENOVATION',t2]*
  t_op[t2]/total_time;
subject to main_cost_calc{i in TECHNOLOGIES} : C_maint[i] == c_maint[i]*
  F_Mult[i];
subject to op_cost_calc{i in RESOURCES} : C_op[i] == sum{t in PERIODS}
  c_op[i,t]*F_Mult_t[i,t]*t_op[t];
subject to totalcost_cal: TotalCost == sum{i in TECHNOLOGIES union  {
  'HYDRO_STORAGE'} diff TECHNOLOGIES_OF_CCUS} (tau[i]*C_inv[i] + C_maint[i])
   + sum{k in TECHNOLOGIES_OF_CCUS} C_inv[k] + sum{j in RESOURCES} C_op[j];
subject to gwp_constr_calc{i in TECHNOLOGIES} : GWP_constr[i] ==
  gwp_constr[i]*F_Mult[i]/lifetime[i];
subject to production{i in TECHNOLOGIES diff STORAGE_TECH, t in PERIODS} :
  Monthly_Prod[i,t] == F_Mult_t[i,t]*t_op[t];
subject to production2{i in TECHNOLOGIES diff STORAGE_TECH} : Annual_Prod[i]
   == sum{t in PERIODS} Monthly_Prod[i,t];
subject to storage{i in STORAGE_TECH, t in PERIODS} : Monthly_Prod[i,t] == sum
  {l in LAYERS: storage_eff_out[i,l] > 0} (Storage_In[i,l,t]*
  storage_eff_in[i,l] - Storage_Out[i,l,t]/storage_eff_out[i,l])*t_op[t];
subject to total_emission{t in PERIODS} : Total_emission[t] == (GWP['CO2_A',t]
   + GWP['CO2_E',t] + GWP['CO2_EE',t])*t_op[t];
subject to co2_emission: sum{t in PERIODS} Total_emission[t] <= co2_limit;
subject to co2_emission2: sum{t in PERIODS} Total_emission[t] >=
  co2_limit_max;
subject to co2: TotalGWP == sum{t in PERIODS} Total_emission[t];
subject to sng_max: sum{i in TECHNOLOGIES diff STORAGE_TECH, t in PERIODS:
  layers_in_out[i,'SNG'] > 0} Monthly_Prod[i,t]*layers_in_out[i,'SNG'] >=
  sng_min;
subject to tech_intermittent_full_utilization{t in PERIODS, tech_inter in
  INTERMITTENT_TECHNOLOGIES} : F_Mult_t[tech_inter,t] == F_Mult[tech_inter]*
  c_p_t[tech_inter,t];
subject to trl_choice{i in TECHNOLOGIES: trl[i] > trl_max || trl[i] <
  trl_min} : F_Mult[i] == 0;
subject to bio_peneration: sum{t in PERIODS} (F_Mult_t['WOOD',t] +
  F_Mult_t['WET_BIOMASS',t])*t_op[t] >= bio_ratio*(avail['WOOD'] + avail[
  'WET_BIOMASS']);
subject to ng_storage{t in PERIODS: t > 1} : STO_NG_LEVEL[t] ==
  STO_NG_LEVEL[t - 1] + layers_in_out['NG_STO','NG_S']*F_Mult_t['NG_STO',t]*
  t_op[t] + layers_in_out['STO_NG','NG_S']*F_Mult_t['STO_NG',t]*t_op[t];
subject to ng_balance: STO_NG_LEVEL[1] == STO_NG_LEVEL[12] + layers_in_out[
  'NG_STO','NG_S']*F_Mult_t['NG_STO',1]*t_op[1] + layers_in_out['STO_NG',
  'NG_S']*F_Mult_t['STO_NG',1]*t_op[1];
var STO_IN{PERIODS}  binary;
var STO_OUT{PERIODS}  binary;
var HELP_STO{PERIODS}  >= 0;
var HELP_STO_OUT{PERIODS}  >= 0;
subject to bi_choice{t in PERIODS} : STO_IN[t] + STO_OUT[t] <= 1;
subject to in_chocie{t in PERIODS} : F_Mult_t['NG_STO',t] <= HELP_STO[t];
subject to aux_1{t in PERIODS} : HELP_STO[t] <= f_max['NG_STO']*STO_IN[t];
subject to aux_2{t in PERIODS} : HELP_STO[t] <= F_Mult_t['NG_STO',t];
subject to aux_3{t in PERIODS} : HELP_STO[t] >= F_Mult_t['NG_STO',t] - (1 -
  STO_IN[t])*f_max['NG_STO'];
subject to out_chocie{t in PERIODS} : F_Mult_t['STO_NG',t] <= HELP_STO_OUT[t];
subject to aux_1_out{t in PERIODS} : HELP_STO_OUT[t] <= f_max['STO_NG']*
  STO_OUT[t];
subject to aux_2_out{t in PERIODS} : HELP_STO_OUT[t] <= F_Mult_t['STO_NG',t];
subject to aux_3_out{t in PERIODS} : HELP_STO_OUT[t] >= F_Mult_t['STO_NG',t]
   - (1 - STO_OUT[t])*f_max['STO_NG'];
subject to co2_storage{t in PERIODS: t > 1} : STO_CO2_LEVEL[t] ==
  STO_CO2_LEVEL[t - 1] + layers_in_out['CO2_STO','CO2_CS']*F_Mult_t[
  'CO2_STO',t]*t_op[t] + layers_in_out['STO_CO2','CO2_CS']*F_Mult_t[
  'STO_CO2',t]*t_op[t];
subject to co2_balance: STO_CO2_LEVEL[1] == STO_CO2_LEVEL[12] +
  layers_in_out['CO2_STO','CO2_CS']*F_Mult_t['CO2_STO',1]*t_op[1] +
  layers_in_out['STO_CO2','CO2_CS']*F_Mult_t['STO_CO2',1]*t_op[1];
var STO_IN_CO2{PERIODS}  binary;
var STO_OUT_CO2{PERIODS}  binary;
var HELP_STO_CO2{PERIODS}  >= 0;
var HELP_STO_OUT_CO2{PERIODS}  >= 0;
subject to bi_choice_co2{t in PERIODS} : STO_IN_CO2[t] + STO_OUT_CO2[t] <= 1;
subject to in_chocie_co2{t in PERIODS} : F_Mult_t['CO2_STO',t] <=
  HELP_STO_CO2[t];
subject to aux_1_co2{t in PERIODS} : HELP_STO_CO2[t] <= f_max['CO2_STO']*
  STO_IN_CO2[t];
subject to aux_2_co2{t in PERIODS} : HELP_STO_CO2[t] <= F_Mult_t['CO2_STO',t];
subject to aux_3_co2{t in PERIODS} : HELP_STO_CO2[t] >= F_Mult_t['CO2_STO',t]
   - (1 - STO_IN_CO2[t])*f_max['CO2_STO'];
subject to out_chocie_co2{t in PERIODS} : F_Mult_t['STO_CO2',t] <=
  HELP_STO_OUT_CO2[t];
subject to aux_1_out_co2{t in PERIODS} : HELP_STO_OUT_CO2[t] <= f_max[
  'STO_CO2']*STO_OUT_CO2[t];
subject to aux_2_out_co2{t in PERIODS} : HELP_STO_OUT_CO2[t] <= F_Mult_t[
  'STO_CO2',t];
subject to aux_3_out_co2{t in PERIODS} : HELP_STO_OUT_CO2[t] >= F_Mult_t[
  'STO_CO2',t] - (1 - STO_OUT_CO2[t])*f_max['STO_CO2'];
subject to h2_storage{t in PERIODS: t > 1} : STO_H2_LEVEL[t] ==
  STO_H2_LEVEL[t - 1] + layers_in_out['H2_STO','H2_S']*F_Mult_t['H2_STO',t]*
  t_op[t] + layers_in_out['STO_H2','H2_S']*F_Mult_t['STO_H2',t]*t_op[t];
subject to h2_balance: STO_H2_LEVEL[1] == STO_H2_LEVEL[12] + layers_in_out[
  'H2_STO','H2_S']*F_Mult_t['H2_STO',1]*t_op[1] + layers_in_out['STO_H2',
  'H2_S']*F_Mult_t['STO_H2',1]*t_op[1];
var STO_IN_H2{PERIODS}  binary;
var STO_OUT_H2{PERIODS}  binary;
var HELP_STO_H2{PERIODS}  >= 0;
var HELP_STO_OUT_H2{PERIODS}  >= 0;
subject to bi_choice_h2{t in PERIODS} : STO_IN_H2[t] + STO_OUT_H2[t] <= 1;
subject to in_chocie_h2{t in PERIODS} : F_Mult_t['H2_STO',t] <=
  HELP_STO_H2[t];
subject to aux_1_h2{t in PERIODS} : HELP_STO_H2[t] <= f_max['H2_STO']*
  STO_IN_H2[t];
subject to aux_2_h2{t in PERIODS} : HELP_STO_H2[t] <= F_Mult_t['H2_STO',t];
subject to aux_3_h2{t in PERIODS} : HELP_STO_H2[t] >= F_Mult_t['H2_STO',t] - (
  1 - STO_IN_H2[t])*f_max['H2_STO'];
subject to out_chocie_h2{t in PERIODS} : F_Mult_t['STO_H2',t] <=
  HELP_STO_OUT_H2[t];
subject to aux_1_out_h2{t in PERIODS} : HELP_STO_OUT_H2[t] <= f_max[
  'STO_H2']*STO_OUT_H2[t];
subject to aux_2_out_h2{t in PERIODS} : HELP_STO_OUT_H2[t] <= F_Mult_t[
  'STO_H2',t];
subject to aux_3_out_h2{t in PERIODS} : HELP_STO_OUT_H2[t] >= F_Mult_t[
  'STO_H2',t] - (1 - STO_OUT_H2[t])*f_max['STO_H2'];
var STO_ELEC_LEVEL{PERIODS}  >= 0
     <= 0;
subject to capacity_factor_Sto_elec{i in  {'ELEC_STO'}, t in PERIODS} :
  STO_ELEC_LEVEL[t] <= F_Mult[i];
subject to elec_storage{t in PERIODS: t > 1} : STO_ELEC_LEVEL[t] ==
  STO_ELEC_LEVEL[t - 1] + layers_in_out['ELEC_STO','ELEC_S']*F_Mult_t[
  'ELEC_STO',t]*t_op[t] + layers_in_out['STO_ELEC','ELEC_S']*F_Mult_t[
  'STO_ELEC',t]*t_op[t];
subject to elec_balance: STO_ELEC_LEVEL[1] == STO_ELEC_LEVEL[12] +
  layers_in_out['ELEC_STO','ELEC_S']*F_Mult_t['ELEC_STO',1]*t_op[1] +
  layers_in_out['STO_ELEC','ELEC_S']*F_Mult_t['STO_ELEC',1]*t_op[1];
var STO_IN_ELEC{PERIODS}  binary;
var STO_OUT_ELEC{PERIODS}  binary;
var HELP_STO_ELEC{PERIODS}  >= 0;
var HELP_STO_OUT_ELEC{PERIODS}  >= 0;
subject to bi_choice_elec{t in PERIODS} : STO_IN_ELEC[t] + STO_OUT_ELEC[t]
   <= 1;
subject to in_chocie_elec{t in PERIODS} : F_Mult_t['ELEC_STO',t] <=
  HELP_STO_ELEC[t];
subject to aux_1_elec{t in PERIODS} : HELP_STO_ELEC[t] <= f_max['ELEC_STO']*
  STO_IN_ELEC[t];
subject to aux_2_elec{t in PERIODS} : HELP_STO_ELEC[t] <= F_Mult_t[
  'ELEC_STO',t];
subject to aux_3_elec{t in PERIODS} : HELP_STO_ELEC[t] >= F_Mult_t[
  'ELEC_STO',t] - (1 - STO_IN_ELEC[t])*f_max['ELEC_STO'];
subject to out_chocie_elec{t in PERIODS} : F_Mult_t['STO_ELEC',t] <=
  HELP_STO_OUT_ELEC[t];
subject to aux_1_out_elec{t in PERIODS} : HELP_STO_OUT_ELEC[t] <= f_max[
  'STO_ELEC']*STO_OUT_ELEC[t];
subject to aux_2_out_elec{t in PERIODS} : HELP_STO_OUT_ELEC[t] <= F_Mult_t[
  'STO_ELEC',t];
subject to aux_3_out_elec{t in PERIODS} : HELP_STO_OUT_ELEC[t] >= F_Mult_t[
  'STO_ELEC',t] - (1 - STO_OUT_ELEC[t])*f_max['STO_ELEC'];
subject to hydro_dams_shift3{t in PERIODS} : F_Mult_t['ELEC_STO',t] <=
  F_Mult_t['HYDRO_DAM',t] + F_Mult_t['NEW_HYDRO_DAM',t];
var STO_DIE_LEVEL{PERIODS}  >= 0
     <= 1e+06;
subject to capacity_factor_Sto_DIE{i in  {'DIE_STO'}, t in PERIODS} :
  STO_DIE_LEVEL[t] <= F_Mult[i];
subject to DIE_storage{t in PERIODS: t > 1} : STO_DIE_LEVEL[t] ==
  STO_DIE_LEVEL[t - 1] + layers_in_out['DIE_STO','DIESEL_S']*F_Mult_t[
  'DIE_STO',t]*t_op[t] + layers_in_out['STO_DIE','DIESEL_S']*F_Mult_t[
  'STO_DIE',t]*t_op[t];
subject to DIE_balance: STO_DIE_LEVEL[1] == STO_DIE_LEVEL[12] +
  layers_in_out['DIE_STO','DIESEL_S']*F_Mult_t['DIE_STO',1]*t_op[1] +
  layers_in_out['STO_DIE','DIESEL_S']*F_Mult_t['STO_DIE',1]*t_op[1];
var STO_IN_DIE{PERIODS}  binary;
var STO_OUT_DIE{PERIODS}  binary;
var HELP_STO_DIE{PERIODS}  >= 0;
var HELP_STO_OUT_DIE{PERIODS}  >= 0;
subject to bi_choice_DIE{t in PERIODS} : STO_IN_DIE[t] + STO_OUT_DIE[t] <= 1;
subject to in_chocie_DIE{t in PERIODS} : F_Mult_t['DIE_STO',t] <=
  HELP_STO_DIE[t];
subject to aux_1_DIE{t in PERIODS} : HELP_STO_DIE[t] <= f_max['DIE_STO']*
  STO_IN_DIE[t];
subject to aux_2_DIE{t in PERIODS} : HELP_STO_DIE[t] <= F_Mult_t['DIE_STO',t];
subject to aux_3_DIE{t in PERIODS} : HELP_STO_DIE[t] >= F_Mult_t['DIE_STO',t]
   - (1 - STO_IN_DIE[t])*f_max['DIE_STO'];
subject to out_chocie_DIE{t in PERIODS} : F_Mult_t['STO_DIE',t] <=
  HELP_STO_OUT_DIE[t];
subject to aux_1_out_DIE{t in PERIODS} : HELP_STO_OUT_DIE[t] <= f_max[
  'STO_DIE']*STO_OUT_DIE[t];
subject to aux_2_out_DIE{t in PERIODS} : HELP_STO_OUT_DIE[t] <= F_Mult_t[
  'STO_DIE',t];
subject to aux_3_out_DIE{t in PERIODS} : HELP_STO_OUT_DIE[t] >= F_Mult_t[
  'STO_DIE',t] - (1 - STO_OUT_DIE[t])*f_max['STO_DIE'];
var STO_GASO_LEVEL{PERIODS}  >= 0
     <= 1e+05;
subject to capacity_factor_Sto_GASO{i in  {'GASO_STO'}, t in PERIODS} :
  STO_GASO_LEVEL[t] <= F_Mult[i];
subject to GASO_storage{t in PERIODS: t > 1} : STO_GASO_LEVEL[t] ==
  STO_GASO_LEVEL[t - 1] + layers_in_out['GASO_STO','GASOLINE_S']*F_Mult_t[
  'GASO_STO',t]*t_op[t] + layers_in_out['STO_GASO','GASOLINE_S']*F_Mult_t[
  'STO_GASO',t]*t_op[t];
subject to GASO_balance: STO_GASO_LEVEL[1] == STO_GASO_LEVEL[12] +
  layers_in_out['GASO_STO','GASOLINE_S']*F_Mult_t['GASO_STO',1]*t_op[1] +
  layers_in_out['STO_GASO','GASOLINE_S']*F_Mult_t['STO_GASO',1]*t_op[1];
var STO_IN_GASO{PERIODS}  binary;
var STO_OUT_GASO{PERIODS}  binary;
var HELP_STO_GASO{PERIODS}  >= 0;
var HELP_STO_OUT_GASO{PERIODS}  >= 0;
subject to bi_choice_GASO{t in PERIODS} : STO_IN_GASO[t] + STO_OUT_GASO[t]
   <= 1;
subject to in_chocie_GASO{t in PERIODS} : F_Mult_t['GASO_STO',t] <=
  HELP_STO_GASO[t];
subject to aux_1_GASO{t in PERIODS} : HELP_STO_GASO[t] <= f_max['GASO_STO']*
  STO_IN_GASO[t];
subject to aux_2_GASO{t in PERIODS} : HELP_STO_GASO[t] <= F_Mult_t[
  'GASO_STO',t];
subject to aux_3_GASO{t in PERIODS} : HELP_STO_GASO[t] >= F_Mult_t[
  'GASO_STO',t] - (1 - STO_IN_GASO[t])*f_max['GASO_STO'];
subject to out_chocie_GASO{t in PERIODS} : F_Mult_t['STO_GASO',t] <=
  HELP_STO_OUT_GASO[t];
subject to aux_1_out_GASO{t in PERIODS} : HELP_STO_OUT_GASO[t] <= f_max[
  'STO_GASO']*STO_OUT_GASO[t];
subject to aux_2_out_GASO{t in PERIODS} : HELP_STO_OUT_GASO[t] <= F_Mult_t[
  'STO_GASO',t];
subject to aux_3_out_GASO{t in PERIODS} : HELP_STO_OUT_GASO[t] >= F_Mult_t[
  'STO_GASO',t] - (1 - STO_OUT_GASO[t])*f_max['STO_GASO'];
param out_max{TECHNOLOGIES}  >= 0 default 1e+10;
param out_min{TECHNOLOGIES}  >= 0 default 0;
subject to prod_max{i in TECHNOLOGIES diff STORAGE_TECH} : Annual_Prod[i]
   <= out_max[i];
subject to prod_min{i in TECHNOLOGIES diff STORAGE_TECH} : Annual_Prod[i]
   >= out_min[i];
subject to ccu{t in PERIODS} : sum{i in TECHNOLOGIES diff STORAGE_TECH
   diff TECHNOLOGIES_OF_CCS diff  {'CO2_STO'}: layers_in_out[i,'CO2_C'] < 0}
  -(Annual_Prod[i]*layers_in_out[i,'CO2_C']) >= STO_CO2_LEVEL[t];
param reno_share_max >= 0 <= 1 default 0.5;
param reno_share_min >= 0 <= 1 default 0;
param reno_max >= 0 default 30000;
param reno_min >= 0 default 10000;
subject to renovation_max: Annual_Prod['DHN_RENOVATION'] + Annual_Prod[
  'DEC_RENOVATION'] <= reno_max;
subject to renovation_min: Annual_Prod['DHN_RENOVATION'] + Annual_Prod[
  'DEC_RENOVATION'] >= reno_min;
param fossil_vec_share_min default 0;
param fossil_vec_share_max default 1;
subject to fuel_vehicle_min: sum{i in  {'CAR_GASOLINE', 'CAR_DIESEL'}}
  Annual_Prod[i] >= fossil_vec_share_min*(sum{ii in (
   TECHNOLOGIES_OF_END_USES_TYPE['MOB_PRIVATE_LOCAL']) union (
   TECHNOLOGIES_OF_END_USES_TYPE['MOB_PRIVATE_LONGD'])} Annual_Prod[ii]);
subject to fuel_vehicle_max: sum{i in  {'CAR_GASOLINE', 'CAR_DIESEL'}}
  Annual_Prod[i] <= fossil_vec_share_max*(sum{ii in (
   TECHNOLOGIES_OF_END_USES_TYPE['MOB_PRIVATE_LOCAL']) union (
   TECHNOLOGIES_OF_END_USES_TYPE['MOB_PRIVATE_LONGD'])} Annual_Prod[ii]);
param bus_share_min default 0;
param bus_share_max default 1;
subject to bus1: sum{i in BUSES} Annual_Prod[i] >= bus_share_min*
  end_uses_demand_year['MOBILITY_PASSENGER_LOCAL','TRANSPORTATION'];
subject to bus2: sum{i in BUSES} Annual_Prod[i] <= bus_share_max*
  end_uses_demand_year['MOBILITY_PASSENGER_LOCAL','TRANSPORTATION'];
minimize obj: TotalCost;
###model-end

###current-problem/environment-start
problem Initial;
environ Initial;
###current-problem/environment-end

###objectives-start
objective obj;
###objectives-end

###fixes-start
###fixes-end

###drop-restore-start
###drop-restore-end

