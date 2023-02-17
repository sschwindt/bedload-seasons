# import all required packages and load basic data frames
try:
    import os, sys
    import logging
    from itertools import combinations
    import pandas as pd
    from scipy import stats
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import numpy as np
    # for distribution checking
    import statsmodels.api as sm  # qq plot
    import pylab  # qq plot
    import seaborn as sns
    from statannotations.Annotator import Annotator
    from fitter import Fitter, get_common_distributions, get_distributions
    import scikit_posthocs as sp
    # for model development
    from sklearn.feature_selection import f_regression
    from sklearn.preprocessing import LabelEncoder
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.neural_network import MLPRegressor
    from sklearn.model_selection import train_test_split, cross_val_score, KFold
    from sklearn.metrics import r2_score
    from sklearn.metrics import mean_squared_error
    pd.options.mode.chained_assignment = None  # default='warn'
    # for workbook manipulation
    from .workbook_fun import write_xlsx, append_df_to_excel
    # load modified msno (not the pip-installed one)
    sys.path.insert(0, os.path.dirname(__file__))
    import missingno as msno
except Exception as e:
    print('Import incomplete - errors likely:\n' + str(e))

# set constants
g = 9.81
rho_s = 2680
rho_f = 1000
s = rho_s/rho_f
nan_value = np.nan

# switch between full dataset and valid samplers only
# pay attention to also adapt line 115-118
BEDLOAD_XLSX = 'bedload-data-valid-samplers.xlsx'

# set script working direciton (do not touch)
SCRIPT_DIR = r'' + os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/'

# other globals
FULL_LABEL_DICT = {
    'month': 'Date',
    'discharge': 'Discharge (m3/s)',
    'unit_discharge': 'Unit discharge (m3/s/m)',
    'bedload': 'Bedload (kg/s)',
    'unit_bedload': 'Unit bedload (kg/s/m)',
    'water_depth': 'Water depth (m)',
    'top_width': 'Top width (m)',
    'lat': 'Latitude (deg)',
    'lon': 'Longitude (deg)',
    'log_Phi_norm_positive': 'Log dimensionless bedload',
    'log_Phi_cat': 'Log dimensionless bedload',
    'Phi_cat': 'Dimensionless bedload',
    'Phi': 'Dimensionless bedload',
    'altitude_cat': 'Elevation category',
    'altitude': 'Elevation (m a.s.l.)',
    'seasonality': 'Season',
    'season_ranked': 'Season',
    'river_source': 'Dominant water source',
    'src_ranked': 'Dominant water source',
    'slope_cat': 'Slope category',
    'slope': 'Slope (-)',
    'snowmelt_during_meas': 'Snowmelt during measurement',
    'snow_ranked': 'Snowmelt (active)',
    'snowmelt_prone': 'Snowmelt prone site',
    'fr_cat': 'Froude category',
    'fr': 'Froude number (-)',
    'd50_cat': 'Grain size category',
    'd_50': 'Grain size (m)',
    'flow_regime': 'Flow permanence',
    'permanence_ranked': 'Flow permanence',
    'sinuosity_cat': 'Sinuosity category',
    'sinuosity': 'Sinuosity (-)',
    'sampler type': 'Sampler type',
    'glaciation_current': 'Currently glaciated',
    'glacier_ranked': 'Currently glaciated',
    'entrench_cat': 'Entrenchment category',
    'entrench_ratio': 'Entrenchment ratio',
    'log_omega_x_cat': 'Log dimensionless streampower',
    'log_omega_x': 'Log dimensionless streampower',
    'omega_x_cat': 'Dimensionless streampower',
    'omega_x': 'Dimensionless streampower',
    'confinement': 'Confined site',
    'confinement_ranked': 'Confined site',
    'dam': 'Dam upstream of the site',
    'dam_ranked': 'Dam upstream of the site',
}

