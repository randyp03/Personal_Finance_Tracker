# This file draws all plots for the program

# importing libraries
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# draws cash flow plot for each month
def draw_cash_flow(df):
    net_income_df = df.copy()
    net_income_df.loc[net_income_df['Category'] != 'Income', 'Amount'] *= -1
    net_income_df = net_income_df.groupby(['Month'])[['Amount']].sum().sort_values('Amount', ascending=False)
    net_income_df['Net_Status'] = ['Negative' if x < 0 else 'Positive' for x in net_income_df['Amount']]
    palette = {'Positive': '#4bd02b', 'Negative': '#e33434'}

    fig, ax = plt.subplots()
    sns.barplot(net_income_df,
                x='Month',
                y='Amount',
                hue = 'Net_Status',
                palette=palette,
                legend=False)
    ax.set_title('Monthly Cash Flow')
    ax.set_xlabel('Month')
    ax.set_ylabel('Amount ($)')
    plt.tight_layout()

    return plt.show()

# returns a barplot displaying categorical expenses
def draw_categorical_expenses(df):
    fig, ax = plt.subplots()
    sns.barplot(df.loc[df['Category'] != 'Income'].groupby('Category')[['Amount']].sum().sort_values('Amount', ascending=False),
                x='Amount',
                y='Category',
                orient='h')
    ax.set_title('Categorical Expenses')
    ax.set_xlabel('Amount ($)')
    ax.set_ylabel('Category')
    plt.tight_layout()

    return plt.show()

# returns a bar plot displaying expenses by month colored by sub-category
def draw_subcat_expenses(df):
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(df.loc[df['Category'] != 'Income'].groupby(['Month','Sub-Category'])[['Amount']].sum().sort_values('Amount', ascending=False),
                x='Amount',
                y='Month',
                hue="Sub-Category",
                dodge=False,
                orient='h')
    ax.set_title('Sub-Category Expenses')
    ax.set_xlabel('Amount ($)')
    ax.set_ylabel('Month')
    plt.tight_layout()

    return plt.show()

# returns cumulative sum of current month to compare to previous month
def draw_cumsum_plot(df):
    df=df.loc[df['Category'] != 'Income']
    # create cumulative sum column
    df['CumSum'] = df.groupby('Month')['Amount'].cumsum()
    # get the current month and previous month
    curr_month = df['Date_Formatted'].dt.to_period('M').max()
    prev_month = curr_month - 1 if curr_month != 1 else 12

    # create two different datasets to plot
    curr_month_df = df.loc[df['Date_Formatted'].dt.to_period('M') == curr_month]
    prev_month_df = df.loc[df['Date_Formatted'].dt.to_period('M') == prev_month]
    line_color = '#317fce'

    # get the most recent transaction day entered for the current month
    most_recent_day = curr_month_df['Day'].max()
    # get the cumulative sum max until most recently entered day
    curr_month_max = curr_month_df['CumSum'].max()
    # get the cumulative sum max until the same day of the previous month
    prev_month_max_same_day = prev_month_df.loc[prev_month_df['Day'] <= most_recent_day]['CumSum'].max()
    # get the difference of the two cumulative sums
    difference = round(prev_month_max_same_day - curr_month_max,2)
    # return spending string depending on how it compares to the previous month
    if difference < 0:
        spending_text = f'${abs(difference)} more than last month'
        comp_color = '#e33434' # red
    else: 
        spending_text = f'${abs(difference)} less than last month'
        comp_color = '#4bd02b' # green

    fig, ax = plt.subplots()
    # plot current month
    sns.lineplot(data=curr_month_df,
             x='Day',
             y='CumSum',
             errorbar=None,
             color=line_color,
             label=curr_month)
    # plot previous month with added transparency and dotted lines
    sns.lineplot(data=prev_month_df,
             x='Day',
             y='CumSum',
             errorbar=None,
             color=line_color,
             alpha=0.3,
             linestyle="dashed",
             label=prev_month)
    ax.set_title(f'{curr_month.strftime("%B")} Spending')
    ax.set_xlabel('Day')
    ax.set_ylabel('Amount ($)')
    plt.legend().remove()
    # display current point in graph
    plt.text(x=most_recent_day, y=curr_month_max, s='Today', weight='bold')
    # display total spending during current month
    plt.text(x=1,
             y=np.percentile(np.array(prev_month_df['CumSum']), 95), 
             s=f'${curr_month_max}', 
             fontdict={ 
                 "fontsize":20
                 })
    # display comparison to previous month's spending
    plt.text(x=1,
             y=np.percentile(np.array(prev_month_df['CumSum']), 85), 
             s=spending_text, 
             fontdict={
                 "color":comp_color, 
                 "fontsize":12
                 })
    plt.tight_layout()

    return plt.show()

# main function to view different plots
def plot(PLOTS, df):
    print()
    print(f"{'*' * 15} Available Charts {'*' * 15}")
    for plot in PLOTS:
        print(f"{plot} - {PLOTS[plot]}")

    choice = int(input('\nWhich visual would you like to view? '))
    
    try:
        if choice == 0:
            return
        elif choice == 1:
            draw_cash_flow(df)
        elif choice == 2:
            draw_categorical_expenses(df)
        elif choice == 3:
            draw_subcat_expenses(df)
        elif choice == 4:
            draw_cumsum_plot(df)
    # user must choose one of the options above
    except KeyError:
        print('\nInvalid option. Please enter an option from the available list.\n')
        plot(PLOTS)

def main(csv_file):
    # manipulate dataset before calling PLOT function
    DATE_FORMAT = '%m-%d-%Y'
    df = pd.read_csv(csv_file)

    visuals_df = df.copy().sort_values('Date')
    visuals_df['Date_Formatted'] = pd.to_datetime(visuals_df['Date'], format=DATE_FORMAT)
    visuals_df['Month'] = visuals_df['Date_Formatted'].dt.month
    visuals_df['Day'] = visuals_df['Date_Formatted'].dt.day

    PLOTS = {
        0: 'Exit',
        1: 'Cash Flow',
        2: 'Categorical Expenses',
        3: 'Sub-Categorical Expenses',
        4: 'Monthly Spending',
    }

    plot(PLOTS, visuals_df)

if __name__ == "__main__":
    csv_file = 'transactions.csv'
    
    main(csv_file)