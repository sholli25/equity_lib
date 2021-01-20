# Data Analyst Lessons

## Project Structure

- Consistent project structure is imperative. This means that anyone, regardless of what project they are coming from, should be able to navigate through a project structure and find things with ease. They still may need to consult a README but if a team uses the same structure consistently, any decisions to deviate will be self-explaining.
- Cookie cutter is a low level software that is meant to solve this problem. It is not necessary for you to use this software as there is a learning curve to working with the command line, but reading the documentation of how the software works and why the design choices were made is invaluable: https://drivendata.github.io/cookiecutter-data-science/

## Non-Data Tasks

1. Create a Data Inventory
2. Log use cases for files, a matrix can be helpful for high level view of what is contained in a file. More use for project managers to understand limits of a file.
3. Conclude Data Collection and provide evidence that all data has been collected

## Cleaning

### Sequence of Cleaning

1. Clean files individually. During the process of cleaning a file, you should create a numerical index, a source name, and a MFD column. Any invalid data. Duplicates should be excluded and placed in another tab for traceability sake. When you exclude a duplicate, the columns for exclusion should be labeled in the MFD column.
2. Concatenate all cleaned files composing a Master file. The Master file has a wider scope since there can be duplicates within the joined files. You can use this to spread unique data on a shared key. If a shared key does not exist (such as smoothed name) it must be created first.
   1. Note that cleaning should not be done at the mastering level. There may be quirks that exist within a single file that are best resolved in that file. This point may not make sense at first because it seems inefficient but it actually gives you stronger confidence in the Master file. Confidence makes you faster.

### Loading Data

- When loading data outside of a formal database, you must be cautious of changing the data type while loading. For example, Zip Codes and NIGP codes need to be loaded as strings, otherwise you may not preserve the integrity of the original data.
- It is important for this to happen on load so that you don't need to patch the data. Still though, this may be required because an exported file or even a poorly designed database may not maintain the integrity of the data

### Assertions

- Assertion statements allow you to make logical assertions about anything as a mathematical check of your logic. For example, filtering a data set on a boolean condition (Exclude vs Don't Exclude). It is important that you check to see that filtering is working and you haven't lost rows in the process. This becomes more important when you are filtering by more complex conditions, like work category or ethnicity.
- Never assume anything is working. As soon as you catch yourself making an assumption, write an assertion statement to give you peace of mind and confidence with what you are doing.
- More on assertions: https://www.programiz.com/python-programming/assert-statement

### Regular Expressions

- Regular Expressions are narrowly defined syntax expressions which define a pattern. For example, a valid email matches a certain pattern. Anything that doesn't match that pattern is not a valid email
- When cleaning data there are certain fields which need to be cleaned before they can be used for things like surveys, outreach, determining relevant market region, and in general understanding the quality of the data you received

## Version Control

- Unavoidable step in developing software in a collaboration, but it is even useful for one person just to reduce cognitive load in changes
- Git is the most commonly used version control system
- A lot to say on this topic but better to go straight to the Git/GitHub documentation

## Useful Resources

- Tidy Data by Hadley Wickham (the creator of R): https://vita.had.co.nz/papers/tidy-data.pdf
- Deep Learning based Text Classification: A Comprehensive Review: https://arxiv.org/abs/2004.03705
- Kedro (reproducible research framework): https://github.com/quantumblacklabs/kedro
- Using Machine Learning to assign NAICS: https://www.census.gov/content/dam/Census/newsroom/press-kits/2019/jsm/Using%20Machine%20Learning%20to%20Assign%20North%20American%20Industry%20Classification%20System%20Codes%20to%20Establishments_Dumbacher.pdf