SUB_CATEGORY_ORDER = {
    'log_Phi_norm_positive': False,
    'Phi': False,
    'log_Phi': False,
    'log_Phi_cat': ['very little bedload', 'little bedload', 'moderate bedload', 'high bedload', 'very high bedload'],
    'Phi_cat': ['very little bedload', 'little bedload', 'moderate bedload', 'high bedload', 'very high bedload'],
    'altitude_cat': ['coastal altitude', 'low altitude', 'mid altitude', 'high altitude', 'alpine altitude'],
    'altitude': ['coastal altitude', 'low altitude', 'mid altitude', 'high altitude', 'alpine altitude'],
    'seasonality': ['W1', 'W2', 'SP1', 'SP2', 'SU1', 'SU2', 'F1', 'F2'],
    'season_ranked': [*range(1, 9)],
    'river_source': False,
    'slope_cat': ['very low', 'low', 'moderate', 'steep', 'very steep'],
    'slope': ['very low', 'low', 'moderate', 'steep', 'very steep'],
    'snowmelt_during_meas': False,
    'fr_cat': ['calm', 'fluvial', 'near-critical', 'torrential'],
    'fr': ['calm', 'fluvial', 'near-critical', 'torrential'],
    'd50_cat': ['sand', 'coarse sand', 'gravel', 'pebble', 'cobble'],
    'd_50': ['sand', 'coarse sand', 'gravel', 'pebble', 'cobble'],
    'flow_regime': ['perennial', 'intermittent', 'ephemeral'],
    'sinuosity_cat': ['straight', 'low sinuosity', 'meandering', 'tortuously meandering', 'braided'],
    # use the following line with bedload-data-valid-samplers.xlsx
    'sampler type': ['Helley-Smith (single device)', 'Helley-Smith (multiple)', 'others'],
    # uncomment the following line and comment the previous line when using bedload-data.xlsx
    # 'sampler type': ['Helley-Smith (single device)', 'Helley-Smith (multiple)', 'Hydrophones', 'Cross-sectional traps', 'others'],
    'glaciation_current': False,
    'entrench_cat': ['entrenched', 'moderately entrenched', 'slightly entrenched', 'wide'],
    'log_omega_x_cat': ['very little stream power', 'little stream power', 'moderate stream power', 'high stream power', 'very high stream power'],
    'omega_x_cat': ['very little stream power', 'little stream power', 'moderate stream power', 'high stream power', 'very high stream power'],
    'log_omega_x': ['very little stream power', 'little stream power', 'moderate stream power', 'high stream power', 'very high stream power'],
    'omega_x': ['very little stream power', 'little stream power', 'moderate stream power', 'high stream power', 'very high stream power'],
    'confinement': ['Unconfined', 'Confined (unknown)', 'Confined (engineered)', 'Confined (naturally)'],
    'dam': False,
}

# define test parameters
TEST_PARAMETERS = {
    'bedload': {
        'numeric column': 'log_Phi_norm_positive',
        'category column': 'log_Phi_cat',
        'stats xlsx target': 'fitting-results/posthoc-dunn-Phi.xlsx',
        'figure name label': 'Phi'
    },
}

# setup logging
info_formatter = logging.Formatter("%(asctime)s - %(message)s")
warn_formatter = logging.Formatter("WARNING [%(asctime)s]: %(message)s")
error_formatter = logging.Formatter("ERROR [%(asctime)s]: %(message)s")
logger = logging.getLogger("logfile")
logger.setLevel(logging.DEBUG)
logger_warn = logging.getLogger("warnings")
logger_warn.setLevel(logging.WARNING)
logger_error = logging.getLogger("errors")
logger_error.setLevel(logging.ERROR)
# create console handler and set level to info
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(info_formatter)
logger.addHandler(console_handler)
console_whandler = logging.StreamHandler()
console_whandler.setLevel(logging.WARNING)
console_whandler.setFormatter(warn_formatter)
logger_warn.addHandler(console_whandler)
console_ehandler = logging.StreamHandler()
console_ehandler.setLevel(logging.ERROR)
console_ehandler.setFormatter(error_formatter)
logger_error.addHandler(console_ehandler)
# create info file handler and set level to debug
info_handler = logging.FileHandler(SCRIPT_DIR + "logfile.log", "w")
info_handler.setLevel(logging.DEBUG)
info_handler.setFormatter(info_formatter)
logger.addHandler(info_handler)
# create warning file handler and set level to error
warn_handler = logging.FileHandler(SCRIPT_DIR + "warnings.log", "w")
warn_handler.setLevel(logging.WARNING)
warn_handler.setFormatter(warn_formatter)
logger_warn.addHandler(warn_handler)
# create error file handler and set level to error
err_handler = logging.FileHandler(SCRIPT_DIR + "errors.log", "w")
err_handler.setLevel(logging.ERROR)
err_handler.setFormatter(error_formatter)
logger_error.addHandler(err_handler)
