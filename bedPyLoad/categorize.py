try:
    from .get_data import *
except Exception as e:
    print('Import incomplete - errors likely:\n' + str(e))


# constants
number_of_cats = 5

df['slope_cat'] = pd.cut(df['slope'],
                         bins=[0, 0.005, 0.01, 0.02, 0.05, 0.1],
                         labels=SUB_CATEGORY_ORDER['slope_cat'])
df['altitude_cat'] = pd.cut(df['altitude'], 
                            bins=[0, 50, 200, 800, 1800, 10000], 
                            labels=SUB_CATEGORY_ORDER['altitude_cat'])
df['sinuosity_cat'] = pd.cut(df['sinuosity'], 
                             bins=[0, 1.2, 1.4, 1.5, 2.5, 100], 
                             labels=SUB_CATEGORY_ORDER['sinuosity_cat'])
df['entrench_cat'] = pd.cut(df['entrench_ratio'], 
                            bins=[0, 1.4, 2.2, 4.0, 100], 
                            labels=SUB_CATEGORY_ORDER['entrench_cat'])
df['d50_cat'] = pd.cut(df['d_50'], 
                       bins=[0.000063, 0.001, 0.002, 0.004, 0.064, 0.256],
                       labels=SUB_CATEGORY_ORDER['d50_cat'])
df['fr_cat'] = pd.cut(df['fr'], 
                      bins=[0, 0.5, 0.9, 1.1, 100], 
                      labels=SUB_CATEGORY_ORDER['fr_cat'])
df['log_omega_x_cat'] = pd.cut(df['log_omega_x'], 
                               bins=[-4.124, 1.214, 2.188, 2.94, 3.608, 6.88], 
                               labels=SUB_CATEGORY_ORDER['log_omega_x_cat'])
df['omega_x_cat'] = pd.cut(df['omega_x'],
                           bins=[0.0152, 3.054, 7.997, 17.149, 35.53, 970.081],
                           labels=SUB_CATEGORY_ORDER['log_omega_x_cat'])
df['log_Phi_cat'] = pd.cut(df['log_Phi'],
                           bins=[-14.258, -7.455, -5.908, -4.606, -2.8, 1.908], 
                           labels=SUB_CATEGORY_ORDER['log_Phi_cat'])
df['Phi_cat'] = pd.cut(df['Phi'],
                       bins=[-0.000999071, 0.000592, 0.0027, 0.0117, 0.0729, 5.432],
                       labels=SUB_CATEGORY_ORDER['log_Phi_cat'])

# extract data frame of categories only
df_cat = df[[
    # transformed numerical vars
    'slope_cat', 'altitude_cat', 'sinuosity_cat', 'entrench_cat', 'd50_cat', 'fr_cat', 'omega_x_cat', 'Phi_cat',
    # inherent categorical variables
    'seasonality', 'confinement', 'flow_regime', 'snowmelt_during_meas',
    'dam', 'glaciation_current', 'sampler type', 'river_source',
]]

# extract data frame of numerical variables only
df_num = df[['Phi', 'omega_x', 'fr', 'water_depth', 'top_width', 'd_50', 'slope',
             'sinuosity', 'entrench_ratio', 'confinement_ranked', 'altitude',  # 'lat', 'lon',
             'dam_ranked', 'glaciation_current', 'season_ranked', 'snow_ranked', 'glacier_ranked',
             'src_ranked', 'permanence_ranked']]
