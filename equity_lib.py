import numpy as np
import pandas as pd

def get_award_columns():
    award_columns = ['index', 'Source', 'All Sources',
                 'Final MFD', 'Algorithmic MFD', 'Manual MFD', 'Vendor MFD',
                 'Status', 'Requisition Number', 'Contract Number', 'PO Number',
                 'Number of Instances', 'Date Column',
                 'Award Date', 'Business Name', 'Supplier_Name_Normalized', 'Amount Column', 'Award Amount',
                 'Department Name', 'Item Description 1', 'Item Description 2',
                 'Identifier Type 1', 'Identifier 1',
                 'Identifier Type 2', 'Identifier 2',
                 'Item NIGP 5', 'Item NIGP 3', 'Final Item NIGP',
                 'Item Work Category 3', 'Item Work Category 5', 'Final Item Work Category',
                 'Item Work Categorization Type', 'Potentially Exclude', 'Actually Exclude',
                 'Vendor Number', 'Address1', 'Address2', 'Zip']

    print(award_columns)

def convert_dollars(df,col_name):
    """Converts comma separated dollars into floats """
    df[col_name] = df[col_name].replace('[^.0-9]','',regex=True).astype(float)
    return df

def convert_date_string(df,col_name):
    """Converts date strings into datetime format"""
    df[col_name] = pd.to_datetime(df[col_name], infer_datetime_format=True)
    return df

def parse_email (s):
    """Replace moves removes all spaces: beginning middle and end"""
    s = s.replace(' ','').lower()
    """Parses a string as an email address, returning an (id, domain) pair."""
    pattern = '''
    (?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])
    '''
    matcher = re.compile(pattern, re.VERBOSE)
    matches = matcher.match(s)
    if matches:
        return (matches.group(0))
    else:
        print(s)
        raise ValueError("Bad email address")

def parse_phone(s):
    """
    Any of the below patterns will be parsed as valid phone numbers
    (404) 555-1212
    (404) 5551212
    404-555-1212
    404-5551212
    404555-1212
    4045551212
    """
    pattern = '''
    ^\s* # Leading spaces
    (?P<areacode>
    \d{3}-? # "xxx" or "xxx-"
    | \(\d{3}\)\s* # OR "(xxx) "
    )
    (?P<prefix>\d{3}) # xxx
    -? # Dash (optional)
    (?P<suffix>\d{4}) # xxxx
    \s*$ # Trailing spaces
    '''
    matcher = re.compile(pattern, re.VERBOSE)
    matches = matcher.match(s)
    if matches is None:
        print(s)
        return s
    else:
        areacode = re.search('\d{3}', matches.group ('areacode')).group()
        prefix = matches.group ('prefix')
        suffix = matches.group ('suffix')
        return areacode+'-'+prefix+'-'+suffix

def parse_zip(s):
    s = s.strip()
    """
    Any of the below patterns will be parsed as valid zip codes
    https://stackoverflow.com/questions/2577236/regex-for-zip-code
    12345
    12345-6789
    12345 1234
    123451234
    """
    pattern = '''
     ^\d{5}(?:[-\s]?\d{4})?$
    '''
    matcher = re.compile(pattern, re.VERBOSE)
    matches = matcher.match(s)
    if matches:
        return (matches.group(0))
    else:
        print(s)
        return np.nan

def clean_zip_codes(df,df_name,zip_column):
    df[zip_column] = df[zip_column].astype(str)
    '''
    This function parses all zip codes with a regular expression. All valid zip codes
    are put in the newly created column called "Valid Zip". Any invalid zip code will 
    not be transferred and will require manual resolution. The explicit lines needed
    to correct the invalid zip codes is output as well.
    '''

    def parse_zip(s):
        s = str(s).strip()
        """
        Any of the below patterns will be parsed as valid zip codes
        https://stackoverflow.com/questions/2577236/regex-for-zip-code
        12345
        12345-6789
        12345 1234
        123451234
        """
        pattern = '''
         ^\d{5}(?:[-\s]?\d{4})?$
        '''
        matcher = re.compile(pattern, re.VERBOSE)
        matches = matcher.match(s)
        if matches:
            return (matches.group(0))
        else:
            return np.nan

    # Data Cleaning Function data cleaner loc statement cleaning zip code corrector
    def data_cleaner(df, df_name, messy_column_name, new_column, use_custom_array=False,custom_array=False):
        if use_custom_array:
            array = custom_array
        else:
            array = df[messy_column_name].unique()

        for i in array:
            print(df_name + '.loc[' + df_name + '[\'' + messy_column_name + '\']==\'' + str(
                i) + '\',\'' + new_column + '\'] = \'\'')

    df['Valid Zip'] = df[df[zip_column].notnull()][zip_column].apply(parse_zip)
    custom_array = df[(df[zip_column].notnull())&(df['Valid Zip'].isnull())][zip_column].unique()
    data_cleaner(df,df_name,zip_column,'Valid Zip',True,custom_array)

def import_directory(path):
    import glob

    # path = r + path  # use your path
    all_files = glob.glob(path + "/*.xlsx")

    li = []

    for filename in all_files:
        df = pd.read_excel(filename, index_col=None, header=0)
        li.append(df)

    return pd.concat(li, axis=0, ignore_index=True)


def get_exclusion_reasons():
    list_1 = ['Duplicate', 'Invalid Award Amount',
              'Less than 1000', 'No Vendor', 'Null Award Amount',
              'Exclusion Category', 'Award Status']

    print(list_1)

