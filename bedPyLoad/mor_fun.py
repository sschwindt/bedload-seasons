"""
Script provides functions for application at all levels, for instance, to plot data.
more_fun is an acronym for 'morpho-analyst functions' or 'more fun', depending on your preference
"""
import os.path
import pandas
from .config import *


def annotated_plot(
        df,
        target_var,
        num_var,
        x_label=None,
        y_label=None,
        plot_type='boxplot',
        fig_format='png',
        fig_path=None,
        color_palette=None,
        dpi=300,
        bbox='tight',
        test='Kruskal',
        text_format='simple',
        text_offset=7,
        y_scale=None
):
    """
    Make an annotated plot with statannotations.stats. Read more about statannoation usage at
    https://github.com/trevismd/statannotations/tree/master/usage

    :param pd.DataFrame df: DataFrame containing categorical and numerical data to be boxplotted.
                            Categories will occur on the x-axis according to target_var.
                            Numerical data according tu num_var
    :param str target_var: name of a target variable that must be contained in the column names of df
    :param str num_var: name of a numerical variable on the Y-axis that must be contained in the column names of df
    :param str x_label: if provided, this string replaces the column name of target_var (categorical)
    :param str y_label: if provided, this string replaces the column name of the numeric y variable
    :param str plot_type: default is 'boxplot', options are 'violinplot', 'swarmplot'
    :param str fig_format: file ending of image file; default is 'png'
    :param str fig_path: name and directory of image (figure) to save WITHOUT FILE FORMAT ending, MUST end on '/'
    :param str,list,dict color_palette: colors to be used with the `hue` variable
    :param int dpi: dots per inch for figure (default is 300)
    :param str bbox: default 'tight' applies narrow figure margins
    :param str test: type of statistical test for calculating p-values. Default is 'Kruskal'. Options are defined in
                        statannotations.stats.StatTest.STATTEST_LIBRARY (line 88ff)
    :param str text_format: formatting of p-value annotations. Default is 'simple'. Options are 'star' and 'full'
    :param int text_offset: number of pixels for offset of p-value annotations. Default is 5.
    :param str y_scale: default is None but can be set to 'log' for logarithmic y axis.
    :return int: 0 = success, -1 = error occurred
    """

    configuration = {
        'test': test,
        'text_format': text_format,
        'text_offset': text_offset,
    }

    # treat original dataframe (remove nan and potentially replace labels
    df = df[[target_var, num_var]].copy()
    df = df.dropna().reset_index(drop=True)
    logging.info('* created the following dataframe for test: ' + str(test))
    logging.info(df.head(3))
    cat_key = target_var
    if x_label:
        df = df.rename(columns={target_var: x_label})  # must not use inplace=True
        target_var = x_label
    if y_label:
        df = df.rename(columns={num_var: y_label})
        num_var = y_label

    # setup figure
    col_categories = np.unique(df[target_var]).tolist()  # must be a list
    if SUB_CATEGORY_ORDER[cat_key]:
        categories = SUB_CATEGORY_ORDER[cat_key]
        for cat in categories:
            if not(cat in col_categories):
                categories.remove(cat)
    else:
        categories = col_categories
    fig_args = {
        'x': target_var,
        'y': num_var,
        # 'hue': target_var,
        'data': df,
        'order': categories,
        'palette': color_palette,
        'boxprops': {'facecolor': (.3, .3, .3, .07)},
        'flierprops': {'marker': 'o', 'markerfacecolor': 'gray', 'markersize': 5,
                       'markeredgecolor': 'black', 'alpha': .35},
        'medianprops': {'color': 'gray'},
        # 'hue_order': categories,
        'dodge': True,
    }

    # prepare plot
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    # setup fonts
    sns.set_context("paper", font_scale=1.5)
    # apply scaling if defined
    if y_scale:
        logging.info('* using logarithmic y-axis')
        ax.set_yscale('log')
    # make plot
    logging.info('* making base plot...')
    plot_type_dict = {
        'boxplot': sns.boxplot,
        'violinplot': sns.violinplot,
        'swarmplot': sns.swarmplot,
    }
    plot_type_dict[plot_type](ax=ax, **fig_args)

    # define pairs for calculating p-values
    if not SUB_CATEGORY_ORDER[cat_key]:
        # if categories are not defined neighbors as per config.py (i.e. False)
        logging.info('* pairing all categories...')
        pairs = [comb for comb in combinations(categories, 2)]  # last 2 sets pair-wise (not 3-3 cats or similar)
    else:
        # this applies only pairing neighboring categories (e.g. good for seasons such as winter and spring)
        logging.info('* pairing neighboring categories only...')
        rotated_cats = categories[1:] + categories[:1]
        pairs = [(cat, rotated_cats[idx - 1]) for idx, cat in enumerate(rotated_cats)]
    logging.info('* using the following pairs: ' + str(pairs))

    # instantiate Annotator
    logging.info('* annotating figure...')
    try:
        annotator = Annotator(
            ax=ax, pairs=pairs, **fig_args
        )
    except Exception as e:
        logging.error('ERROR: could not plot {0}:\n {1}'.format(str(target_var), str(e)))
        return -1
    annotator.new_plot(ax, plot=plot_type, **fig_args)
    logging.info('* applying {0} test to calculate p-values...'.format(str(test)))
    try:
        if len(pairs) < 13:
            annotator.configure(**configuration).apply_test().annotate()
        else:
            logging.warning('* SKIPPING ANNOTATION (%s are too many pairs for visualization)' % str(len(pairs)))
    except Exception as e:
        logging.error(e)
        logging.error('*** looks like there are NoneTypes in the data set...')
        return -1
    plt.xticks(rotation=45)
    ax.set(xlabel=None)  # remove redundant x-label information
    # write figure to disk
    try:
        fig_name = str(fig_path) + str(cat_key) + '.' + str(fig_format)
        logging.info('  -- trying to save ' + fig_name)
        fig.savefig(
            fig_name,
            format=fig_format,
            dpi=dpi,
            bbox_inches=bbox
        )
        plt.close()
        logging.info('* saved ' + fig_name)
    except Exception as e:
        logging.error('ERROR WHILE SAVING FIGURE:')
        logging.error(e)
        return -1
    return 0


