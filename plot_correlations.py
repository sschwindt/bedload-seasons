"""
Plot and save dataset completeness and Spearman correlatins
"""
try:
    from bedPyLoad.categorize import *
except Exception as e:
    print('Import incomplete - errors likely:\n' + str(e))

if __name__ == '__main__':
    # create correlation plot
    plot_df_correlations(
        df_num,
        figure_base_name='figures/dataset-corr-',
        replace_col_names=FULL_LABEL_DICT,
    )
    # for Office fans: also write it to an xlsx workbook
    df_num.corr(method='spearman').to_excel('corr-spearman.xlsx')