# Firm Name Cleaning Used https://medium.com/@isma3il/supplier-names-normalization-part1-66c91bb29fc3
# for inspiration, then tweaked
def clean_names_frame(df,name_column):
    # Renaming business name column
    # df.rename(columns={name_column:'Supplier_Name'},inplace=True)

    # Libraries
    from cleanco import cleanco
    # Import supplier names to dataframe
    # ----------------------------------------
    # Convert to uppercase
    df['Supplier_Name_Normalized'] = df[name_column].apply(lambda x: str(x).upper())
    # Remove commas
    df['Supplier_Name_Normalized'] = df['Supplier_Name_Normalized'].apply(lambda x: str(x).replace(',', ''))
    # Remove apostrophe
    df['Supplier_Name_Normalized'] = df['Supplier_Name_Normalized'].apply(lambda x: str(x).replace("''", ''))
    # Remove hyphens
    df['Supplier_Name_Normalized'] = df['Supplier_Name_Normalized'].apply(lambda x: str(x).replace(' - ', ' '))
    # Remove text between parenthesis
    df['Supplier_Name_Normalized'] = df['Supplier_Name_Normalized'].apply(lambda x: str(x).replace(r"\(.*\)", ""))
    # Replacing AND with symbol
    df['Supplier_Name_Normalized'] = df['Supplier_Name_Normalized'].apply(lambda x: str(x).replace(' AND ', ' & '))
    # Remove spaces in the begining/end
    df['Supplier_Name_Normalized'] = df['Supplier_Name_Normalized'].apply(lambda x: str(x).strip())
    # Remove business entities extensions (1)
    df['Supplier_Name_Normalized'] = df['Supplier_Name_Normalized'].apply(
        lambda x: cleanco(x).clean_name() if type(x) == str else x)
    # Remove dots
    df['Supplier_Name_Normalized'] = df['Supplier_Name_Normalized'].apply(lambda x: str(x).replace('.', ''))
    # Remove business entities extensions (2) - after removing the dots
    df['Supplier_Name_Normalized'] = df['Supplier_Name_Normalized'].apply(
        lambda x: cleanco(x).clean_name() if type(x) == str else x)
    # Specific Polish to companies
    df['Supplier_Name_Normalized'] = df['Supplier_Name_Normalized'].apply(lambda x: str(x).replace('SP ZOO', ''))

    # Count unique values
    print('Supplier names:', df[name_column].nunique())
    print('Normalized names:', df['Supplier_Name_Normalized'].nunique())


# A narrowly defined algorithm meant to extract values from a PDF with poor table design
# This crawls through the frame and pulls out data that is supposed to be in one row
# But because of the table converted it gets stored in a lower row with a separate index
# This problem originally solved in the Prism Vendor file
def extract_codes(df):
    last_filled_index = 0
    for row in df.itertuples(index=True,name='Pandas'):
        name = str(getattr(row,'_1'))
        nigp = str(getattr(row,'_2')).lstrip().rstrip()
        if(name!='nan'):
            last_filled_index = getattr(row,'Index')
        else:
            pass
        if(nigp[0].isdigit()):
            if(df.at[last_filled_index,'NIGP String']!=''):
                old_value = df.at[last_filled_index,'NIGP String']
                df.at[last_filled_index,'NIGP String'] = old_value+';'+nigp
            else:
                df.at[last_filled_index,'NIGP String'] = nigp

# This function determines what percent of a file matches with a database, making sure all values are unique
def percentFileMatched(database, file, shared_column, filter_column):
    # Drop duplicates by shared column on both db and file
    db_temp = database.drop_duplicates(subset=[shared_column])
    file_temp = file.drop_duplicates(subset=[shared_column])
    # Unique number of entries
    unique_db = len(db_temp[shared_column].unique())
    unique_file = len(file_temp[shared_column].unique())

    print('unique_db: ' + str(unique_db))
    print('unique_file: ' + str(unique_file))

    # Merge file to db
    results = db_temp.merge(file_temp, on=shared_column, how='left')
    results = results[results[filter_column].notnull()].copy()

    # results = results[results[filter_column].notnull()]
    number_matches = len(results)
    print('number_matches: ' + str(number_matches))
    print('percent matched: ' + str(number_matches / unique_file))

    return results


# Exporting Excel Files
def export_excel(df_list, sheet_names, path):
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    for i in range(len(df_list)):
        df_list[i].to_excel(writer, sheet_name=sheet_names[i], index=False)
    writer.save()


# Data frame value counter frequency counter
def valueCounter(df, path):
    f = open(path, "w+")
    for i in range(df.shape[1]):
        colname = df.columns[i]
        f.write('Column Name: ' + colname + '\n')
        f.write('Number of Values: ' + str(len(df[colname])) + '\n')
        f.write('Number of Unique Values: ' + str(len(df[colname].unique())) + '\n')
        f.write('-----------------------------------------------------------' + '\n')
        f.write(str(df.iloc[:, i].value_counts(dropna=False)) + '\n')
        f.write('\n\n')

    f.close()


# Exclusion Algorithm
def mfd_exclusions(df, name_column):

    exclusion_list = ['Charles','Maryland','Baltimore','MD','City','County','Sheriff','Department','Fire','Country','States','State','United','U.S.','Federal','Council','Government','Govt.','Church','Ministries',
                    'Ministry','Theaters','Theater','Clubs','Foundations','Foundation','Publishing','Institute','Association','League','Libraries','Library','Scouts','Scout','School','Daycare','Learning','Chapter',
                    'Commissions','Commission','YMCA','YWCA','College','University','Society','Chamber','Hospitals','Hospital','Bureau','Department','Agency','National','Goodwill','Salvation','Unions','Union','Catholic',
                    'Baptist','Methodist','Muslim','Jewish','Presbyterian','Episcopal','Junior','Circuit','Court','Alliance','District','A.S.S.N','Habitat','Humanity','Non-profit','Organization','Authority','Center',
                    'Development','Campaign','Conference','Board','Division','Awareness','Christian','Museum','Charity','Health Care','Health','Dept','Coalition','Collaborative','Trust','Park','Natl','Committee','Sports',
                    'Sport','Habitat','Centers','Treasury','Dep','United','Govrnt','Gov','Govt','YMCA','Community','Assn','Univ','Municipal','Police','Assoc','Cross','Public','Safety','Agncy','Enforcement','Children',
                    'Partnership','Nursery','Depart','SPA','RESORT','BANK']
    
    print(exclusion_list)
    
    df['Potentially Exclude'] = False
    for index, row in df.iterrows():
        array = df.iloc[index][name_column].title().split()
        # print(array)
        for i in range(len(array)):
            # print(i)
            if array[i] in exclusion_list:
                # print(i)
                df.at[index, 'Potentially Exclude'] = True


# Find intersection of two dataframe's column name
def column_overlap(df_1, df_2):
    print(set(df_1.columns).intersection(set(df_2.columns)))


# Print list of columns fill when align aligning compare
def frame_align(list_of_columns, df, df_name):
    for i in np.setdiff1d(list_of_columns, df.columns):
        print(df_name + '[\'' + i + '\'] = np.nan')


