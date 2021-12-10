import pandas as pd
import geopandas as gpd

# Uncomment to display entire dataframe for troubleshooting purposes
# pd.set_option("display.max_rows", None, "display.max_columns", None)


fifty_states_only = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA",
                     "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                     "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT",
                     "VA", "WA", "WV", "WI", "WY", 'Total']

abbrev_to_state_dict = {'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AZ': 'Arizona', 'CA': 'California',
                        'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida',
                        'GA': 'Georgia', 'HI': 'Hawaii', 'IA': 'Iowa', 'ID': 'Idaho', 'IL': 'Illinois',
                        'IN': 'Indiana', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana',
                        'MA': 'Massachusetts', 'MD': 'Maryland', 'ME': 'Maine', 'MI': 'Michigan',
                        'MN': 'Minnesota', 'MO': 'Missouri', 'MS': 'Mississippi', 'MT': 'Montana',
                        'NC': 'North Carolina', 'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire',
                        'NJ': 'New Jersey', 'NM': 'New Mexico', 'NV': 'Nevada', 'NY': 'New York', 'OH': 'Ohio',
                        'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island',
                        'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas',
                        'UT': 'Utah', 'VA': 'Virginia', 'VI': 'Virgin Islands', 'VT': 'Vermont',
                        'WA': 'Washington', 'WI': 'Wisconsin', 'WV': 'West Virginia', 'WY': 'Wyoming', 'Total': 'Total'}

state_to_abbrev_dict = {"Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
                        "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL",
                        "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN",
                        "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME",
                        "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
                        "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE",
                        "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
                        "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
                        "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI",
                        "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX",
                        "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
                        "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY", "Total": "Total"}


