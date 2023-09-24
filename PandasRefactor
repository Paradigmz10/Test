import pandas as pd

def reshape_and_add_totals_with_pandas(
    program_management_review=None,
    funding_set=None,
    funding_type=None,
    previous_two_fiscal_years=None,
):
    if not all([program_management_review, funding_set, funding_type, previous_two_fiscal_years]):
        return pd.DataFrame()

    # Convert funding_set into a DataFrame
    df = pd.DataFrame([vars(item) for item in funding_set])

    # Create pivot table for primary logic
    df_no_carryover = df[df['carryover'] == False]
    pivot = df_no_carryover.pivot_table(
        index='appropriation_category',
        columns='fiscal_quarter',
        values=['spend_plan', 'obligations', 'expenditures'],
        aggfunc='sum'
    ).fillna(0)

    # Compute the sums
    pivot['spend_plan', 'Total'] = pivot['spend_plan'].sum(axis=1)
    pivot['obligations', 'Total'] = pivot['obligations'].sum(axis=1)
    pivot['expenditures', 'Total'] = pivot['expenditures'].sum(axis=1)

    # Process carryover_funding
    carryover_mask = (
        (df['funding_type'] == funding_type) &
        df['carryover']
    )
    df_carryover = df[carryover_mask]

    # Separate logic for previous_two_fiscal_years and fiscal_quarters
    carryover_pivot_list = []
    for fy in previous_two_fiscal_years:
        fiscal_qtrs = list(fy.fiscal_quarters.all())
        df_fy = df_carryover[df_carryover['fiscal_quarter'].isin(fiscal_qtrs)]
        
        pivot_carryover = df_fy.pivot_table(
            index='appropriation_category',
            columns='fiscal_quarter',
            values=['spend_plan', 'obligations', 'expenditures'],
            aggfunc='sum'
        ).fillna(0)

        # Compute the sums
        pivot_carryover['spend_plan', 'Total'] = pivot_carryover['spend_plan'].sum(axis=1)
        pivot_carryover['obligations', 'Total'] = pivot_carryover['obligations'].sum(axis=1)
        pivot_carryover['expenditures', 'Total'] = pivot_carryover['expenditures'].sum(axis=1)
        
        carryover_pivot_list.append(pivot_carryover)

    # Combining DataFrames for each fiscal year
    carryover_df = pd.concat(carryover_pivot_list, axis=1)
    
    # Adding total row for carryover
    carryover_totals = carryover_df.sum()
    carryover_df.loc['Total'] = carryover_totals

    # Compute bottom line calculations
    bottomline_df = pivot + carryover_df
    bottomline_df = bottomline_df.loc[['Total']]

    # Combine all the DataFrames
    final_df = pd.concat([pivot, carryover_df, bottomline_df], axis=0)

    return final_df