# Prioritize prioritization Algorithm
def source_prioritizer(all_sources):
    highest_priority = ''

    if 'Buyspeed' in all_sources:
        highest_priority = 'Buyspeed'
    elif 'MyPro' in all_sources:
        highest_priority = 'MyPro'
    elif 'OnBase Web Data' in all_sources:
        highest_priority = 'OnBase Web Data'
    elif '2013 2018 SoleSource for Disparity Study' in all_sources:
        highest_priority = '2013 2018 SoleSource for Disparity Study'
    elif 'Disparity Query for Prime info No Goals' in all_sources:
        highest_priority = 'Disparity Query for Prime info No Goals'
    elif 'Novus' in all_sources:
        highest_priority = 'Novus'
    else:
        highest_priority = 'NO MATCH'

    return highest_priority


# Work Categorization Algorithm Classification
def assign_work_category(df):
    # work_category_manual_search['Auto Work Category'] = ''
    # work_category_manual_search['Match Count'] = np.NaN

    # County Names, State Names, City Names, Federal Agencies

    construction = ['Contractor', 'Renovations', 'Builder', 'Paint', 'Trucking', 'Hauling', 'Demolition', 'Fence',
                    'Fencing', 'Grading', 'Paving', 'Pave', 'Concrete', 'Roof', 'Electrical', 'Install', 'Installation',
                    'Plumbing', 'Restoration', 'Windows', 'Door Replacement', 'Asbestos', 'Abatement', 'Heating', 'Air',
                    'Resurface', 'Drainage', 'Masonry', 'Flooring']
    construction_1 = ['Contractors', 'Contracting', 'Builders', 'Builder', 'Painting', 'Remodeling', 'Roofing',
                      'Electric', 'Energy', 'Floors', 'Floor', 'Construction', 'Building']
    ane = ['Engineer', 'Architect', 'Environmental', 'Survey', 'Design', 'Erosions', 'Inspections', 'Archeologist',
           'Infrastructure', 'Aerospace']
    ane_1 = ['Engineering', 'Surveying', 'Mapping', 'Planning']
    p_services = ['Health', 'Audit', 'Medical', 'Consultants', 'Lawyer', 'Law', 'Legal', 'Bank', 'Account',
                  'Psychology', 'Financial', 'Counseling', 'Business Analyst', 'Pharmacy', 'Pharmaceuticals']
    p_services_1 = ['Tax', 'Cpa']
    o_services = ['Childcare', 'Repair', 'Towing', 'Solution', 'Research', 'Service', 'Maintenance', 'Restoration',
                  'Restaurant', 'Enforcement', 'Parking', 'Sales', 'Technology', 'Management', 'Lawn', 'Landscaping',
                  'Landscape', 'Data', 'Staffing', 'Cleaning', 'Transportation', 'Janitor', 'Waste', 'Pest',
                  'Associates', 'Advertising', 'Real Estate', 'Printing', 'Security', 'Marketing', 'Graphic Design',
                  'Interior Design', 'Training', 'Software Maintenance', 'Insurance', 'Delivery']
    o_services_1 = ['Child Care', 'Daycare', 'Preschool', 'Creative', 'Solutions', 'Technologies', 'Lawncare',
                    'Landscapes', 'Learning', 'Photography', 'Graphics', 'Graphic', 'Imaging', 'Media', 'Systems',
                    'Fire', 'Protection']
    goods = ['Good', 'Parts', 'Equipment', 'Supply', 'Break', 'Car', 'Truck', 'Tire', 'Hardware', 'Product', 'Rental',
             'Sheet Metal Fabrication', 'Lease', 'Software', 'License']
    goods_1 = ['Supplies', 'Prosthetics', 'Furnishings', 'Manufacturing', 'Distribution', 'Distributing']

    construction.extend(construction_1)
    ane.extend(ane_1)
    p_services.extend(p_services_1)
    o_services.extend(o_services_1)
    goods.extend(goods_1)
    # print(construction)

    for index, row in df.iterrows():
        array = str(df.at[index, 'Smoothed Name']).replace(',', ' ').replace('.', ' ').title().split()
        #         print(array)
        matchCount = 0
        for i in range(len(array)):
            #             print(i)

            if array[i] in construction:
                if matchCount == 0:
                    df.at[index, 'Auto Work Category'] = 'Construction'
                matchCount += 1
                df.at[index, 'Match Count'] = matchCount
            elif array[i] in ane:
                if matchCount == 0:
                    df.at[index, 'Auto Work Category'] = 'A & E'
                matchCount += 1
                df.at[index, 'Match Count'] = matchCount
            elif array[i] in p_services:
                if matchCount == 0:
                    df.at[index, 'Auto Work Category'] = 'Professional Services'
                matchCount += 1
                df.at[index, 'Match Count'] = matchCount
            elif array[i] in o_services:
                if matchCount == 0:
                    df.at[index, 'Auto Work Category'] = 'Other Services'
                matchCount += 1
                df.at[index, 'Match Count'] = matchCount
            elif array[i] in goods:
                if matchCount == 0:
                    df.at[index, 'Auto Work Category'] = 'Goods'
                matchCount += 1
                df.at[index, 'Match Count'] = matchCount
    #             else:
    #                 df.at[index,'Auto Work Category'] = np.NaN

    df['Auto Work Category'] = df['Auto Work Category'].replace('', np.NaN)

    return df


# Resmooth a dataframe that has been smoothed before but need to add new sources
def resmooth(smoothed, unsmoothed, smoothing_file_path):
    smoothed.drop(['Smoothed Name'], axis=1, inplace=True)

    unsmoothed['Business Name'] = unsmoothed['Business Name'].astype(str).apply(lambda x: x.lstrip())
    unsmoothed['Business Name'] = unsmoothed['Business Name'].astype(str).apply(lambda x: x.rstrip())
    unsmoothed['Business Name'] = unsmoothed['Business Name'].replace('nan', np.nan)

    df = pd.concat([smoothed, unsmoothed])
    print('Number of rows of combined frame: ' + str(len(df)))
    df.drop_duplicates(subset=['Source', 'Business Name'], inplace=True)
    print('Number of rows of combined frame, dups dropped by Source AND Business Name: ' + str(len(df)))

    smoothing_file = pd.read_excel(smoothing_file_path)
    smoothing_file = smoothing_file[['Source', 'Business Name', 'Smoothed Name']]

    df = df.merge(smoothing_file, on=['Source', 'Business Name'], how='left')
    values = {'Smoothed Name': 'name_to_be_smoothed'}
    df.fillna(value=values, inplace=True)

    df['Sort Upper'] = df['Business Name'].str.upper()
    df.sort_values(by='Sort Upper', inplace=True)

    print('Number of rows to be smoothed: ' + str(len(df[df['Smoothed Name'] == 'name_to_be_smoothed'])))

    return df


