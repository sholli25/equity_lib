# Reasons to exclude
- Duplicate
- Invalid Award Amount
- Less than 1000
- No Vendor
- Null Award Amount
- Exclusion Category
- Award Status


# Disable Autosave

```{python}
# %autosave 0
```

# Python Index based loops

```{python jupyter={'outputs_hidden': True}}
fruits = ['banana', 'apple',  'mango']

for index in range(len(fruits)):
    print('Current fruit :', fruits[index])
```


# Import multiple files directory

```{python jupyter={'outputs_hidden': True}}
#https://stackoverflow.com/questions/20906474/import-multiple-csv-files-into-pandas-and-concatenate-into-one-dataframe

import pandas as pd
import glob

path = r'C:\Users\Griffin Strong\OneDrive\Omar\My Notebooks\NCDOT\data\190416\FY 2014 Disparity Study Files\Invoice Data\Invoice 1' # use your path
all_files = glob.glob(path + "/*.xlsx")

li = []

for filename in all_files:
    df = pd.read_excel(filename, index_col=None, header=0)
    li.append(df)

invoice_1 = pd.concat(li, axis=0, ignore_index=True)
```


# Remove Scientific, Globally setting the float length

```{python jupyter={'outputs_hidden': True}}
pd.options.display.float_format = '{:.5f}'.format
```
