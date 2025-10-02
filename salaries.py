from cmath import isnan
import streamlit as st 
import pandas as pd
import altair as alt


# # import grid 12 step 1 data
# grid12_df = pd.read_csv("grid-salary-data/grid12-step1.csv")
# # calculate percentage increase and add it to dataframe
# grid12_df = grid12_df.sort_values("YEAR")
# grid12_df = grid12_df.rename(columns={"YEAR": "year", "ANNUAL_SALARY": "salary"})
# grid12_df["pct_increase"] = grid12_df["salary"].pct_change() * 100

# grid12_df

# # display grid 12 step 1 salary data
# st.write('Grid 12 Step 1 Annual Salary by Fiscal Year')
# grid12_salary_line_chart = st.line_chart(data=grid12_df, y='salary', x_label='Fiscal Year', y_label='Annual Salary')

# import deputy minister salary data
dm_25_df = pd.read_csv("deputy-ministers-data/fye25-deputy-ministers.csv")
dm_25_df.set_index('Name', inplace=True)
dm_24_df = pd.read_csv("deputy-ministers-data/fye24-deputy-ministers.csv")
dm_24_df.set_index('Name', inplace=True)
dm_23_df = pd.read_csv("deputy-ministers-data/fye23-deputy-ministers.csv")
dm_23_df.set_index('Name', inplace=True)
dm_22_df = pd.read_csv("deputy-ministers-data/fye22-deputy-ministers.csv")
dm_22_df.set_index('Name', inplace=True)
dm_21_df = pd.read_csv("deputy-ministers-data/fye21-deputy-ministers.csv")
dm_21_df.set_index('Name', inplace=True)
dm_20_df = pd.read_csv("deputy-ministers-data/fye20-deputy-ministers.csv")
dm_20_df.set_index('Name', inplace=True)
dm_19_df = pd.read_csv("deputy-ministers-data/fye19-deputy-ministers.csv")
dm_19_df.set_index('Name', inplace=True)
dm_18_df = pd.read_csv("deputy-ministers-data/fye18-deputy-ministers.csv")
dm_18_df.set_index('Name', inplace=True)
dm_17_df = pd.read_csv("deputy-ministers-data/fye17-deputy-ministers.csv")
dm_17_df.set_index('Name', inplace=True)

# deputy minister to the premier
dm_to_premier_salaries = {}
# Nov 2020 - Nov 2022: Lori Wanamaker
dm_to_premier_salaries['31 Mar 2020'] = {'name': 'Lori Wanamaker', 'salary': int(dm_20_df.loc['WANAMAKER, LORI M'][" Salary and Other Compensation "].replace(',',''))}
dm_to_premier_salaries['31 Mar 2021'] = {'name': 'Lori Wanamaker', 'salary': int(dm_21_df.loc['WANAMAKER, LORI M'][" Salary and Other Compensation "].replace(',',''))}
dm_to_premier_salaries['31 Mar 2022'] = {'name': 'Lori Wanamaker', 'salary': int(dm_22_df.loc['WANAMAKER, LORI M.'][" Salary and Other Compensation "].replace(',',''))}
dm_to_premier_salaries['31 Mar 2023'] = {'name': 'Lori Wanamaker', 'salary': int(float(dm_23_df.loc['WANAMAKER,  LORI M'][" Salary and Other Compensation "].replace(',','')))}
# Nov 2022 - present: Shannon Salter
dm_to_premier_salaries['31 Mar 2024'] = {'name': 'Shannon Salter', 'salary': int(dm_24_df.loc['SALTER, SHANNON'][" Salary and Other Compensation "].replace(',',''))}
dm_to_premier_salaries['31 Mar 2025'] = {'name': 'Shannon Salter', 'salary': int(dm_25_df.loc['Salter,Shannon'][" Salary and Other Compensation "].replace(',',''))}

dm_premier_df = pd.DataFrame([{"date": date, "name": values["name"], "salary": values["salary"]} for date, values in dm_to_premier_salaries.items()])
dm_premier_df.sort_values('date')
dm_premier_df['pct_increase'] = dm_premier_df.groupby('name')['salary'].pct_change() * 100

chart = (
    alt.Chart(dm_premier_df).mark_line(point=True).encode(x=alt.X("date:O", title="Year"), y=alt.Y("salary:Q", title="Salary"), color="name:N")
)
st.altair_chart(chart, use_container_width=True)
dm_premier_df

annual_cpi_df = pd.read_csv("cpi_annual_averages.csv")
st.write("BC Annual CPI changes (indexed to 100 for year 2002)")
annual_cpi_df