# Mark Duplicates
def mark_duplicates(df, column_list):
    df['Duplicate'] = df.duplicated(subset=column_list)
    df.loc[(df['Duplicate'] == True)&(df['MFD'].isnull()), 'MFD'] = 'Dup by:' + ','.join(column_list)
    df.drop(['Duplicate'], axis=1, inplace=True)
    return df


# Getting the frequency count number of times a value appears in a data frame
# two_cols is the generally two columns that should drop dups on
# for example: ['Primary Key','HUB Certification']
# This example finds if there are conflicts for that data
def get_number_of_instances(df, find_conflicts, primary_key, two_cols):
    # You would drop dups only in instance where you're trying to find the
    # conflicts
    if find_conflicts == True:
        temp = df.drop_duplicates(subset=two_cols)
    else:
        temp = df.copy()

    name_counts = temp[primary_key].value_counts().rename('number_of_instances')
    dup_names = temp.merge(name_counts.to_frame(),
                           left_on=primary_key,
                           right_index=True)

    if find_conflicts == True:
        dup_names = dup_names[dup_names['number_of_instances'] > 1]

    return dup_names


# Regular Expression Req Number regex
def get_five_digits(req):
    import re

    x = re.findall('([\d]{5})', req)
    if not x:
        return np.nan
    else:
        string = ';'.join(x)
        return string


# Changing default number of rows all columns displayed show all
def set_max_columns():
    pd.set_option('display.max_columns', None)


def set_max_rows():
    pd.set_option('display.max_rows', None)


# Extracting values from comma separated cells new line
def extract_new_line_data(df):
    # tnucp.rename(columns={0:'Col0',1:'Col1',2:'Col2',3:'Col3',4:'Col4',5:'Col5'},inplace=True)
    for index, row in df.iterrows():
        array = str(df.iloc[index]['Company Information ']).split('\n')
        for i in range(len(array)):
            df.at[index, i] = array[i]

    return df


# Marking Exclusions
def mark_exclusions(df):
    df.loc[(~(df['Award Date'] >= '1-1-14') | ~(df['Award Date'] <= '12-31-18')) & (
        df['MFD']).isnull(), 'MFD'] = 'Outside Date Range'
    df.loc[
        ((df['Award Amount'].isnull()) | (df['Award Amount'] == 0)) & (df['MFD'].isnull()), 'MFD'] = 'Null Award Amount'
    df.loc[(df['Award Amount'] < 1000) & (df['MFD']).isnull(), 'MFD'] = 'Less than 1000'


# Marking Data Gaps
# Creating a function to mark exclusions where multiple individual items can be placed in the MFD column The goal should be to preserve
# what is already in MFD and to exclude rows that have much deeper reasons for exclusions such as being exclusion categories or less than threshold map
def mark_gaps(df):
    # Set a boolean so that we can maintain the integrity of not overwriting those rows that have deeper exclusion reasons
    # (hence the benefit of the MFD.isnull check in the loc statements)
    df.loc[df['MFD'].notnull(), 'Hard Exclusion'] = 'Y'
    # Make all null values empty strings
    df['MFD'].replace(np.nan, '', inplace=True)
    # Marking Gaps
    df.loc[(df['Zip'].isnull()) &
           (df['Hard Exclusion'].isnull()), 'MFD'] = df['MFD'] + 'No Zip,'
    df.loc[(df['Work Category'].isnull()) &
           (df['Hard Exclusion'].isnull()), 'MFD'] = df['MFD'] + 'No WC,'
    df.loc[(df['Work Category'] == '?') &
           (df['Hard Exclusion'].isnull()), 'MFD'] = df['MFD'] + 'No WC,'
    # Fixing the good rows so they have null values in the MFD again
    df['MFD'].replace('', np.nan, inplace=True)
    return df


def sort_consolidated_values(consolidated_values):
    consolidated_values = str(consolidated_values)
    if(consolidated_values == 'nan'):
        return np.nan
    else:
        sorted_values = ';'.join(sorted(consolidated_values.split(';'),key=str.lower))
        return sorted_values

def get_number_of_values(all_work_categories):
    all_work_categories = str(all_work_categories)
    num_work_categories = 0
    for char in all_work_categories:
        if char == ';':
            num_work_categories += 1
    if(all_work_categories=='nan'):
        return 0
    elif(num_work_categories == 0):
        return 1
    else:
        # plus 1 because semicolons offset the count by 1
        return num_work_categories+1

# Get the unique strings within a delimited semi colon separated string
def get_unique(string):
    string = str(string)
    # intilize a null list
    unique_list = []
    list1 = string.split(';')
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    # print list
    final_string = ';'.join(unique_list)

    if(final_string=='nan'):
        return np.nan
    else:
        return final_string

# Converting Force forcing multiple rows to a single row and preserving unique data collapse condense consolidate
def consolidate_values(consolidate_col, primary_key, df, get_unique_values=True, drop_dup=False):
    df[consolidate_col] = df[consolidate_col].astype(str)
    consolidated_values = df.groupby(primary_key)[consolidate_col].apply(';'.join).reset_index()
    consolidated_values.rename(columns={consolidate_col: 'All ' + consolidate_col + 's'}, inplace=True)
    df = df.merge(consolidated_values, on=primary_key, how='left')

    if drop_dup == True:
        df.drop_duplicates(subset=[primary_key], inplace=True)

    created_column_name = 'All ' + consolidate_col + 's'

    df[created_column_name] = df[created_column_name].astype(str).apply(lambda x: x.replace('nan;', ''))
    df[created_column_name] = df[created_column_name].astype(str).apply(lambda x: x.replace(';nan', ''))
    df.loc[df[created_column_name] == 'nan', created_column_name] = np.nan

    # Sorting values
    df[created_column_name] = df[created_column_name].apply(sort_consolidated_values)

    # Getting Number of Values
    number_of_values = 'Number of ' + consolidate_col + 's'
    df[number_of_values] = df[created_column_name].apply(get_number_of_values)

    if get_unique_values == True:
        unique_column_name = 'All Unique ' + consolidate_col + 's'

        df[unique_column_name] = df[created_column_name].apply(get_unique)
        df[unique_column_name].replace('nan', np.nan, inplace=True)
        # Removing the created column which is arbitrary with unique option passed
        df.drop([created_column_name],axis=1,inplace=True)
        df[number_of_values] = df[unique_column_name].apply(get_number_of_values)

    return df


