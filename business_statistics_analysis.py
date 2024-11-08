import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pycountry

#----------------------------------------------------------#
#----------------ARABELA CARCELES CARRILLO-----------------#
#-----------------------COPYRIGHT--------------------------#
#----------------------------------------------------------#


#BUSINESS STATISTICS INDIVIDUAL PROJECT
#ANALYSING THE RELATIONSHIP BETWEEN EDUCATION AND ECONOMIC OUTPUT
#Source: World Bank Data
#License Type: CC BY-4.0
#Variables:
#   -Primary completion rate, total (% of relevant age group)
#	-Lower secondary completion rate, total (% of relevant age group)
#	-Children out of school (% of primary school age)
#	-Adolescents out of school (% of lower secondary school age)
#	-GDP per capita (current US$)
#REMINDER: it may be necessary to make changes on the file path
#Used ChatGPT to solve some code related problems


#----------------------------------------------------------#
#----------------------------------------------------------#
#----------------------------------------------------------#


#File load
data_df = pd.read_excel("data.xlsx")

#Null values on World Bank datasets, are represented as ".."
#I needed to change them in order to them delete them
data_df.replace("..", pd.NA, inplace=True)

#One dataframe for each country, we delete the dataframes that do not correspond to countries
#Remove unnecessary columns 
columns_to_remove = ["Series Code", "Country Name", "Country Code"]
dataframes_by_country = {
    country: df.dropna(axis=1)  # Deelete columns with Null Values
                 .drop(columns=columns_to_remove, errors='ignore')  #Delete unnecessary columns
    for country, df in data_df.groupby('Country Name') 
    #In the original dataset, some rows were not valid countries
    if pd.notna(country) and not isinstance(pycountry.countries.get(name=country), type(None))
}

#Years we want to study
#In most dataset, information related to 2022 and 2023 does not exist
#Te selected range allows to have 21 rows of relevant and "recent" data
required_years = set(range(2000, 2022))  # 2022 is exclusive, so it stops at 2021

# Filter dataframes that contain all years from 2000 to 2021
dataframes_by_country_20 = {
    country: df.loc[:, [col for col in df.columns if (col[:4].isdigit() and int(col.split(" ")[0]) in required_years) or col == 'Series Name']]
    for country, df in dataframes_by_country.items()
    if required_years.issubset(
        # Check if all required years are present in the column names
        {int(col.split(" ")[0]) for col in df.columns if col[:4].isdigit()}
    )
}

#To do the SLR, years need to be rows, and the variables for each country have to be columns
final_df = {country: df.T for country, df in dataframes_by_country_20.items()}
for country, df in final_df.items():
    # Set the first row as column names
    df.columns = df.iloc[0]
    # Remove the first row and reset the index
    final_df[country] = df[1:]


# Save the dataset
output_file_path = 'Country_Data.xlsx'
with pd.ExcelWriter(output_file_path) as writer:
    for country, df in final_df.items():
        df.to_excel(writer, sheet_name=country[:31], index=False)  # Limitar el nombre a 31 caracteres (límite de Excel)


    