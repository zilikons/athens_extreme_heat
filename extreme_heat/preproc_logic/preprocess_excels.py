import pandas as pd
import geopandas as gpd
import os
import re
from extreme_heat.main_interface.params import *

def rename_excel_columns(filepath: str) -> pd.DataFrame:
    '''
    This function takes the excel filepath and renames the columns, depending on the file name
    '''
    print(filepath)
    df = pd.read_excel(filepath)
    # Regex to get the file name
    file_name = re.search(r'\/(\w+).xls',filepath).group(1)
    if file_name == '1_2011_1991_Deprivation':
        df.columns = ['code','description','deprivation','asd']
        df = df.drop(columns='asd')
        df['desc'] = 0
        df['total'] = 0
    if file_name == '2_2011_Age':
        df.columns = ['code','desc','description','to_14','to_24','to_34','to_44','to_54','to_64','to_74',
                      'from_75','total']
    if file_name == '3_2011_Kyria_Pigi_Poron':
        df.columns = ['code','desc','description','work','investments','retirement','subsidies','loans_saving','dependant','other_income','total']
    if file_name == '4_2011_Enoikisi':
        df.columns = ['code','desc','description','owner','part_owner','rent','other_housing_situation','communal_housing','total']
    if file_name == '5_2011_sqr_m':
        df.columns = ['code','desc','description','to_30','to_50','to_70','to_90','to_120','to_150','to_200','to_300','from_300','communal_or_other','total']
    if file_name == '6_2011_Construction':
        df.columns = ['code','desc','description','before_1919','from_1919_to_1945','from_1946_to_1960','from_1961_to_1970','from_1971_to_1980','from_1981_to_1990','from_1991_to_2000','from_2001_to_2005','after_2005','non_normal','communal_or_other_situation','total']
    if file_name == '8_2011_Unemployment':
        df.columns = ['code','desc','description','employed','looking_for_work','first_time_looking','student','retired','independent','housework','other_employ','total']
    if file_name == '9_2011_Nationality':
        df.columns = ['code','desc','description','greek','greek_and_other','developed_eu','developed_east_eu','developed_non_eu','developing_east_eu','developing_na_me','other_non_eu','no_nation','no_answer','total']
    if file_name == 'AthensSocialAtlas_HouseHoldTypesData':
        df.columns = ['code','desc','description','hh_type_1','hh_type_2','hh_type_3','hh_type_4','hh_type_5','hh_type_6','hh_type_7','hh_type_8']
        df['desc'] = 0
        df['total'] = 0
    return df

def merge_dataframes(list_of_dataframes: list) -> pd.DataFrame:
    '''
    This function takes a list of dataframes and merges them into one
    '''
    df = list_of_dataframes[-1]
    for i in range(0,len(list_of_dataframes)-1):
        #First drop the columns that are not needed
        list_of_dataframes[i] = list_of_dataframes[i].drop(columns = ['desc','description','total'])
        df = df.merge(list_of_dataframes[i],on='code',how='inner')
    return df

def create_list_of_filepaths(filepath_directory:str) -> list:
    '''
    This function takes the filepath of the directory and creates a list of filepaths
    '''
    # Get the list of files in the directory
    list_of_filepaths = [f for f in os.listdir(filepath_directory) if os.path.isfile(os.path.join(filepath_directory, f))]
    # Delete the .DS_Store file
    list_of_filepaths.remove('.DS_Store')
    # Delete the 7th file
    list_of_filepaths.remove('7_2011_15Types.xls')
    return list_of_filepaths

def prepare_shapefile(filepath:str) -> gpd.GeoDataFrame:
    shape = gpd.read_file(filepath)
    shape = shape.drop(2999)
    shape = shape[['MOXAP','geometry']]
    shape.columns = ['code','geometry']
    shape['code'] = shape['code'].astype('int32')
    return shape