def stats_test(
        dataframe: pandas.DataFrame,
        numeric_var_name: str,
        target_columns: list,
        numeric_var_as_categories_name: str = None,
        stats_results_xlsx: str = 'stats-results.xlsx',
        figure_path: str = 'fitting-results/figures/'
):
    """
    Runs Dunn posthoc test on categories with reference to a non-normally distributed variable defined as
    `numeric_var_name`. This function is tweaked for this package and requires the global variables defined in config.py.


    :param dataframe: A pandas dataframe containing all numeric and categorical data
    :param numeric_var_name: Name of a numerical variable (typical response variable) to be tested. MUST be a column
                             name of `dataframe`
    :param target_columns: List of column names to be tested for differences with the numeric variable
    :param numeric_var_as_categories_name: For the Dunn test, the numerical variable should also be categorized
                                           (e.g. in categories 'low', 'average', 'high'). This argument is the name of a
                                           column in `dataframe` that contains the numerical variable as categories.
    :param stats_results_xlsx: Name of an xlsx file to store Dunn test results (default name applies if not provided)
    :param figure_path: directory or subdirectory where figures will be stored; MUST end on '/'
    :return int success: successful execution when 0, otherwise -1
    """

    for target_var in target_columns:
        if numeric_var_as_categories_name == target_var:
            # do not correlate the numeric version of a variable with its categorization
            continue
        logging.info('> Pre-processing for Dunn tests...' + target_var)
        # run Dunn tests and write results to XLSX files
        df_cat4sub = pd.concat(
            [dataframe[numeric_var_as_categories_name], dataframe[target_var]],
            axis=1
        ).reset_index().dropna(axis=0)

        logging.info('  ...with %s samples.' % str(df_cat4sub.size))
        if numeric_var_as_categories_name:
            logging.info('> Dunn test with categorical data driving categorized numerical variable...')
            try:
                num_as_cat_df = sp.posthoc_dunn(df_cat4sub, val_col=target_var, group_col=numeric_var_as_categories_name, p_adjust='holm')
                append_df_to_excel(stats_results_xlsx, sheet_name=target_var, df=num_as_cat_df, startrow=0)
            except Exception as e:
                logging.warning('WARNING: NOT ENOUGH SAMPLES - SKIPPING DUNN TEST DIRECTION\n' + str(e))
            logging.info('> Dunn test for categorical data as a function of categorized numerical variable...')
            try:
                cat_from_num_df = sp.posthoc_dunn(df_cat4sub, val_col=numeric_var_as_categories_name, group_col=target_var, p_adjust='holm')
                append_df_to_excel(stats_results_xlsx, sheet_name=target_var, df=cat_from_num_df, startrow=9)
            except Exception as e:
                logging.warning('WARNING: NOT ENOUGH SAMPLES - SKIPPING DUNN TEST DIRECTION\n' + str(e))
        else:
            logging.warning('> Skipping Dunn test because I do not have information on categorization of the numerical parameter')

        logging.info('> Jumping into annotated plotting...')
        if not os.path.isdir(figure_path):
            os.makedirs(figure_path)
        try:
            annotated_plot(
                dataframe,
                target_var,
                num_var=numeric_var_name,
                x_label=FULL_LABEL_DICT[target_var],
                y_label=FULL_LABEL_DICT[numeric_var_name],
                fig_path=figure_path,
                dpi=500,
            )
        except Exception as e:
            logging.warning('WARNING: NOT ENOUGH SAMPLES - SKIPPING ANNOTATED PLOT\n' + str(e))
        logging.info('> STATS TEST FINISHED FOR ' + numeric_var_name.upper())
    return 0