# Convert float to string
def float_to_string(string):
    string = str(string)
    if string == 'nan':
        string = np.nan
    else:
        string = string.split('.')[0]

    return string


# Convert NAICS to NIGP
def naics_to_nigp(master, path):
    crosswalk = pd.read_excel(path)
    crosswalk['NAICS'] = crosswalk['NAICS'].astype(str)
    crosswalk['NIGP 5'] = crosswalk['NIGP_CODE'].astype(str)
    crosswalk['NIGP 3'] = crosswalk['NIGP 5'].astype(str).apply(lambda x: x[:3])
    crosswalk = crosswalk[['NAICS', 'NIGP 5', 'NIGP 3', 'NIGP_Description']]
    # There are multiple NIGP codes for a single NAICS code but I have already verified that it is arbitrary.
    crosswalk.drop_duplicates(subset=['NAICS'], inplace=True)

    def fix_nigp_5(string):
        string = str(string)
        if len(string) == 4:
            return '0' + string
        elif len(string) == 3:
            return '00' + string
        else:
            return string

    crosswalk['NIGP 5'] = crosswalk['NIGP 5'].apply(fix_nigp_5)
    master = master.merge(crosswalk, on='NAICS', how='left')
    return master

def nigp_to_work_category(master,path='../data/1.0-ob-GSPC-NIGP-Conversion-Lookup.xlsx',os_name='Other Services',ane_name='Architecture & Engineering'):
    '''
    Convert a cleaned NIGP 5 and NIGP 3 column in an existing dataframe to work category based on
    a lookup table passed in the optional path parameter. Attempts to convert 5 digit NIGP when possible,
    but will default to 3 digit if a match does not exist in the lookup table.
    '''
    original_size = len(master)

    nigp = pd.read_excel(path,converters={"Commodity Code":str})

    nigp.loc[nigp['Industry Classification']=='Non-Professional Services','Industry Classification'] = os_name
    nigp.loc[nigp['Industry Classification']=='Construction Related Professional Services','Industry Classification'] = ane_name

    # If the last two digits of the code are something other than '00', it is a five digit code
    nigp_5 = (nigp[nigp['Commodity Code'].apply(lambda x: x[3:5])!='00']
              .dropna(subset=['Industry Classification'])
              .drop_duplicates(subset=['Commodity Code'])
              .rename(columns={"Commodity Code":'NIGP 5','Commodity Description':'Commodity Description 5','Industry Classification':'NIGP 5 Category'}))

    # If the last two digits of the code are '00', it is a 3 digit code
    nigp_3 = nigp[nigp['Commodity Code'].apply(lambda x: x[3:5])=='00'].copy()

    nigp_3['Commodity Code'] = nigp_3['Commodity Code'].apply(lambda x: str(x)[:3])

    nigp_3 = (nigp_3
              .dropna(subset=['Industry Classification'])
              .drop_duplicates(subset=['Commodity Code'])
              .rename(columns={"Commodity Code":'NIGP 3','Commodity Description':'Commodity Description 3','Industry Classification':'NIGP 3 Category'}))

    master = master.merge(nigp_5,on='NIGP 5',how='left')
    master = master.merge(nigp_3,on='NIGP 3',how='left')

    assert len(master) == original_size

    master['NIGP Item Work Category'] = master['NIGP 5 Category']
    master.loc[(master['NIGP 5 Category'].isnull())&(master['NIGP 3 Category'].notnull()),'NIGP Item Work Category'] = master['NIGP 3 Category']

    print('The following NIGP 5 did not merge: ')
    print(master[(master['NIGP Item Work Category'].isnull())&(master['NIGP 5'].notnull())]['NIGP 5'].value_counts())

    print('The following NIGP 3 did not merge: ')
    print(master[(master['NIGP Item Work Category'].isnull())&(master['NIGP 3'].notnull())]['NIGP 3'].value_counts())

    return master

# Creating Unique Arrays for the Relevant Market Regions
Main_County = {
    'Hamilton County': 'TN'
}
MSA_Counties = {
    'Catoosa County': 'GA',
    'Dade County': 'GA',
    'Marion County': 'TN',
    'Sequatchie County': 'TN',
    'Walker County': 'GA'
}
CSA_Counties = {
    'Bradley County': 'TN',
    'Jackson County': 'AL',
    'Mcminn County': 'TN',
    'Murray County': 'GA',
    'Polk County': 'TN',
    'Rhea County': 'TN',
    'Whitfield County': 'GA'
}
Surrounding_Counties = {
    'Bledsoe Couny': 'TN',
    'Meigs County': 'TN'
}
Main_State = 'TN'
Relevant_States = ['TN', 'GA', 'KY', 'VA', 'NC', 'AL', 'MS', 'MO', 'AR']
Relevant_Market_Order = ['Main County', 'MSA', 'CSA', 'Surrounding Counties', 'TN', 'GA', 'KY', 'VA', 'NC', 'AL', 'MS',
                         'MO', 'AR', 'USA']


# This function checks if the value of the passed dictionary matches the passed state
# For this to work, the dictionary needs to be inverted because searching a dictionary
# only works on keys, so the key value pair needs to be flipped

# This is a helper function for the create_relevant_market function

def check_inverse_mapping(state, dictionary):
    # Inverting the mapping of the dictionary so I can check both key and value in a one line if statement
    # https://stackoverflow.com/questions/483666/python-reverse-invert-a-mapping
    inv_map = {}
    for k, v in dictionary.items():
        # inv_msa[v] = inv_msa.get(v, [])
        # inv_msa[v].append(k)
        inv_map.setdefault(v, []).append(k)

    if state in inv_map:
        return True
    else:
        return False


def create_relevant_market(df):
    df['Relevant Market Region'] = ''

    for index, row in df.iterrows():
        temp_state = df.iloc[index]['State'].strip()
        temp_county = df.iloc[index]['County'].strip()
        if temp_county in Main_County and temp_state == Main_County[temp_county]:
            df.at[index, 'Relevant Market Region'] = 'Main County'
        elif temp_county in MSA_Counties and check_inverse_mapping(temp_state, MSA_Counties):
            df.at[index, 'Relevant Market Region'] = 'MSA'
        elif temp_county in CSA_Counties and check_inverse_mapping(temp_state, CSA_Counties):
            df.at[index, 'Relevant Market Region'] = 'CSA'
        elif temp_county in Surrounding_Counties and check_inverse_mapping(temp_state, Surrounding_Counties):
            df.at[index, 'Relevant Market Region'] = 'Surrounding Counties'
        elif temp_state in Relevant_States:
            df.at[index, 'Relevant Market Region'] = temp_state
        else:
            # Else it is within the USA
            df.at[index, 'Relevant Market Region'] = 'USA'


