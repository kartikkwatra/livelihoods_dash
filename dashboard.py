import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_authenticator as stauth



import yaml
from yaml.loader import SafeLoader

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

authenticator.login()

def protected_page():

    # functions to transform data
    def transform_data(data, id_vars, var_name):
        df = pd.DataFrame(data)
        df_long = df.melt(id_vars=id_vars, var_name=var_name, value_name='Value')
        transposed_df = df_long.pivot(index=var_name, columns=id_vars, values='Value')
        return transposed_df

    # data
    admin_profile = {
        'District': 'Anantpur',
        'Total Geographical Area (Sq.km)': 1000,
        'Agro-climatic Zone': 'Zone A',
        'No. of Sub Divisions': 3,
        'No. of Blocks': 10,
        'No. of Villages (Inhabited)': 200,
        'No. of Panchayats': 50
    }

    admin_df = transform_data([admin_profile], id_vars='District', var_name='Basic Profile')

    ## landholding
    landholding = {
        '% of land holding <= 1 Ha': 30,
        '% of land holding >1 to <=2 Ha': 40,
        '% of land holding >2 Ha': 30
    }
    landholding_df = pd.DataFrame(landholding.items(), columns=['Category', 'Value'] )

    ## households
    # households
    households = {
        'Brick/Stone/Concrete Houses': 80,
        'Electricity Supply': 90,
        'Source of Drinking Water': 95,
        'Independent Toilets': 70,
        'Access to Banking Services': 60,
        'Radio/TV Sets': 75
    }
    households_df = pd.DataFrame(households.items(), columns=['Households', 'No. of Households'])

    ## village profile
    village_profile = {
        'Villages Electrified': 150,
        'Villages having Agriculture Power Supply': 120,
        'Villages having Post Offices': 80,
        'Villages having Banking Facilities': 100,
        'Villages having Primary Schools': 90,
        'Villages having Primary Health Centres': 70,
        'Villages having Potable Water Supply': 110,
        'Villages connected with Paved Approach Roads': 130
    }
    village_profile_df = pd.DataFrame(village_profile.items(), columns=['Village Profile', 'Count'])

    ## Crop production profile
    crop_data = {
        'Crop': ['Paddy', 'Cotton', 'Maize', 'Redgram', 'Bengal Gram', 'Ground Nut', 'Fresh fruits'],
    'Area (ha)': [35331, 40669, 27627, 47131, 87490, 53480, 153096],
    'Prod. (MT)': [141145, 13084, 103484, 3390, 36308, 292161, 424081],
    'Yield(Kg/ha)': [143376, 29954, 91480, 21413, 51065, 323890, 424081],
    'Year': ['2020-21', '2020-21', '2020-21', '2020-21', '2020-21', '2020-21', '2020-21'],
    'State_Avg_Yield':  [157714, 32949, 100828, 23554, 56172, 356279, 466489]
    }

    crop_df = pd.DataFrame(crop_data)

    ## Agroprocessing units
    processing_units = {
        'Food (Rice/Flour/Dal/Oil/Tea/Coffee)': {
            'No of units': 5,
            'Capacity.[MT]': 100
        },
        'Sugarcane (Gur/Khandsari/Sugar)': {
            'No of units': 3,
            'Capacity.[MT]': 50
        },
        'Fruit (Pulp/Juice/Fruit drink)': {
            'No of units': 2,
            'Capacity.[MT]': 30
        },
        'Spices (Masala Powders/Pastes)': {
            'No of units': 4,
            'Capacity.[MT]': 80
        },
        'Dry-fruit (Cashew/Almond/Raisins)': {
            'No of units': 2,
            'Capacity.[MT]': 40
        },
        'Cotton (Ginnining/Spinning/Weaving)': {
            'No of units': 3,
            'Capacity.[MT]': 60
        },
        'Milk (Chilling/Cooling/Processing)': {
            'No of units': 2,
            'Capacity.[MT]': 20
        },
        'Meat (Chicken/Mutton/Pork/Dryfish)': {
            'No of units': 4,
            'Capacity.[MT]': 70
        },
        'Animal feed (Cattle/Poultry/Fishmeal)': {
            'No of units': 3,
            'Capacity.[MT]': 50
        }
    }
    processing_units_df = pd.DataFrame(processing_units).T.reset_index().rename(columns={'index': 'Agroprocessing Units'})

    # infrastructure and support services for agriculture
    agri_assets = {
        'Item': ['Agriculture Tractors', 'Power Tillers', 'Threshers/Cutters', 'Pumpsets Energised', 'Agriculture Pumpsets'],
        'Value': [28338, 561, 3894, 159000, 225000]
    }
    agri_assets_df = pd.DataFrame(agri_assets)

    # agri inputs
    agri_inputs = {
        'Item': ['Fertiliser/Feed/Pesticide Outlets', 'Total N/P/K Consumption [MT]', 'Certified Seeds Supplied [MT]', 'Pesticides Consumed [MT]'],
        'Value': [1371, 74144, 150025, 79]
    }
    agri_inputs_df = pd.DataFrame(agri_inputs)

    # agri services
    agri_services = {
        'Item': ['Agro Service Centres', 'Soil Testing Centres', 'Plantation Nurseries', 'Farmers\' Clubs', 'Krishi Vigyan Kendras'],
        'Value': [40, 2, 55, 136, 2]
    }
    agri_services_df = pd.DataFrame(agri_services)



    # Create the new data frame
    narega_progress_data = {
        'Progress': ['Approved Labour Budget [In Lakhs]', 'Persondays of Central Liability so far [In Lakhs]', '% of Total LB',
                    '% as per Proportionate LB', 'SC persondays % as of total persondays', 'ST persondays % as of total persondays',
                    'Women Persondays out of Total (%)', 'Average days of employment provided per Household',
                    'Average Wage rate per day per person(Rs.)', 'Total No of HHs completed 100 Days of Wage Employment',
                    'Total Households Worked [In Lakhs]', 'Total Individuals Worked [In Lakhs]', 'Differently abled persons worked'],
        'FY 2020-2021': [280.71, 279.93, 99.73, None, 18.69, 4.97, 53.59, 66.3, 231.41, 77, 4.22, 7.65, 10068],
        'FY 2021-2022': [256.99, 255.34, 99.36, None, 18.22, 4.96, 54.08, 62.71, 225.37, 770, 4.07, 7.26, 9494],
        'FY 2022-2023': [104.52, 108.31, 103.62, None, 19.3, 3.86, 56.19, 53.84, 214.79, 6, 2.01, 3.63, 4314],
        'FY 2023-2024': [109, 109.04, 100.04, None, 18.38, 3.93, 56.16, 54.75, 239.75, 34672, 1.99, 3.42, 4080],
        'FY 2024-2025': [90, 21.4, 23.78, 63.93, 17.18, 4.38, 56.11, 17.59, 259.61, 2, 1.22, 1.97, 2441],
    }

    narega_progress_df = pd.DataFrame(narega_progress_data)

    #naraga fin progress data
    fin_progress_data = {
        'Fin_Progress': ['Total Exp(Rs. in Lakhs.)', 'Wages(Rs. In Lakhs)', 'Material and skilled Wages(Rs. In Lakhs)',
                        'Material(%)', 'Total Adm Expenditure (Rs. in Lakhs.)', 'Admin Exp(%)',
                        'Average Cost Per Day Per Person(In Rs.)', '% of Total Expenditure through EFMS',
                        '% payments gererated within 15 days'],
        'FY 2020-2021': [102267.02, 65062.42, 33959.09, 34.29, 3245.52, 3.17, 333.67, 100, 99.08],
        'FY 2021-2022': [81710.69, 57607.32, 21789.05, 27.44, 2314.32, 2.83, 303.2, 100, 99.17],
        'FY 2022-2023': [46955.55, 23319.7, 20668.06, 46.99, 2967.79, 6.32, 329.22, 100, 99.53],
        'FY 2023-2024': [41452.98, 26142.94, 13388.08, 33.87, 1921.96, 4.64, 312.6, 100, 100],
        'FY 2024-2025': [9662.56, 4899.12, 4335.29, 46.95, 428.14, 4.43, 294.67, 100, 100]
    }
    fin_progress_df = pd.DataFrame(fin_progress_data)


    # narega work demand
    data = {
        'District': ['Anantpur'],
        'April Household': [133749],
        'April Persons': [232179],
        'May Household': [160007],
        'May Persons': [282184],
        'June Household': [149174],
        'June Persons': [255144],
        'July Household': [108265],
        'July Persons': [172532],
        'August Household': [38672],
        'August Persons': [56983],
        'September Household': [16166],
        'September Persons': [24715],
        'October Household': [13385],
        'October Persons': [20520],
        'November Household': [61255],
        'November Persons': [91294],
        'December Household': [48706],
        'December Persons': [74043],
        'January Household': [41792],
        'January Persons': [63419],
        'February Household': [46517],
        'February Persons': [70060],
        'March Household': [68265],
        'March Persons': [107322]
    }

    df = pd.DataFrame(data)

    # Melt the DataFrame to get the required format
    melted_df = pd.melt(df, id_vars=['District'], value_vars=[col for col in df.columns if col.endswith(('Household', 'Persons'))], var_name='Month_Type', value_name='Value')

    # Split the 'Month_Type' column into 'Month' and 'Type' columns
    melted_df[['Month', 'Type']] = melted_df['Month_Type'].str.split(' ', expand=True)

    # Reorder and rename columns
    narega_demand_df = melted_df[['District', 'Month', 'Type', 'Value']]


    ## Financing
    # Create the dataframe
    targets_achievements_data = {
        'Year': ['2020-2021', '2021-2022', '2022-2023'],
        'Crop Loan Target': [1000000, 1200000, 1500000],
        'Crop Loan Achievement': [900000, 1100000, 1400000],
        'Term Loan Target': [2000000, 2200000, 2500000],
        'Term Loan Achievement': [1800000, 2100000, 2400000],
        'Total Agri Credit Target': [3000000, 3400000, 4000000],
        'Total Agri Credit Achievement': [2700000, 3300000, 3900000],
        'Non-Farm Sector Target': [500000, 550000, 600000],
        'Non-Farm Sector Achievement': [450000, 520000, 590000],
        'Other Priority Sector Target': [800000, 900000, 1000000],
        'Other Priority Sector Achievement': [750000, 880000, 990000],
        'Total Priority Sector Target': [3800000, 4200000, 4700000],
        'Total Priority Sector Achievement': [3450000, 4180000, 4790000]
    }

    targets_achievements_df = pd.DataFrame(targets_achievements_data)

    financing_data = {
        'Year': ['FY 2020-2021', 'FY 2021-2022', 'FY 2022-2023'],
        'Priority Sector Loans (Total Amount)': [1000000, 1200000, 1500000],
        'Priority Sector Loans (% of Total Loans)': [80, 85, 90],
        'Loans to Agriculture Sector (Total Amount)': [800000, 900000, 1000000],
        'Loans to Agriculture Sector (% of Total Loans)': [60, 65, 70],
        'Loans to Weaker Sections': [500000, 550000, 600000],
        'Loans under DRI Scheme': [200000, 220000, 250000],
        'Loans to Women': [300000, 330000, 360000]
    } 

    financing_df = pd.DataFrame(financing_data)

    granular_credit_data = {
        'Year': ['2018-19', '2019-20', '2020-21'],
        'Crop production': [702337.33, 887536.00, 889163.44],
        'Minor Irrigation': [1467.96, 1740.57, 1930.79],
        'Farm Mechanisation': [595.47, 1655.52, 4111.70],
        'Plantation &Horticulture (inclg Sericulture)': [400.00, 734.10, 3411.11],
        'Forestry & Wasteland Development': [0.00, 20.76, 54.01],
        'AH - Dairy Development': [22611.73, 33825.51, 41739.50],
        'AH - Poultry Development': [1665.28, 2282.10, 1418.60],
        'AH - Sheep, Goat & Piggery': [13407.46, 6857.33, 8809.86],
        'Fisheries': [24.00, 13.77, 62.81],
        'Agri-Infrastructure': [None, None, None],
        'Storage Godowns & Marketing Infrastructure': [2720.00, 322.00, 490.00],
        'Land Development': [2938.96, 242.00, 2518.77],
        'Agri-Infra others': [0, 0.00, 0.00],
        'Ancillary Activities': [None, None, None],
        'Food & Agro-Processing': [1594.00, 2589.53, 709.07],
        'Others': [585.00, 2364.00, 237.17]
    }

    granular_credit_df = pd.DataFrame(granular_credit_data)
    # granular_credit_df = df.melt(id_vars='Year', var_name='Sector', value_name='Value')
    # granular_credit_df = granular_credit_df.pivot(index='Year', columns='Sector', values='Value').reset_index()

    # Allied Infra
    allied_infra = {
        'Item': ['Veterinary Hospitals/Dispensaries', 'Disease Diagnostic Centers', 'Artificial Insemination Centers',
                'Animal Breeding Farms', 'Animal Husbandry Training Centers', 'Dairy Cooperative Societies',
                'Improved Fodder Farms', 'Animal Markets', 'Milk Collection Centres', 'Fishermen Societies',
                'Fish seed farms', 'Fish Markets', 'Poultry hatcheries', 'Slaughter houses'],
        'Value': [153, 2, 402, 2, 2, 50, 3, 9, 959, 112, 2, 1, 'Nil', 1]
    }
    allied_infra_df = pd.DataFrame(allied_infra)


    #Allied Production
    allied_prod = {
        'Item': ['Fish', 'Egg', 'Milk', 'Meat'],
        'Production': [191380, 3593, 1023, 101380]
    }
    allied_prod_df = pd.DataFrame(allied_prod)


    # Work patterns
    work_patterns = {
        'Category': ['No of Cultivators', 'Small/Marginal Farmers', 'Agricultural Labourers', 'Workers engaged in Household Industry',
                    'Workers engaged in Allied Agro-activities', 'Other workers'],
        'Value': [500, 200, 300, 100, 150, 250]
    }
    work_patterns_df = pd.DataFrame(work_patterns)

    # Rainfall
    rainfall_data = {
        'Rainfall': [500],
        'Variation from Normal': [50],
        'Availability of Ground Water [Ham]': [100]
    }
    rainfall_df = pd.DataFrame(rainfall_data, index=['Value']).T

    # web app
    # Define CSS styles
    center_css = """
    <style>
    .center-column {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    </style>
    """


    st.header('Rural Livelihoods Dashboard', divider='rainbow')

    district, agri, allied, narega, fin = st.tabs(["District Profile", "Agricultural Profile", "Allied Activities", "NAREGA" , "Financing"])

    with district:
        col1, empty_col, col2 = st.columns([1, 0.1, 1])

        with col1: 
            # admin profile
            st.write(admin_df)

            # households bar chart
            fig = px.bar(households_df, y='Households', x='No. of Households')
            fig.update_layout(width=400, height=400)
            st.plotly_chart(fig)

            st.subheader("Work Patterns")
            st.dataframe(work_patterns_df)

        with col2:
            # landholding pie chart
            fig = px.pie(landholding_df, values='Value', names='Category')
            fig.update_layout(width=400, height=250)
            st.plotly_chart(fig)

            # village bar chart
            fig = px.bar(village_profile_df, y='Village Profile', x='Count')
            fig.update_layout(width=400, height=400)
            st.plotly_chart(fig)

            # Water
            st.subheader("Rainfall")
            st.dataframe(rainfall_df)

    with agri:
        
        with st.container():

            st.subheader("Crop Production Profile")

            col1, empty_col, col2 = st.columns([1, 0.1, 1])
            
            with col1:
            
                # Calculate the percentage area of each crop
                crop_df['% Area'] = crop_df['Area (ha)'] / 910972 * 100

                # Calculate the percentage production of each crop
                crop_df['% Production'] = crop_df['Prod. (MT)'] / crop_df['Prod. (MT)'].sum() * 100

                # crop production grouped bar chart
                fig = px.bar(crop_df, x='Crop', y=['% Area', '% Production'], barmode='group')
                fig.update_layout(width=500, height=400)
                st.plotly_chart(fig)

            with col2:
                # Yields bar chart
                fig = px.bar(crop_df, x='Crop', y=['Yield(Kg/ha)','State_Avg_Yield'], barmode='group')
                fig.update_layout(width=500, height=400)
                st.plotly_chart(fig)

        with st.container():
            # Create a 3-column layout
            col1, col2, col3 = st.columns(3)

            # Add content to each column
            with col1:
                st.subheader("Agri Inputs")
                st.dataframe(agri_inputs_df)

            with col2:
                st.subheader("Agri Assets")
                st.dataframe(agri_assets_df)

            with col3:
                st.subheader("Agri Services")
                st.dataframe(agri_services_df)
        with st.container():
            st.subheader("Agroprocessing Units")
            st.dataframe(processing_units_df)

    with allied:
        # Create a 2-column layout
        col1, col2 = st.columns(2)

        # Add content to each column
        with col1:
            st.subheader("Allied Infrastructure")
            st.dataframe(allied_infra_df)

        with col2:
            st.subheader("Allied Production")
            st.dataframe(allied_prod_df)

    with narega:
        
        # empoyment offered/ employment availed
        emp_offered_hh = 221524
        emp_availed_hh = 199166

        emp_availed_persons = 341790
        emp_offered_persons = 396828

        # Display the ratio as two columns
        col1, col2 = st.columns(2)
        
        with col1:
            ratio_emp_hh = emp_availed_hh / emp_offered_hh
            # Display the ratio as a metric
            st.metric("Ratio of Employment Availed to Offered to households",  str(round(ratio_emp_hh, 2) * 100) + "%")
        
            # growth rate of Average Wage rate per day per person(Rs.) from narega prgress data
            growth_rate = narega_progress_df.loc[narega_progress_df['Progress'] == 'Average Wage rate per day per person(Rs.)'].iloc[0, 1:].pct_change().mean() * 100

            # Display the growth rate as a metric
            st.metric("CAGR (5 Y) of Average Wage rate per day per person(Rs.)", str(round(growth_rate, 2)) + "%")

        with col2:
            ratio_emp_persons = emp_availed_persons / emp_offered_persons
            # Display the ratio as a metric
            st.metric("Ratio of Employment Availed to Offered to persons", str(round(ratio_emp_persons, 2) * 100) + "%")

        

        # Work Demand
        selected_type = st.selectbox('Select Type', narega_demand_df['Type'].unique())
        # Filter the data based on selected Type
        filtered_demand_df = narega_demand_df[narega_demand_df['Type'] == selected_type]
        # Line graph
        fig = px.line(filtered_demand_df, x='Month', y='Value', color='District')
        fig.update_layout(title='Work Demand: 2023-24', width=800, height=400)
        st.plotly_chart(fig)


        # Progress
        selected_progress = st.selectbox('Select Progress', narega_progress_df['Progress'])

        # Filter the data based on selected progress
        filtered_df = narega_progress_df[['FY 2020-2021', 'FY 2021-2022', 'FY 2022-2023', 'FY 2023-2024', 'FY 2024-2025']].copy()
        filtered_df['Progress'] = narega_progress_df['Progress']
        filtered_df = filtered_df.set_index('Progress').transpose()

        # Bar chart
        fig = px.bar(filtered_df, x=filtered_df.index, y=selected_progress)
        fig.update_layout(width=800, height=400)
        st.plotly_chart(fig)

        # Fin Progress
        selected_fin_progress = st.selectbox('Select Financial Progress', fin_progress_df['Fin_Progress'])
        # Filter the data based on selected progress
        filtered_fin_df = fin_progress_df[['FY 2020-2021', 'FY 2021-2022', 'FY 2022-2023', 'FY 2023-2024', 'FY 2024-2025']].copy()
        filtered_fin_df['Fin_Progress'] = fin_progress_df['Fin_Progress']
        filtered_fin_df = filtered_fin_df.set_index('Fin_Progress').transpose()
        
        # Bar chart
        fig = px.bar(filtered_fin_df, x=filtered_fin_df.index, y=selected_fin_progress)
        fig.update_layout(width=800, height=400)
        st.plotly_chart(fig)


    with fin:
        # Get the latest year from granular_credit_df
        latest_year = granular_credit_df['Year'].max()

        # Filter the dataframe for the latest year
        latest_year_df = granular_credit_df[granular_credit_df['Year'] == latest_year]

        # Get the top three sectors based on their values in the latest year
        top_three_sectors = latest_year_df.drop(columns='Year').sum().sort_values(ascending=False).index.tolist()[:3]
        top_three_sectors_str = ', '.join(top_three_sectors)
        st.write("Top Three Sectors:")
        st.code(top_three_sectors_str)

        # subsector credit
        with st.container():

            col1, empty_col, col2 = st.columns([1, 0.2, 1])

            with col1:
                # Grouped bar chart
                column_names = ['Crop production', 'Minor Irrigation', 'Farm Mechanisation', 'Plantation &Horticulture (inclg Sericulture)',
                                'Forestry & Wasteland Development', 'AH - Dairy Development', 'AH - Poultry Development',
                                'AH - Sheep, Goat & Piggery', 'Fisheries', 'Agri-Infrastructure', 'Storage Godowns & Marketing Infrastructure',
                                'Land Development', 'Agri-Infra others', 'Ancillary Activities', 'Food & Agro-Processing', 'Others']
                selected_columns = st.multiselect('Select columns', column_names, default=top_three_sectors[:2], key='granular_credit')
                filtered_df = granular_credit_df[['Year'] + selected_columns]
                fig = px.bar(filtered_df, x='Year', y=selected_columns, barmode='group', title='Granular Credit Data')
                fig.update_layout(width=600, height=400)
                st.plotly_chart(fig)
            
            with col2:
                # Calculate growth rate for selected columns
                growth_rate_df = filtered_df.copy()
                for col in selected_columns:
                    growth_rate_df[col] = growth_rate_df[col].pct_change() * 100
                
                # Display growth rate as st.metric
                for col in selected_columns:
                    growth_rate = growth_rate_df[col].iloc[-1]
                    st.metric(label=col+' Growth (over latest year)', value=round(growth_rate,1),delta= round(growth_rate_df[col].iloc[-1] - growth_rate_df[col].iloc[-2]) )

        # targets vs achievements
        with st.container():
            col1, empty_col, col2 = st.columns([1, 0.2, 1])
            
            with col1:
                # Grouped bar chart
                column_names = ['Crop Loan Target', 'Crop Loan Achievement', 'Term Loan Target', 'Term Loan Achievement',
                                'Total Agri Credit Target', 'Total Agri Credit Achievement', 'Non-Farm Sector Target',
                                'Non-Farm Sector Achievement', 'Other Priority Sector Target', 'Other Priority Sector Achievement',
                                'Total Priority Sector Target', 'Total Priority Sector Achievement']
                selected_columns = st.multiselect('Select columns', column_names, default=['Crop Loan Target', 'Crop Loan Achievement'], key='targets_vs_achievements')
                filtered_df = targets_achievements_df[['Year'] + selected_columns]
                fig = px.bar(filtered_df, x='Year', y=selected_columns, barmode='group', title='Targets vs Achievements')
                fig.update_layout(width=600, height=400)
                st.plotly_chart(fig)
            with col2:
                with st.container():
                    # Calculate growth rate for selected columns
                    growth_rate_df = filtered_df.copy()
                    for col in selected_columns:
                        growth_rate_df[col] = growth_rate_df[col].pct_change() * 100
                    # Display growth rate as st.metric
                    for col in selected_columns:
                        growth_rate = growth_rate_df[col].iloc[-1]
                        st.metric(label=col+' Growth (over latest year)', value=round(growth_rate,1),delta= round(growth_rate_df[col].iloc[-1] - growth_rate_df[col].iloc[-2]) )

        # Financing
        with st.container():
            col1, empty_col, col2 = st.columns([1, 0.2, 1])

            with col1:
                # Create a dropdown using column names
                column_names = financing_df.columns[1:]
                selected_column = st.selectbox('Select a column', column_names)

                # Filter the data based on the selected column
                filtered_df = financing_df[['Year', selected_column]]

                # Create a bar chart
                fig = px.bar(filtered_df, x='Year', y=selected_column, title='Financing Overview')
                fig.update_layout(xaxis_title='Year', yaxis_title=selected_column)
                st.plotly_chart(fig)
            
            with col2:
                # Calculate growth rate for selected column
                growth_rate_df = filtered_df.copy()
                growth_rate_df[selected_column] = growth_rate_df[selected_column].pct_change() * 100

                # Display growth rate as st.metric
                growth_rate = growth_rate_df[selected_column].iloc[-1]
                st.metric(label=selected_column + ' Growth (over latest year)', value=round(growth_rate, 1), delta=round(growth_rate_df[selected_column].iloc[-1] - growth_rate_df[selected_column].iloc[-2]))

if st.session_state["authentication_status"]:
    # authenticator.logout()
    # st.write(f'Welcome *{st.session_state["name"]}*')
    protected_page()
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')



