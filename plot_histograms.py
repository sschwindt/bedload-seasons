"""
Plot and save histograms of measurement frequency per variable category
"""
try:
    from bedPyLoad.categorize import *
except Exception as e:
    print('Import incomplete - errors likely:\n' + str(e))


def plot_category_histograms(directory):
    """
    plot histograms of all dataframe columns (as per the config.py)
    :param str directory: tell where plots should be saved; either absolute or relative path ending on '/'
                            Important: relative paths should not start with '/' or '\\'
    :return: 0 if successful
    """
    if not os.path.isdir(directory):
        os.makedirs(directory)

    for par in FULL_LABEL_DICT.keys():
        # check if categorical or numeric Series to define bins
        df4a = df[par].dropna()
        if df4a.dtype == float:
            print('...skipping numeric type: ' + par)
            continue
        print('PLOTTING: ' + par)
        # prepare plot
        fig, ax = plt.subplots(1, 1, figsize=(12, 6))
        # make x-labels
        try:
            if not SUB_CATEGORY_ORDER[par]:
                cat_order = df4a.unique().tolist()
            else:
                cat_order = SUB_CATEGORY_ORDER[par]
        except KeyError:
            # skip irrelevant undefined entries in SUB_CATEGORY_ORDER dict
            continue
        # make ys (number of occurrences)
        freq_dict = df4a.value_counts().to_dict()
        frequencies = [freq_dict[i] for i in cat_order]
        # agglomerate into df
        plot_df = pd.DataFrame(
            list(zip(cat_order, frequencies)),
            columns=['Categories', 'Number of Measurements']
        )
        sns.set_style('whitegrid')  # options: darkgrid, whitegrid, dark, white, ticks
        sns.barplot(
            data=plot_df,
            x='Categories',
            y='Number of Measurements',
            palette='blend:#7AB,#EDA',  # 'dark:#5A9_r',
            edgecolor='.3',
            orient='v',
            ax=ax,
            alpha=0.5,
        )
        ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
        ax.grid(visible=True, which='minor', color=[0.88, 0.88, 0.88], linewidth=0.5)
        # ax.set_title(FULL_LABEL_DICT[par])
        ax.set(xlabel=None, ylim=(1, 10000))
        ax.set_yscale('log')
        plt.xticks(rotation=45)  # rotate too-long xlabels
        fig.savefig(directory + '%s.png' % par, dpi=600, bbox_inches='tight')
        print('- saved: ' + directory + '%s.png' % par)
        ax.cla()
        plt.close()


if __name__ == '__main__':
    use_directory = 'figures/histograms/'
    plot_category_histograms(use_directory)
