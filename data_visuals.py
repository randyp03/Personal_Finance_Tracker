# This file draws all plots for the program

# importing libraries
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import calendar

# draws cash flow plot for each month
def draw_cash_flow(df):
    cash_flow_df = df.copy()

    # all categories not income are considered expense
    cash_flow_df.loc[cash_flow_df['Category'] != "Income", 'Category'] = "Expense"
    # get the totals for each category of each month
    cash_flow_df = cash_flow_df.groupby(['Month','Category'])[['Amount']].sum().reset_index()
    # determining palette for each category
    palette = {'Income': '#4bd02b', 'Expense': '#e33434'}

    # create net income for each month to display at top of plot
    net_income_df = df.copy()
    net_income_df.loc[net_income_df['Category'] != 'Income', 'Amount'] *= -1
    net_income_df = net_income_df.groupby(['Month'])[['Amount']].sum().reset_index()
    net_income = net_income_df.loc[net_income_df['Month']== net_income_df['Month'].max(), 'Amount'][1]

    fig, ax = plt.subplots()
    
    sns.barplot(cash_flow_df,
                x='Month',
                y='Amount',
                hue = 'Category',
                hue_order=palette.keys(),
                errorbar=None,
                palette=palette)
    # setting custom plot title, labels, and text
    ax.set_title('Monthly Cash Flow')
    ax.set_xlabel('Month')
    ax.set_ylabel('Amount ($)')
    ax.set_ylim(top=cash_flow_df['Amount'].max() + (cash_flow_df['Amount'].max() * 0.3))
    # display net income text
    net_income_text = ax.text(x=0.05, 
                              y=0.95,
                              s='${:.2f}'.format(net_income),
                              fontdict=
                                {
                                  "color": '#e33434' if net_income < 0 else '#4bd02b',
                                  "fontsize":20
                                },
                              horizontalalignment='left',
                              verticalalignment='top',
                              transform=ax.transAxes
                            )
    # get box of net_income_text
    renderer = plt.gcf().canvas.get_renderer()
    bbox_1 = net_income_text.get_window_extent(renderer=renderer)
    # getting dimensions of net_income_text box
    bbox_width = bbox_1.width / ax.figure.dpi / ax.get_window_extent().width
    bbox_height = bbox_1.height / ax.figure.dpi / ax.get_window_extent().height

    # adding net_income subtext
    ax.text(
        x=0.05 + bbox_width + 0.26,
        y=0.95 - bbox_height - 0.02,
        s=f"{calendar.month_abbr[net_income_df['Month'].max()]} Net Income",
        fontdict={"fontsize":12},
        horizontalalignment='left',
        verticalalignment='top',
        transform=ax.transAxes
    )
    for container in ax.containers:
        ax.bar_label(container)
    # creates a more compact layout
    # plt.tight_layout()

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
    df.loc[:,['Month_Period']] = df['Date_Formatted'].dt.to_period('M')

    # create df for cumulative sum plot
    cumsum_df=df.loc[df['Category'] != 'Income']
    # create cumulative sum column
    cumsum_df['CumSum'] = cumsum_df.groupby('Month_Period')['Amount'].cumsum()
    # get the current month and previous month
    curr_month = cumsum_df['Month_Period'].max()
    prev_month = curr_month - 1 if curr_month != 1 else 12

    # create two different datasets to plot
    curr_month_df = cumsum_df.loc[cumsum_df['Month_Period'] == curr_month]
    prev_month_df = cumsum_df.loc[cumsum_df['Month_Period'] == prev_month]
    line_color = '#317fce'

    # get the most recent transaction day entered for the current month
    most_recent_day = curr_month_df['Day'].max()
    # get the cumulative sum max until most recently entered day
    curr_month_max = curr_month_df['CumSum'].max()
    # get the cumulative sum max until the same day of the previous month
    prev_month_max_same_day = prev_month_df.loc[prev_month_df['Day'] <= most_recent_day]['CumSum'].max()
    # get the difference of the two cumulative sums
    difference = prev_month_max_same_day - curr_month_max

    fig, ax = plt.subplots()
    # plot current month
    sns.lineplot(data=curr_month_df,
             x='Day',
             y='CumSum',
             errorbar=None,
             color=line_color)
    # plot previous month with added transparency and dotted lines
    sns.lineplot(data=prev_month_df,
             x='Day',
             y='CumSum',
             errorbar=None,
             color=line_color,
             alpha=0.3,
             linestyle="dashed")
    ax.set_title(f'{curr_month.strftime("%B")} Spending')
    ax.set_xlabel('Day')
    ax.set_ylabel('Amount ($)')
    # display current point in graph
    ax.text(x=most_recent_day, y=curr_month_max, s='Today', weight='bold')
    # display total spending during current month
    ax.text(x=1,
            y=np.percentile(np.array(prev_month_df['CumSum']), 95), 
            s=f'${curr_month_max}', 
            fontdict={
                "fontsize":20
                }
            )
    # # display comparison to previous month's spending
    ax.text(x=1,
            y=np.percentile(np.array(prev_month_df['CumSum']), 85), 
            s= '${:.2f} more than last month'.format(abs(difference)) if difference < 0 
                else '${:.2f} less than last month'.format(abs(difference)), 
            fontdict={
                "color":'#e33434' if difference < 0 else '#4bd02b', 
                "fontsize":12
                }
            )
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