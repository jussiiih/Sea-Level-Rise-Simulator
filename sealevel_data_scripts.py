import os
import pandas as pd
import glob


CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
data_dir = CURR_DIR_PATH + "/data/"


def transform_hourly_avgs(dataframes):
   '''Transform the hourly data into a daily average'''
   dataframes.set_index(['Year', 'Month', 'Day'], inplace=True)
   df_daily_avg = dataframes.groupby(level=['Year', 'Month', 'Day'])[dataframes.columns[-1]].mean()
   dataframes[dataframes.columns[-1]] = df_daily_avg
   dataframes.drop(dataframes.columns[-2], axis=1, inplace=True)
   dataframes.reset_index(inplace=True)  # reset index to access 'Year', 'Month', and 'Day' as columns
   dataframes.drop_duplicates(subset=['Year', 'Month', 'Day'], inplace=True)

def clean_columns(df):
    '''Creates a date column from Year, Month and Day columns. Renames the se level data column.'''
    # Creating date column
    df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
    df.drop(columns=['Year', 'Month', 'Day'], inplace=True)
    # Renaming
    df.rename(columns={'Theoretical mean water [mm]': 'Sea level [mm]', 'Observation station': 'Location'}, inplace=True)

def frame_to_csv(df, name):
    '''Creates a new csv file'''
    filepath = 'data/' + name + '.csv'
    df.to_csv(filepath, index=False)

def combine_csv_files():
    '''Combines the Helsinki sea-level files to one dataframe and csv-file'''
    dfs = []
    files = glob.glob(os.path.join(data_dir, 'Helsinki Kaivopuisto*'))
    for file in files:
        df = pd.read_csv(file)
        dfs.append(df)
    sealevel_df = pd.concat(dfs, ignore_index=True)
    # Count daily averages
    transform_hourly_avgs(sealevel_df)
    # Transform/clean columns
    clean_columns(sealevel_df)
    # Save as csv
    frame_to_csv(sealevel_df, 'Helsinki-sea-level')
 
def transform_global_data():
    '''Transforms and cleans the global data file'''
    filepath = data_dir + 'sea-level.csv'
    df = pd.read_csv(filepath)
    df.rename(columns={'Global sea level as an average of Church and White (2011) and UHSLC data': 'Sea level [mm]', 'Entity': 'Location', 'Day': 'Date'}, inplace=True)
    df.drop(columns=['Code', 'Global sea level according to Church and White (2011)', 'Global sea level according to UHSLC',], inplace=True)
    frame_to_csv(df, 'Global-sea-level')

# Call the functions
combine_csv_files()
transform_global_data()
