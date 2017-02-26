import file_dir_dialog as fdd  # wjt custom module
import read_txt as rt          # wjt custom module
import plot_generator as pg    # wjt custom module

import pandas as pd            # data analysis package; need for DataFrame object
import re                      # regular expression module
import os                      # python core library package
from os.path import join       # in this case using from...import allows you to type 'join' directly


# create pandas DataFrame objects by reading data from excel
df = pd.read_excel('TagMatchList.xlsx', sheetname='Model Results').set_index('date_time')
df_tml = pd.read_excel('TagMatchList.xlsx', sheetname='TML').set_index('Root')
# create empty lists
cols_new = []
units = []
# at this point, the df column names look like 'FL-WURSL5FL (mgd)',
# but we want the column name to look like 'FL-WURSL5FL' for matching and plotting later.
# split the DataFrame column names by space: new column name is to left of space, units to right
for c in df.columns.tolist():
    cols_new.append(c.split(' ')[0])
    # to be safe, check that there is a space in the column name, as we expect
    if ' ' in c:
        units.append(c.split(' ')[1])
    else:
        units.append('')

# define new column names
df.columns = cols_new
# x values for plotting are the index values, which are Datetime
x = df.index.values
# user picks files to read. get_files() returns a tuple of file paths
for f in fdd.get_files():
    # read_file returns a dictionary of values from the file
    fdata = rt.read_file(f)
    value_typ = fdata['type']
    # 'values' contains the scada values
    y1 = fdata['values']
    # get root file name (:-4 leaves off the file extension). sloppy, since it assumes a three-character extension
    # root = os.path.basename(f)[:-4]
    # better way is:
    fn = os.path.basename(f)
    root = fn[:fn.rindex('.')]

    try:
        # from the tag match list df, get the model id using an index value
        model_id = df_tml.ix[root.strip(), 'Model_ID']
        # get the model results using the name of the column
        y2 = df[model_id].values
        col_index = df.columns.get_loc(model_id)
        unit = units[col_index].strip()
    except KeyError:
        model_id = None
    # if the model id was found, plot the results
    if model_id:
        print(root)
        pg.make_plot(x, y1, 'actual', ylabel=value_typ + ' ' + unit,
                  title=root + '\nSAN ANTONIO WATER SYSTEM\nAugust 14, 2012', format_string='k-o')
        pg.make_plot(x, y2, 'modeled', ylabel=value_typ + ' ' + unit,
                  title=root + '\nSAN ANTONIO WATER SYSTEM\nAugust 14, 2012', format_string='r--o')
        pg.save_as_png(join(os.getcwd(), 'output', root + '.png'))
