"""
Script should run standalone to avoid OS-foced shutdown of the code because of memory usage
"""

from bedPyLoad.categorize import *


@log_actions
def calcNdraw_stats_glob(
        dataframe: pandas.DataFrame,
        base_directory: str,
):
    """
    Calls mor_fun.stats_test to calculate and plot p-values and dependencies between subcategories of
    a pandas.DataFrame

    :param dataframe: Contains all columns with numerical and or
    :param base_directory: where the results (xlsx and png plots) should be stored - should end on '/'
    :return int: 0 in the case of successful execution
    """
    if not os.path.isdir(base_directory):
        os.makedirs(base_directory)
    for t, t_pars in TEST_PARAMETERS.items():
        print('--- STATS FOR %s ---' + str(t).upper())
        # delete if xlsx target already exists (required for soft manipulation with append_df_to_excel funtion)
        if os.path.isfile(base_directory+t_pars['stats xlsx target']):
            os.remove(base_directory+t_pars['stats xlsx target'])
        stats_test(
            dataframe=dataframe,
            numeric_var_name=t_pars['numeric column'],
            target_columns=list(df_cat.columns),
            numeric_var_as_categories_name=t_pars['category column'],
            stats_results_xlsx=base_directory+t_pars['stats xlsx target'],
            figure_path=base_directory + '%s/' % str(t)
        )
    return 0


if __name__ == '__main__':

    calcNdraw_stats_glob(
        dataframe=df,
        base_directory='figures/'
    )