bcgeu_wage_increases_df = pd.read_csv("grid-salary-data/bcgeu_wage_increases.csv")

# reshape for purpose of chart
dm_premier_df['date'] = pd.to_datetime(dm_premier_df['date'], format="%d %b %Y")
dm_premier_df['year'] = dm_premier_df['date'].dt.year

annual_cpi_df['date'] = pd.to_datetime(annual_cpi_df['date'], format="%d %b %Y")
annual_cpi_df['year'] = annual_cpi_df['date'].dt.year
annual_cpi_df = annual_cpi_df.rename(columns={'Annual Percent Change': 'pct_increase'})

# make sure "date" column is in datetime format
bcgeu_wage_increases_df["date"] = pd.to_datetime(bcgeu_wage_increases_df["date"], format="%d %b %Y", errors="coerce")
# extract year from "date" column
bcgeu_wage_increases_df["year"] = bcgeu_wage_increases_df["date"].dt.year

st.header("BCGEU Wage Increase History")
st.table(bcgeu_wage_increases_df)

st.header("Year-over-Year Inflation in BC vs. BCGEU Wage Increases vs. Deputy Minister to the Premier Wage Increases")

chart = (
    alt.Chart(dm_premier_df)
    .mark_line(point=True)
    .encode(
        x=alt.X("year:O", title="Year"),
        y=alt.Y("pct_increase:Q", title="Percent Change"),
        tooltip=[alt.Tooltip("year:O"), alt.Tooltip("pct_increase:Q", title="DM to the Premier Wage Increase (%)", format=".2f")]
    )
)
cpi_chart = (
    alt.Chart(annual_cpi_df)
    .mark_tick(color="black", thickness=2)
    .encode(
        x=alt.X("year:O"),
        y=alt.Y("pct_increase:Q"),
        tooltip=[alt.Tooltip("year:O"), alt.Tooltip("pct_increase:Q", title="CPI Increase (%) in BC", format=".1f")]
    )
)
bcgeu_inc_chart = (
    alt.Chart(bcgeu_wage_increases_df)
    .mark_bar()
    .encode(
        x=alt.X("year:O", title="Year"),
        y=alt.Y("pct_increase:Q", stack="zero"),
        color=alt.value("#ff7f0e"),
        tooltip=[alt.Tooltip("date:T"), alt.Tooltip("pct_increase:Q", title="Wage Increase (%)", format=".1f")]
    )
)
percentages_charts = [chart, bcgeu_inc_chart, cpi_chart]
combined_percentages_charts = alt.layer(*percentages_charts).resolve_scale(y="shared").properties(
        width="container",  # let width flex to container
        height=400          # fixed height in pixels
    )
st.altair_chart(combined_percentages_charts, use_container_width=True)

# Deputy Minister Salary & Travel Expenses over time (interactive chart)
dm_yearly_dfs = {
    2017: dm_17_df,
    2018: dm_18_df,
    2019: dm_19_df,
    2020: dm_20_df,
    2021: dm_21_df,
    2022: dm_22_df,
    2023: dm_23_df,
    2024: dm_24_df,
    2025: dm_25_df,
}
# reshape dm_yearly_dfs into a single dataframe
all_years = []
for year, df in dm_yearly_dfs.items():
    df_year = df.reset_index()[["Name", " Salary and Other Compensation ", " Travel"]].copy()
    df_year["Year"] = year
    all_years.append(df_year)
combined_df = pd.concat(all_years, ignore_index=True)
combined_df = combined_df.rename(columns={" Salary and Other Compensation ": "Salary", " Travel": "Travel"})
combined_df = combined_df.dropna(subset=["Name"]) # drop rows where value of Name is null
combined_df = combined_df[combined_df["Name"] != "Grand Total"] # drop rows where value of Name is "Grantd Total"
combined_df["Name_clean"] = (
    combined_df["Name"]
    .str.strip()
    .str.replace(".", "")       # strip periods
    .str.replace(",", ", ", regex=True)     # normalize commas
    .str.replace(r"\s+", " ", regex=True)   # collapse spaces
    .str.title()                            # title case
)
combined_df["Salary"] = (
    combined_df["Salary"]
    .astype(str)                            # ensure string first
    .str.replace(r"[^\d.]", "", regex=True) # strip commas, spaces, symbols
    .astype(float)                          # convert string to float
)
combined_df["Travel"] = (
    combined_df["Travel"]
    .astype(str)                            # ensure type string first
    .str.replace(r"[^\d.]", "", regex=True) # strip commas, spaces, symbols
)
combined_df["Travel"] = pd.to_numeric(combined_df["Travel"], errors="coerce")