# Fix Clean NIGP
def fix_nigp_3(string):
    string = str(string)
    if len(string) == 1:
        return '00' + string
    elif len(string) == 2:
        return '0' + string
    else:
        return string

    rom_nigp['NIGP 3'] = rom_nigp['NIGP 3'].apply(fix_nigp_3)


def fix_nigp_5(string):
    string = str(string)
    if len(string) == 4:
        return '000' + string
    elif len(string) == 3:
        return '00' + string
    else:
        return string


def fix_nigp_7(string):
    string = str(string)
    if len(string) == 6:
        return '0' + string
    elif len(string) == 5:
        return '00' + string
    elif len(string) == 4:
        return '000' + string
    elif len(string) == 3:
        return '0000' + string
    elif len(string) == 2:
        return '00000' + string
    else:
        return string


# Distance between two strings Levenshtein Distance similarity
from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


# Clean Simple Cleaning Phone Numbers Email

def clean_phone(string):
    string = str(string).replace(" ", "").replace("(", "").replace(")", "").replace("-", "").replace(".", "")
    string = str(string)[:10]

    if len(string) < 10:
        return np.nan
    else:
        return string


# Data Cleaning Function data cleaner loc statement cleaning zip code corrector
def data_cleaner(df, df_name, messy_column_name, new_column, use_custom_array=False,custom_array=False):
    if use_custom_array:
        array = custom_array
    else:
        array = df[messy_column_name].unique()

    for i in array:
        print(df_name + '.loc[' + df_name + '[\'' + messy_column_name + '\']==\'' + str(
            i) + '\',\'' + new_column + '\'] = \'\'')

# Clean Cleaning Names
def cleanest_names(df, name_column, no_new_column):
    df['Cleanest Name'] = df[name_column]
    df['Cleanest Name'] = df['Cleanest Name'].apply(lambda x: str(x).replace("&", ''))
    df['Cleanest Name'] = df['Cleanest Name'].apply(lambda x: str(x).replace("-", ''))
    df['Cleanest Name'] = df['Cleanest Name'].apply(lambda x: str(x).replace(',', ''))
    df['Cleanest Name'] = df['Cleanest Name'].apply(lambda x: str(x).replace('.', ''))
    df['Cleanest Name'] = df['Cleanest Name'].apply(lambda x: str(x).replace("'", ''))
    df['Cleanest Name'] = df['Cleanest Name'].apply(lambda x: str(x).upper())
    df['Cleanest Name'] = df['Cleanest Name'].apply(lambda x: str(x).lstrip())
    df['Cleanest Name'] = df['Cleanest Name'].apply(lambda x: str(x).rstrip())
    df['Cleanest Name'] = df['Cleanest Name'].apply(lambda x: str(x)[:-4] if x.endswith('llc') else x)
    df['Cleanest Name'] = df['Cleanest Name'].apply(lambda x: str(x)[:-5] if x.endswith('pllc') else x)
    df['Cleanest Name'] = df['Cleanest Name'].apply(lambda x: str(x)[:-4] if x.endswith('inc') else x)
    df['Cleanest Name'] = df['Cleanest Name'].apply(lambda x: str(x)[:-4] if x.endswith('ltd') else x)
    df['Cleanest Name'] = df['Cleanest Name'].apply(lambda x: str(x)[:-5] if x.endswith('corp') else x)
    df['Cleanest Name'] = df['Cleanest Name'].apply(lambda x: str(x).replace(" ", ''))

    if no_new_column:
        df[name_column] = df['Cleanest Name']
        df.drop(['Cleanest Name'], axis=1, inplace=True)


# Award File Columns needed
def get_utilization_columns():
    list_1 = ['Number of Instances', 'MFD', 'Source', 'Pulled From', 'ACTIVE_FLAG', 'Business Name',
              'Smoothed Name', 'Owner', 'Phone', 'Email', 'Address',
              'City', 'County', 'State', 'Zip', 'DBE Category', 'Work Description',
              'NIGP 5', 'NIGP 3', 'Work Category',
              'Work Categorization Type', 'Potential Minority Identifier',
              'Relevant Market Region',
              'Po Number', 'Po Creation Date',
              'Status',
              'Po Item Description',
              'Po Comments', 'Item Category',
              'Small Business Flag', 'Women Owned Flag',
              'Actual Shipment Amount', 'Final Work Category',
              'Potentially Exclude',
              'Null Shipment Amount',
              'Department Name', 'Ethnicity', 'Certification']

    for i in list_1:
        print(i)


def get_vendor_columns():
    list_1 = ['Number of Instances', 'ACTIVE_FLAG', 'MFD', 'Source', 'Pulled From', 'Business Name',
              'Smoothed Name', 'VENDOR_NBR', 'Owner', 'Phone', 'Email', 'Address',
              'City', 'County', 'State', 'Zip', 'DBE Category', 'Work Description',
              'NIGP 5', 'NIGP 3', 'Ethnicity', 'Certification', 'Work Category',
              'Work Categorization Type', 'Potential Minority Identifier',
              'Relevant Market Region', 'Potentially Exclude']

    for i in list_1:
        print(i)


# Expand Explode semi colon separated values into new rows
def explode_delimited(df, delimited_col, delimiter):
    s = df[delimited_col].str.split(delimiter, expand=True).stack()
    i = s.index.get_level_values(0)
    df2 = df.loc[i].copy()

    new_col = 'New ' + delimited_col

    df2[new_col] = s.values

    # Strip is important here because it removes white spaces
    df2[new_col] = df2[new_col].apply(lambda x: x.strip())
    return df2


# Create horizontal bar create meta table

def createMetaTable(df):
    col_names = []
    col_amount = []
    col_unique = []

    for col in df.columns:
        col_names.append(col)

        col_name = str(col)
        temp = df.dropna(subset=[col_name])
        col_amount.append(len(temp[col_name]))

        col_unique.append(len(temp[col_name].unique()))

    # intialise data of lists.
    data = {'Column Name': col_names, 'Fill Amount': col_amount, 'Number Unique': col_unique}

    # Create DataFrame
    df = pd.DataFrame(data)
    df.sort_values(by=['Fill Amount', 'Number Unique'], ascending=False, inplace=True)

    # Marking columns with less than 5 percent of the max number of rows
    maxValue = df['Fill Amount'].max()
    df.loc[df['Fill Amount'] < (0.05 * maxValue), 'Less than 5 Percent'] = 'Y'

    return df