def feature_engineering(data:gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    data['House_before_1980'] = data['before_1919'] + data['from_1919_to_1945'] + data['from_1946_to_1960'] + data['from_1961_to_1970'] + data['from_1971_to_1980']
    data = data.drop(columns = ['before_1919','from_1919_to_1945','from_1946_to_1960','from_1961_to_1970','from_1971_to_1980'])
    data['Houses_after_1980'] = data['from_1981_to_1990'] + data['from_1991_to_2000'] + data['from_2001_to_2005'] + data['after_2005']
    data['Houses_communal_or_other'] = data['communal_or_other_situation'] + data['non_normal']
    data = data.drop(columns = ['from_1981_to_1990','from_1991_to_2000','from_2001_to_2005','after_2005','communal_or_other_situation','non_normal'])
    data['Elderly'] = data['to_74'] + data['from_75']
    data = data.drop(columns = ['to_74','from_75'])
    data['Young'] = data['to_14'] + data['to_24']
    data = data.drop(columns=['to_14','to_24'])
    data['Adult'] = data['to_34'] + data['to_44'] + data['to_54'] + data['to_64']
    data = data.drop(columns=['to_34','to_44','to_54','to_64'])
    data['Developed_imm'] = data['developed_east_eu']+data['developed_eu'] + data['developed_non_eu']
    data = data.drop(columns = ['developed_east_eu','developed_eu','developed_non_eu'])
    data['Greek'] = data['greek'] + data['greek_and_other']
    data = data.drop(columns = ['greek_and_other','greek'])
    data['Developing_imm'] = data['developing_east_eu'] + data['developing_na_me'] + data['other_non_eu'] + data['no_nation'] + data['no_answer']
    data = data.drop(columns=['developing_east_eu','developing_na_me','other_non_eu','no_nation','no_answer'])
    data['Small_house'] = data['to_30'] + data['to_50'] + data['to_70']
    data['Large_house'] = data['to_90'] + data['to_120']
    data['Huge_house'] = data['to_150'] + data['to_200'] + data['to_300'] + data['from_300']
    data['Irregular_house'] = data['communal_or_other']
    data = data.drop(columns=['to_30','to_50','to_70','to_90','to_120','to_150','to_200','to_300','from_300','communal_or_other'])
    data['Living_alone'] = data['hh_type_1'] + data['hh_type_2']
    data['Living_with_others'] = data['hh_type_3'] + data['hh_type_4'] + data['hh_type_5'] + data['hh_type_6'] + data['hh_type_7'] + data['hh_type_8']
    data = data.drop(columns=['hh_type_1','hh_type_2','hh_type_3','hh_type_4','hh_type_5','hh_type_6','hh_type_7','hh_type_8'])
    data['Unemployed'] = data['looking_for_work'] + data['first_time_looking'] + data['other_employ']
    data['Employed_or_studying'] = data['employed'] + data['student'] + data['housework']
    data['Retired'] = data['retired']
    data['Rich'] = data['independent']
    data = data.drop(columns=['looking_for_work','first_time_looking','other_employ','employed','student','housework','retired','independent'])
    data['Social_deprivation'] = data['deprivation']
    data = data.drop(columns=['deprivation'])
    data['Irregular_or_no_income'] = data['subsidies'] + data['loans_saving'] + data['other_income']
    data['Income_from_retirement'] = data['retirement']
    data['Income_from_work_or_dependant'] = data['work'] + data['dependant']
    data['Income_from_investments'] = data['investments']
    data = data.drop(columns=['subsidies','loans_saving','other_income','retirement','work','dependant','investments'])
    data['House_owner'] = data['owner'] + data['part_owner']
    data['Renting'] = data['rent']
    data['Housing_irregular'] = data['communal_housing'] + data['other_housing_situation']
    data = data.drop(columns=['owner','part_owner','rent','communal_housing','other_housing_situation'])
    return data

def preprocess_excel_data(filepath_directory:str,shapefilepath:str) -> pd.DataFrame:
    '''
    This function takes the filepath of the directory and creates a list of filepaths
    '''
    # Get the list of filepaths
    list_of_filepaths = create_list_of_filepaths(filepath_directory)
    # Create a list of dataframes
    list_of_dataframes = []
    for file in list_of_filepaths:
        # Create the filepath
        filepath = filepath_directory + '/' + file
        # Rename the columns
        df = rename_excel_columns(filepath)
        # Append the dataframe to the list
        list_of_dataframes.append(df)
    # Merge the dataframes
    df = merge_dataframes(list_of_dataframes)
    gdf = prepare_shapefile(shapefilepath)
    gdf = gdf.merge(df,on='code',how='inner')
    gdf = feature_engineering(gdf)
    return gdf

if __name__ == '__main__':
    gdf = preprocess_excel_data(LOCAL_RAW_DATA_DIR, LOCAL_RAW_DATA_DIR + '/MOXAP/Moxap_tx132.shp')
    gdf.to_file(LOCAL_DATA_DIR + '/census_data.json', driver='GeoJSON')
