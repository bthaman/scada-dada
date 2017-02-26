import re


def isfloat(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


def get_attr(key, s, delimiter=':'):
    if key in s:
        pos = s.index(delimiter)
        return s[pos+1:].strip()
    else:
        return None


# added this def as a demonstration of using regex
def get_attr_re(key, s, delim=':'):
    m = re.match('^' + key + delim + '(.*)', s)
    attr = m.group(1).strip() if m else None
    return attr


def read_file(fl):
    file_data = {'description': None, 'type': None, 'num_records': None, 'values': []}
    ch = None
    b_data = False
    f = open(fl, 'r')
    for line in f:
        file_data['description'] = get_attr('Description', line) if 'Description' in line else file_data['description']
        file_data['num_records'] = get_attr('Records', line) if 'Records' in line else file_data['num_records']
        file_data['type'] = get_attr('Channel', line) if 'Channel' in line else file_data['type']
        ch = get_attr_re('Channel', line) if 'Channel' in line else ch
        b_data = True if '[DATA]' in line else b_data
        # following conditional tests to see if the line with '[DATA]' has been passed and that the line
        # contains a float, indicating that values should be read
        if b_data and '[DATA]' not in line and isfloat(line.strip()):
            file_data['values'].append(float(line.strip()))
    return file_data

if __name__ == '__main__':
    import os
    from os.path import join
    import pandas as pd
    f = join(os.getcwd(), 'TXTfiles', 'AdobeRanchFlow.txt')
    print(read_file(f))
    print('')
    # keep in mind that if we didn't want the description etc., that the values can be read directly into a dataframe
    # read_csv works fine, even though the file has a .txt extension
    df = pd.read_csv(f, skiprows=10)
    # do some stuff to the DataFrame
    df.columns = ['DATA']
    df['DATA*2'] = df.DATA * 2
    print(df)