def createLayeredBar(meta, path):
    import altair as alt

    # Ref: https://altair-viz.github.io/user_guide/generated/core/altair.EncodingSortField.html
    # Ref: https://altair-viz.github.io/user_guide/encoding.html#sorting-legends
    # Ref: https://vega.github.io/vega/docs/schemes/

    meta_fill = meta[['Column Name', 'Fill Amount']].copy()
    meta_fill.rename(columns={'Fill Amount': 'Amount'}, inplace=True)
    meta_unique = meta[['Column Name', 'Number Unique']].copy()
    meta_unique.rename(columns={'Number Unique': 'Amount'}, inplace=True)
    meta_fill['Type'] = 'Fill Amount'
    meta_unique['Type'] = 'Number Unique'
    meta = pd.concat([meta_fill, meta_unique])

    alt.renderers.enable('notebook')

    chart = alt.Chart(meta).mark_bar(opacity=0.7).encode(
        x=alt.X('Amount:Q', stack=None),
        y=alt.Y('Column Name:O', sort=alt.EncodingSortField(field='Amount', op='count', order='ascending')),
        # color="Type",
        color=alt.Color('Type', scale=alt.Scale(scheme='dark2')),
        tooltip=['Column Name', 'Type', 'Amount']
    ).interactive()

    chart.save(path)

    return chart


# Pandas Profile Profiling
def pandas_profiler(df, df_name, path):
    import pandas_profiling as pp
    profile = pp.ProfileReport(df)
    profile.to_file(outputfile="../references/profiles/Profile_" + df_name + ".html")

def apply_null_exclusions(df,exclusion_list,exclusion_column_name):
    '''
    Looping through the list of exclusions -> Exclusions must be based on a null value
    If MFD is null, then it places the exclusion at the exact index
    If MFD is not null, it appends the new exclusion to the list
    '''
    for i in range(len(exclusion_list)):
        df.loc[(df[exclusion_list[i]].isnull())&(df[exclusion_column_name].notnull()),exclusion_column_name] = df[exclusion_column_name]+';No ' + exclusion_list[i] + ' data'
        df.loc[(df[exclusion_list[i]].isnull())&(df[exclusion_column_name].isnull()),exclusion_column_name] = 'No ' + exclusion_list[i] + ' data'

    return df


# Zip Code Merge
import re
def zip_code_merge(df,path_to_zip_db):

    zipcodes = pd.read_excel(path_to_zip_db,dtype='object')
    zipcodes.rename(columns={'State': 'State Merged'}, inplace=True)
    zipcodes = zipcodes[['Zip', 'County', 'State Merged']].copy()

    # Regular Expression for sequence of 5 digits
    def clean_zip(zipcode):
        x = re.findall('([\d]{5})', zipcode)
        if not x:
            return np.nan
        else:
            string = ';'.join(x)
            return string

    df['Zip'] = df['Zip'].astype(str).apply(clean_zip)
    df = df.merge(zipcodes, on='Zip', how='left')
    print(df[df['County'].isnull()]['Zip'].value_counts())

    return df

# Merging on shared column updating old values with new values
def replace_column(df, nf, shared_col, old_col, new_col):
    nf = nf[[shared_col, new_col]]
    df = df.merge(nf, on=shared_col, how='left')
    # This assigns any new values that were brought in to overwrite the old values
    df.loc[df[new_col].notnull(), old_col] = df[new_col]
    df = df.drop(labels=[new_col], axis=1)

# Mark Final MFD
def mark_final_mfd(df):
    df.loc[(df['Algorithmic MFD'].notnull())|
           (df['Manual MFD'].notnull())|
           (df['Vendor MFD'].notnull()),'Final MFD'] = 'Exclude'

    print("Total Exclusions: " + str(len(df[df['Final MFD'].notnull()])))

    return df

# Fuzzy String Matching
# Best practice is to pass a lookup frame with the relevant columns you are matching for
def fuzzy_search(df,lookup_frame,query_field):
    from fuzzywuzzy import fuzz
    from fuzzywuzzy import process

    matches = pd.DataFrame(columns=[query_field,'Match Name','Similarity Score'])

    unique_names_to_match=df[query_field].unique()
    unique_options = lookup_frame[query_field].unique()

    from tqdm import tqdm
    from time import sleep # To properly update tqdm instead of creating new lines

    for i in tqdm(range(len(unique_names_to_match))):
        # For tqdm
        sleep(0.01)

        ratio_tuple = process.extractOne(unique_names_to_match[i],unique_options)
        match_name = ratio_tuple[0]
        similarity_score = int(ratio_tuple[1])

        # Creating new row in dataframe
        matches.loc[len(matches)] = [unique_names_to_match[i],match_name,similarity_score]

    # Bring in the ethnicities column
    temp = lookup_frame.rename(columns={query_field:'Match Name'})
    matches = matches.merge(temp,on='Match Name',how='left')

    print('fuzzy_results[fuzzy_results[\'Similarity Score\']>=90].drop_duplicates(subset=[\'Supplier_Name_Normalized\',\'Match Name\']).sort_values(by=\'Similarity Score\',ascending=False)[[\'Supplier_Name_Normalized\',\'Match Name\',\'Similarity Score\']].drop([])')

    return matches

# Fuzzy String Matching
# Best practice is to pass a lookup frame with the relevant columns you are matching for
def fuzzy_search_smoothing(df,lookup_frame,query_field):
    from fuzzywuzzy import fuzz
    from fuzzywuzzy import process

    matches = pd.DataFrame(columns=[query_field,'Match Name','Similarity Score'])

    unique_names_to_match=df[query_field].unique()
    unique_options = lookup_frame[query_field].unique()

    from tqdm import tqdm
    from time import sleep # To properly update tqdm instead of creating new lines

    for i in tqdm(range(len(unique_names_to_match))):
        # For tqdm
        sleep(0.01)

        # Function returns a tuple of tuples containing the match and the similarity score
        ratio_tuple = process.extract(unique_names_to_match[i],unique_options,limit=2)
        #print(ratio_tuple)
        #print(len(ratio_tuple))

        # Because the returned number of tuples is more than one, a loop is required
        for index in range(len(ratio_tuple)):
            this_tuple = ratio_tuple[index]
            match_name = this_tuple[0]
            similarity_score = int(this_tuple[1])

            # Creating new row in dataframe
            matches.loc[len(matches)] = [unique_names_to_match[i],match_name,similarity_score]

    # Bring in the ethnicities column
    temp = lookup_frame.rename(columns={query_field:'Match Name'})
    matches = matches.merge(temp,on='Match Name',how='left')

    print('fuzzy_results[fuzzy_results[\'Similarity Score\']>=90].drop_duplicates(subset=[\'Supplier_Name_Normalized\',\'Match Name\']).sort_values(by=\'Similarity Score\',ascending=False)[[\'Supplier_Name_Normalized\',\'Match Name\',\'Similarity Score\']].drop([])')

    return matches