# calculate percent salary increase YoY for each name
combined_df = combined_df.sort_values(["Name_clean", "Year"])
combined_df["pct_increase_salary"] = (
    combined_df.groupby("Name_clean")["Salary"]
    .pct_change() * 100
)


# display data
st.title("Deputy Ministers - Salary and Raises compared to Inflation")

st.write("Use the interactive chart below to compare deputy minister salaries and annual raises per year, against inflation (measured as the percent change in the Consumer Price Index in British Columbia).")

# allow user to select exactly 1 metric to plot
metric = st.radio(
    "Select metric to plot:",
    options=["Salary", "Travel"],
    horizontal=True
)
# let user select 1 or more names
names = st.multiselect(
    "Select name(s)",
    options=combined_df["Name_clean"].unique(),
    default=[combined_df["Name_clean"].unique()[0]]
)
filtered = combined_df[combined_df["Name_clean"].isin(names)]

if filtered.empty:
    st.warning("No data available for the selected name(s)")
else:
    charts = []
    line_chart = (
        alt.Chart(filtered)
        .mark_line(point=True)
        .encode(
            x=alt.X("Year:O", sort=sorted(combined_df["Year"].unique()), title="Year"),
            y=alt.Y(f"{metric}:Q", title=metric, axis=alt.Axis(format="$,.0f"), scale=alt.Scale(domain=[0, filtered[metric].max()])), # format axis for currency
            color=alt.Color("Name_clean:N", legend=alt.Legend(title="Name")),
            tooltip=["Name:N", alt.Tooltip("Year:O"), alt.Tooltip(f"{metric}:Q", format="$,.0f")]
        )
    )
    charts.append(line_chart)
    if metric == "Salary":
        filtered_inflation_df = annual_cpi_df.copy()
        filtered_inflation_df = filtered_inflation_df.rename(
            columns={"pct_increase": "PercentChange"}
        )
        filtered_inflation_df["date"] = pd.to_datetime(filtered_inflation_df["date"], errors="coerce")
        filtered_inflation_df["Year"] = filtered_inflation_df["date"].dt.year
        filtered_inflation_df = filtered_inflation_df[filtered_inflation_df["Year"] > 2016]
        
        # ----------------- shared y-axis for percentages ----------------
        max_y = max(filtered["pct_increase_salary"].max(), filtered_inflation_df["PercentChange"].max())
        if isnan(max_y):
            max_y = 30
        percent_y = alt.Y("PercentChange:Q", stack=False, title="Percent Change", axis=alt.Axis(format=".1f"), scale=alt.Scale(domain=[0, max_y]))
        
        salary_increase_bar_chart = (
            alt.Chart(filtered.assign(PercentChange=filtered["pct_increase_salary"]))
            .mark_bar(opacity=0.7)
            .encode(
                x=alt.X("Year:N", title="Year"),
                xOffset="Name_clean:N",   # 👈 this puts bars side-by-side
                y=percent_y,
                color="Name_clean:N",
                tooltip=[
                    alt.Tooltip("Name_clean:N", title="Name"),
                    alt.Tooltip("Year:O", title="Year"),
                    alt.Tooltip("PercentChange:Q", title="Salary Increase (%)", format=".1f")
                ]
            )
        )

        charts.append(salary_increase_bar_chart)
        
        # inflation as dashed black line
        inflation_chart = (
            alt.Chart(filtered_inflation_df)
            .mark_tick(color="black", thickness=3)
            .encode(
                x=alt.X("Year:O"),
                y=percent_y,
                tooltip=[
                    alt.Tooltip("Year:O"),
                    alt.Tooltip("PercentChange:Q", title="CPI increase in BC", format=".1f")
                ]
            )
        )
        charts.append(inflation_chart)

    # combine all charts, share same y-axis when comparing percentages
    combined_chart = alt.layer(*charts).resolve_scale(y="independent").properties(
        width="container",  # let width flex to container
        height=400          # fixed height in pixels
    )
    st.altair_chart(combined_chart, use_container_width=True)


st.write("CPI data source: https://catalogue.data.gov.bc.ca/dataset/2c75c627-3eb6-41ee-bb54-7b089eade484/resource/2a88899d-e962-43c5-81a5-438e9ef89b9d")
st.write("BCGEU Wage Increases source: https://www2.gov.bc.ca/assets/gov/careers/all-employees/pay-and-benefits/salaries-overtime-and-other-wages/bcgeu_wage_increases.pdf")