class HomesslessPrepWork(object):

    def __init__(self):
        self.create_df_2010_to_2020()
        self.create_df_2017_to_2020_demo()
        self.create_heat_map()

    def import_sheet(self, sheet_name):
        df = pd.read_excel('data/2007-2020-PIT-Estimates-by-state.xlsx', sheet_name=sheet_name)
        cols = df.columns
        new_col_names = []

        for col in cols:
            try:
                col_name = col.split(',')[0]
            except:
                col_name = col
            new_col_names.append(col_name)

        for col in new_col_names:
            col = col.replace(' ', '_').lower()

        df.columns = new_col_names
        df['Year'] = sheet_name

        return df

    def remove_decimal_from_years(self, col):
        if isinstance(col, float):
            return str(int(col))
        else:
            return col

    def create_df_2010_to_2020(self):
        years_range = range(2010, 2021)
        sheet_names = [str(x) for x in years_range]
        dfs = []
        for sheet in sheet_names:
            dfs.append(self.import_sheet(sheet))

        template_sheet = dfs[0]
        cols_to_keep = template_sheet.columns
        slimmed_dfs = []

        for df in dfs:
            df = df[cols_to_keep]
            select_condition = df['State'].isin(fifty_states_only)
            df = df[select_condition]
            slimmed_dfs.append(df)

        master_df_national = pd.DataFrame()

        for df in slimmed_dfs:
            master_df_national = master_df_national.append(df)

        master_df_national.set_index('State', inplace=True)
        master_df_national.to_csv('data/master_df_national.csv')

        df_national_total_pop = pd.read_excel('data/state_populations.xlsx')
        df_national_total_pop.rename(columns={'Geographic Area': 'Full_State'}, inplace=True)
        df_national_total_pop.set_index('Full_State', inplace=True)

        row_dict = {}
        for index, row in df_national_total_pop.iterrows():
            row_dict[index] = str(index).replace('.', '')

        df_national_total_pop.rename(row_dict, axis='index', inplace=True)

        df_national_total_pop.insert(0, 'State', df_national_total_pop.index.map(state_to_abbrev_dict), True)

        select_condition = df_national_total_pop['State'].isin(fifty_states_only)
        df_national_total_pop = df_national_total_pop[select_condition]

        df_national_total_pop.rename(mapper=self.remove_decimal_from_years, axis=1, inplace=True)

        try:
            df_national_total_pop.drop(columns=['Census (4/1/2010)', 'Estimates Base (4/1/2010)'], inplace=True)
        except:
            print("already dropped")

        # Making range of years
        range_of_years = range(2010, 2021)

        df_national_total_pop_reformatted = pd.DataFrame(columns=['State', 'Full_State', 'Year', 'Total_Population'])

        for year in range_of_years:
            temp_df = df_national_total_pop.loc[:, ['State', year]]
            temp_df['Full_State'] = df_national_total_pop.index
            temp_df['Year'] = year
            temp_df['Total_Population'] = df_national_total_pop[year]
            df_national_total_pop_reformatted = df_national_total_pop_reformatted.append(temp_df)

        df_national_total_pop_reformatted = df_national_total_pop_reformatted.loc[:,
                                            ['State', 'Full_State', 'Year', 'Total_Population']]
        df_national_total_pop_reformatted['Year'] = df_national_total_pop_reformatted['Year'].astype(str)
        df_national_total_pop_reformatted['Total_Population'] = df_national_total_pop_reformatted[
            'Total_Population'].astype(int)

        df_national_total_pop_reformatted.rename(columns={'Overall Homeless': 'Overall_Homeless'}, inplace=True)
        master_df_national.rename(columns={'Overall Homeless': 'Overall_Homeless'}, inplace=True)

        merged_df = pd.merge(master_df_national, df_national_total_pop_reformatted, on=['State', 'Year'])
        relevant_data_qa_table = merged_df.loc[:, ['State', 'Full_State', 'Year', 'Overall_Homeless', 'Total_Population']]
        relevant_data_qa_table["Percent_Homeless"] = relevant_data_qa_table['Overall_Homeless'] / relevant_data_qa_table['Total_Population'] * 100
        relevant_data_qa_table['Percent_Homeless'] = relevant_data_qa_table['Percent_Homeless'].astype(float).round(2)
        relevant_data_qa_table['Overall_Homeless'] = relevant_data_qa_table['Overall_Homeless'].astype(int)
        relevant_data_qa_table['Total_Population'] = relevant_data_qa_table['Total_Population'].astype(int)
        relevant_data_qa_table.set_index('State', inplace=True)
        relevant_data_qa_table.to_csv('data/national_homeless_cleaned_up_data.csv')

    def create_df_2017_to_2020_demo(self):
        years_range = range(2017, 2021)
        sheet_names = [str(x) for x in years_range]
        dfs = []
        for sheet in sheet_names:
            dfs.append(self.import_sheet(sheet))

        template_sheet = dfs[0]
        cols_to_keep = template_sheet.columns
        slimmed_dfs = []

        for df in dfs:
            df = df[cols_to_keep]
            select_condition = df['State'].isin(fifty_states_only)
            df = df[select_condition]
            slimmed_dfs.append(df)

        master_df_national_demo = pd.DataFrame()

        for df in slimmed_dfs:
            master_df_national_demo = master_df_national_demo.append(df)

        select_condition = master_df_national_demo['State'].isin(fifty_states_only)
        master_df_national_demo = master_df_national_demo[select_condition]
        master_df_national_demo.rename(mapper=self.remove_decimal_from_years, axis=1, inplace=True)
        master_df_national_demo.to_csv('data/national_homeless_cleaned_up_data_for_demographics.csv')

    def create_heat_map(self):
        relevant_data_qa_table = pd.read_csv('data/national_homeless_cleaned_up_data.csv',thousands=',')
        relevant_data_qa_table.set_index('State', inplace=True)
        relevant_data_to_merge = relevant_data_qa_table[relevant_data_qa_table.Year == 2020].rename(
            columns={'Full_State': 'NAME'})

        gdf = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
        us = gdf[gdf.iso_a3 == "USA"]
        bounds = us.total_bounds
        national_map = gpd.read_file('data/usmap/s_11au16.shp')
        merged = national_map.merge(relevant_data_to_merge, on="NAME")
        merged.loc[:, "Total_Population"] = merged["Total_Population"].map('{:,d}'.format)
        merged.rename(
            columns={'NAME': 'State', 'Total_Population': 'Total Population', 'Percent_Homeless': 'Percent Homeless'},
            inplace=True)
        heat_map = merged.explore(column="Percent Homeless", cmap="Reds",
                                  tooltip=['State', 'Total Population', 'Percent Homeless'],
                                  location=gdf.loc[gdf["iso_a3"].eq("USA"), "geometry"]
                                  .apply(lambda g: [g.centroid.xy[1][0], g.centroid.xy[0][0]])
                                  .values[0],
                                  zoom_start=3, min_zoom=3,
                                  control_scale=True, width=1000, min_lat=bounds[1],
                                  min_lon=bounds[0],
                                  max_lat=bounds[3],
                                  max_lon=bounds[2],
                                  max_bounds=True)  # tooltip_kwds={'NAME': 'State'})

        heat_map.save('data/heatmap.html')


if __name__ == "__main__":
    HomesslessPrepWork()