# Format Phone Numbers
def phone_format(n):
    if not n[0].isdigit():
        return n
    else:
        return format(int(n[:-1]), ",").replace(",", "-") + n[-1]


# Pivot Table
def pivot_sum(df, index_col, values_col):
    pd.set_option('display.float_format', lambda x: '%.2f' % x)
    return pd.DataFrame(pd.pivot_table(df, index=index_col, values=values_col,
                                       aggfunc=np.sum).to_records()).sort_values(by=values_col, ascending=False)


def add_to_existing_column(df,new_data_col,old_data_col):
    '''
    Pass the new column and old column, will transform
    the data frame so old data is preserved and the combined
    data is unique. Returns passed dataframe
    '''
    JOINED_COLUMN_NAME = 'Joined ' + old_data_col
    NUMBER_OF_VALUES = len(df[(df[old_data_col].notnull())&(df[new_data_col].isnull())])
    NUMBER_OF_NEW_VALUES = len(df[(df[new_data_col].notnull())&(df[old_data_col].isnull())])
    NUMBER_OF_NEW_VALUES = NUMBER_OF_NEW_VALUES + len(df[(df[old_data_col].notnull())&(df[new_data_col].notnull())])
    print("NUMBER_OF_VALUES %s" % NUMBER_OF_VALUES)
    print("NUMBER_OF_NEW_VALUES: %s" % NUMBER_OF_NEW_VALUES)

    # If something in field, combine new and old data separated by semicolon
    df.loc[(df[old_data_col].notnull())&(df[new_data_col].notnull()),JOINED_COLUMN_NAME] =  df[old_data_col].astype(str) + ';' + df[new_data_col].astype(str)
    # If nothing in field already, simply add new data
    df.loc[(df[old_data_col].isnull())&(df[new_data_col].notnull()),JOINED_COLUMN_NAME] = df[new_data_col].astype(str)
    # If nothing in new field, simply preserve old data
    df.loc[(df[old_data_col].notnull())&(df[new_data_col].isnull()),JOINED_COLUMN_NAME] = df[old_data_col].astype(str)

    NUMBER_OF_VALUES_AFTER_CAT = len(df[df[JOINED_COLUMN_NAME].notnull()])

    print("NUMBER_OF_VALUES_AFTER_CAT %s" % NUMBER_OF_VALUES_AFTER_CAT)
    df[JOINED_COLUMN_NAME] = df[JOINED_COLUMN_NAME].apply(get_unique)
    assert NUMBER_OF_VALUES+NUMBER_OF_NEW_VALUES == NUMBER_OF_VALUES_AFTER_CAT
    df[old_data_col] = df[JOINED_COLUMN_NAME]
    df = df.drop([JOINED_COLUMN_NAME],axis=1)
    return df

import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.io import output_notebook, show, output_file
from bokeh.models import ColumnDataSource, HoverTool, Panel
from bokeh.models.widgets import Tabs

# output_notebook()
class BokehHistogram():

    def __init__(self, colors=["SteelBlue", "Tan"], height=600, width=600):
        self.colors = colors
        self.height = height
        self.width = width

    def hist_hover(self, dataframe, column, bins=30, log_scale=False, show_plot=True):
        hist, edges = np.histogram(dataframe[column], bins = bins)
        hist_df = pd.DataFrame({column: hist,
                                 "left": edges[:-1],
                                 "right": edges[1:]})
        hist_df["interval"] = ["%d to %d" % (left, right) for left, 
                               right in zip(hist_df["left"], hist_df["right"])]

        if log_scale == True:
            hist_df["log"] = np.log(hist_df[column])
            src = ColumnDataSource(hist_df)
            plot = figure(plot_height = self.height, plot_width = self.width,
                  title = "Histogram of {}".format(column.capitalize()),
                  x_axis_label = column.capitalize(),
                  y_axis_label = "Log Count")    
            plot.quad(bottom = 0, top = "log",left = "left", 
                right = "right", source = src, fill_color = self.colors[0], 
                line_color = "black", fill_alpha = 0.7,
                hover_fill_alpha = 1.0, hover_fill_color = self.colors[1])
        else:
            src = ColumnDataSource(hist_df)
            plot = figure(plot_height = self.height, plot_width = self.width,
                  title = "Histogram of {}".format(column.capitalize()),
                  x_axis_label = column.capitalize(),
                  y_axis_label = "Count")    
            plot.quad(bottom = 0, top = column,left = "left", 
                right = "right", source = src, fill_color = self.colors[0], 
                line_color = "black", fill_alpha = 0.7,
                hover_fill_alpha = 1.0, hover_fill_color = self.colors[1])

        hover = HoverTool(tooltips = [('Interval', '@interval'),
                                  ('Count', str("@" + column))])
        plot.add_tools(hover)

        if show_plot == True:
            show(plot)
        else:
            return plot

    def histotabs(self, dataframe, features, log_scale=False, show_plot=False):
        hists = []
        for f in features:
            h = self.hist_hover(dataframe, f, log_scale=log_scale, show_plot=show_plot)
            p = Panel(child=h, title=f.capitalize())
            hists.append(p)
        t = Tabs(tabs=hists)
        show(t)

    def filtered_histotabs(self, dataframe, feature, filter_feature, log_scale=False, show_plot=False):
        hists = []
        for col in dataframe[filter_feature].unique():
            sub_df = dataframe[dataframe[filter_feature] == col]
            histo = self.hist_hover(sub_df, feature, log_scale=log_scale, show_plot=show_plot)
            p = Panel(child = histo, title=col)
            hists.append(p)
        t = Tabs(tabs=hists)
        show(t)