def log_actions(func):
    logging.basicConfig(
        filename='logfile.log',
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s]:%(message)s'
    )

    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        for handler in logging.getLogger('logfile').handlers:
            handler.close()
            logging.getLogger('logfile').removeHandler(handler)
        for handler in logging.getLogger('warnings').handlers:
            handler.close()
            logging.getLogger('warnings').removeHandler(handler)
        for handler in logging.getLogger('errors').handlers:
            handler.close()
            logging.getLogger('errors').removeHandler(handler)
        print('Check the logfiles: logfile.log, warnings.log, and errors.log.')
    return wrapper


def plot_df_completeness(
        df,
        figure_base_name='base',
        replace_col_names=None
):
    """ Uses missingno package to create a plot of dataframe completeness

    :param pandas.DataFrame df: Dataframe to be plotted
    :param str figure_base_name: syllable to be used with figure names
    :param dict replace_col_names: optional argument to overwrite column names
    :return: write plot
    """

    if replace_col_names:
        try:
            df = df.rename(columns=replace_col_names)
        except Exception as e:
            logging.error("ERROR: The provided argument replace_col_names does not fit the dataframe:\n" + str(e))
            return -1

    fig = msno.matrix(df, labels=True)
    fig_copy = fig.get_figure()
    fig_copy.savefig(figure_base_name+'-completeness.png', bbox_inches='tight', dpi=300)

    plt.close()
    logging.info("successfully saved dataframe completeness plot as " + figure_base_name)


def get_color_list(n, name='hsv'):
    """ Returns a list of n RGB colors

    :param n: size of colormap list
    :param str name: type of color map - must be a standard matplotlib colormap name
    :return list: colormap of size n
    """
    cmap = plt.cm.get_cmap(name, n)
    return [cmap(c) for c in range(n)]


def plot_df_correlations(
        df,
        figure_base_name='base',
        fontsize=16,
        replace_col_names=None
):
    """ Creates a heatmap plot of correlations

    :param pandas.DataFrame df: Dataframe to be plotted
    :param str figure_base_name: syllable to be used with figure names
    :param int fontsize: font size
    :param dict replace_col_names: optional argument to overwrite column names
    :return: write plot
    """

    if replace_col_names:
        try:
            df = df.rename(columns=replace_col_names)
        except Exception as e:
            logging.error("ERROR: The provided argument replace_col_names does not fit the dataframe:\n" + str(e))
            return -1

    plt.figure(figsize=(20, 12))
    ax0 = plt.gca()

    corr_mat = df.corr(method='spearman')
    mask = np.zeros_like(corr_mat)
    mask[np.triu_indices_from(mask)] = True

    sns.heatmap(corr_mat, mask=mask, cmap='RdBu', ax=ax0, cbar=False,
                annot=True, annot_kws={'size': fontsize},
                vmin=-1, vmax=1)

    # visual corrections and modifications
    ax0.xaxis.tick_bottom()
    ax0.set_xticklabels(
        ax0.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=fontsize
    )
    ax0.set_yticklabels(ax0.yaxis.get_majorticklabels(), rotation=0, fontsize=fontsize)
    ax0.xaxis.set_ticks_position('none')
    ax0.yaxis.set_ticks_position('none')
    ax0.patch.set_visible(False)

    for text in ax0.texts:
        t = float(text.get_text())
        if 0.95 <= t < 1:
            text.set_text('<1')
        elif -1 < t <= -0.95:
            text.set_text('>-1')
        elif t == 1:
            text.set_text('1')
        elif t == -1:
            text.set_text('-1')
        else:
            text.set_text(round(t, 2))

    ax0.get_figure().savefig(figure_base_name + '-correlations.png', bbox_inches='tight', dpi=400)
    plt.close()
    logging.info("successfully saved dataframe correlation plot as " + figure_base_name)

