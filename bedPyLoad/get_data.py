try:
    from .mor_fun import *
except Exception as e:
    print('Import incomplete - errors likely:\n' + str(e))

# load and clean bedload data
df = pd.read_excel(
    io='./data/' + BEDLOAD_XLSX,
    header=0,
    skiprows=lambda x: x in [1],   # skip second row containing units
)

# substitute '-' entries with nan
df = df.mask(df == '-')
# mask elements where water depth was zero but bedload was given
df['water_depth'] = df['water_depth'].mask(df['water_depth'] == 0)
# replace F and T letters with pseudo-booleans (real booleans crashes histograms)
df['dam'] = df['dam'].replace({'F': False, 'T': True})
df['glaciation_current'] = df['glaciation_current'].replace({'F': False, 'T': True})
df['snowmelt_during_meas'] = df['snowmelt_during_meas'].replace({'F': False, 'T': True})
df['confinement'] = df['confinement'].replace({'F': 'Unconfined', 'T': 'Confined (unknown)', 'EC': 'Confined (engineered)', 'SC': 'Confined (naturally)'})

# ranked categories according to 50 percent median height regarding bedload of corresponding categories
df['season_ranked'] = df['seasonality'].replace({'W1': 6, 'W2': 8, 'SP1': 4, 'SP2': 2, 'SU1': 1, 'SU2': 5, 'F1': 3, 'F2': 7})
df['src_ranked'] = df['river_source'].replace({'snowmelt': 1, 'ultra-snowmelt': 2, 'rainfall': 3, 'groundwater': 4})
df['permanence_ranked'] = df['flow_regime'].replace({'perennial': 1, 'intermittent': 2, 'ephemeral': 3})
df['dam_ranked'] = df['dam'].replace({False: 2, True: 1})
df['snow_ranked'] = df['snowmelt_during_meas'].replace({False: 2, True: 1})
df['glacier_ranked'] = df['glaciation_current'].replace({False: 1, True: 2})
df['confinement_ranked'] = df['confinement'].replace({'Unconfined': 2, 'Confined (unknown)': 1, 'Confined (engineered)': 4, 'Confined (naturally)': 3})

# interpolate hydraulics
df['u_intp'] = (df['unit_discharge'] / df['water_depth']).to_numpy().astype(float)
df['fr'] = (df['u_intp'] / (g * df['water_depth']) ** 0.5).to_numpy().astype(float)
df['omega_x'] = df['unit_discharge'] * df['slope'] / ((s - 1) * np.sqrt(g) * df['d_50'] ** 1.5)
log_omega_x = np.log(df['omega_x'].to_numpy(copy=True))
log_omega_max = np.nanmax(log_omega_x)
log_omega_min = np.nanmin(log_omega_x)
df['log_omega_x_norm'] = abs(log_omega_x - abs(log_omega_min)) / abs(log_omega_max - log_omega_min)
df['log_omega_x'] = log_omega_x
df['ratio_dis_bl'] = df['bedload'] / rho_s / df['discharge']
df = df[df['ratio_dis_bl'] < 0.1]
# treat bedload measurements and grain characteristics
df['Phi'] = (df['unit_bedload'] / (rho_s * np.sqrt((s - 1) * g) * df['d_50'] ** 1.5)).to_numpy().astype(float)
df['log_Phi'] = np.log(df['Phi'].to_numpy(copy=True))
df['D_x'] = (df['d_max'] - df['d_50']) / df['d_50']
df['D_x'] = df['D_x'].mask(df['D_x'] <= 0.0)  # remove entries where a d_max dummy makes that d_max > d_50
df['Phi_Dx'] = (df['D_x'] * df['Phi']).to_numpy(copy=True).astype(float)
df['log_Phi_Dx'] = np.log(df['Phi_Dx'].to_numpy())
# normalize Phi
log_Phi_num = df['log_Phi'].dropna().to_numpy(copy=True).astype(float)
log_Phi_max = np.nanmax(log_Phi_num)
log_Phi_min = np.nanmin(log_Phi_num)
log_Phi_num = (log_Phi_num + abs(log_Phi_min)) / abs(log_Phi_max - log_Phi_min)
df['log_Phi_norm_positive'] = np.nan_to_num((df['log_Phi'].to_numpy(na_value=np.nan).astype(float) + abs(log_Phi_min)) / abs(log_Phi_max - log_Phi_min), nan=np.nan).tolist()
