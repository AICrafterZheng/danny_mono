import numpy as np
import matplotlib.pyplot as plt

def calculate_mortgage_payment(principal, annual_rate, years):
    """Calculate monthly mortgage payment"""
    monthly_rate = annual_rate / 12
    num_payments = years * 12
    if monthly_rate == 0:
        return principal / num_payments
    return principal * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)

def calculate_remaining_principal(principal, annual_rate, years, months_paid):
    """Calculate remaining principal after a certain number of months"""
    if months_paid >= years * 12:
        return 0
    
    monthly_rate = annual_rate / 12
    num_payments = years * 12
    monthly_payment = calculate_mortgage_payment(principal, annual_rate, years)
    
    if monthly_rate == 0:
        return principal - (monthly_payment * months_paid)
    
    remaining = principal * (1 + monthly_rate)**months_paid
    for i in range(months_paid):
        remaining -= monthly_payment * (1 + monthly_rate)**(months_paid - 1 - i)
    
    return remaining

def analyze_housing_investment(purchase_price, down_payment_percent, loan_interest_rate, 
                              loan_term_years, holding_period_years, property_tax_annual,
                              hoa_monthly, sale_price, monthly_rent, 
                              stock_investment_return, selling_cost_percent):
    """
    Analyze and compare different housing investment scenarios
    
    Args:
        purchase_price: House purchase price
        down_payment_percent: Down payment as a percentage of purchase price
        loan_interest_rate: Annual interest rate as a decimal (e.g., 0.025 for 2.5%)
        loan_term_years: Loan term in years
        holding_period_years: How long you plan to hold the property before selling
        property_tax_annual: Annual property tax
        hoa_monthly: Monthly HOA fees
        sale_price: Expected sale price after holding period
        monthly_rent: Monthly rent if renting instead of buying
        stock_investment_return: Annual return on stock investment as a decimal
        selling_cost_percent: Selling costs as a percentage of sale price
        
    Returns:
        Dictionary containing analysis of different scenarios
    """
    # Calculate down payment and loan amount
    down_payment = purchase_price * down_payment_percent
    loan_amount = purchase_price - down_payment
    
    # Calculate monthly mortgage payment
    monthly_payment = calculate_mortgage_payment(loan_amount, loan_interest_rate, loan_term_years)
    
    # Calculate total payments over holding period
    total_months = holding_period_years * 12
    total_mortgage_payments = monthly_payment * total_months
    total_property_tax = property_tax_annual * holding_period_years
    total_hoa = hoa_monthly * total_months
    
    # Calculate remaining loan balance after holding period
    remaining_balance = calculate_remaining_principal(loan_amount, loan_interest_rate, loan_term_years, total_months)
    
    # Calculate selling costs
    selling_costs = sale_price * selling_cost_percent
    
    # Scenario 1: Buy and sell
    costs_buying = down_payment + total_mortgage_payments + total_property_tax + total_hoa
    net_from_sale = sale_price - selling_costs - remaining_balance
    buy_profit = net_from_sale - costs_buying
    
    # Modify this line
    buy_equity_gain = net_from_sale - (down_payment + total_mortgage_payments + total_property_tax + total_hoa)
    
    # Calculate rent savings
    rent_savings = monthly_rent * total_months
    buy_total_benefit = buy_equity_gain + rent_savings
    
    # Scenario 2: Rent and don't invest
    rent_cost = monthly_rent * total_months
    
    # Scenario 3: Rent and invest down payment
    # Calculate future value of investment
    investment_future_value = down_payment * (1 + stock_investment_return)**(holding_period_years)
    investment_gain = investment_future_value - down_payment
    rent_invest_net = investment_gain - rent_cost
    
    results = {
        "inputs": {
            "purchase_price": purchase_price,
            "down_payment": down_payment,
            "loan_amount": loan_amount,
            "monthly_payment": monthly_payment,
            "holding_period_years": holding_period_years,
            "sale_price": sale_price,
            "monthly_rent": monthly_rent,
            "stock_investment_return": stock_investment_return,
            "selling_cost_percent": selling_cost_percent,
            "loan_interest_rate": loan_interest_rate,
            "loan_term_years": loan_term_years
        },
        "buy_and_sell": {
            "total_payments": costs_buying,
            "mortgage_payments": total_mortgage_payments,
            "property_tax": total_property_tax,
            "hoa_fees": total_hoa,
            "remaining_balance": remaining_balance,
            "selling_costs": selling_costs,
            "net_from_sale": net_from_sale,
            "equity_gain": buy_equity_gain,
            "rent_savings": rent_savings,
            "total_benefit": buy_total_benefit
        },
        "rent_only": {
            "total_rent": rent_cost,
            "net_worth_change": -rent_cost
        },
        "rent_and_invest": {
            "total_rent": rent_cost,
            "investment_value": investment_future_value,
            "investment_gain": investment_gain,
            "net_worth_change": rent_invest_net
        }
    }
    
    return results

def format_color(text, color):
    """Format text with color using ANSI escape codes"""
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'bold': '\033[1m',
        'underline': '\033[4m',
        'end': '\033[0m'
    }
    return f"{colors.get(color, '')}{text}{colors['end']}"

def format_currency(amount, color=None):
    """Format amount as currency with optional color"""
    formatted = f"${amount:,.2f}"
    if color:
        return format_color(formatted, color)
    return formatted

def print_results(results):
    """Print analysis results in a readable format with calculation details"""
    inputs = results["inputs"]
    buy = results["buy_and_sell"]
    rent = results["rent_only"]
    invest = results["rent_and_invest"]
    
    print(f"\n{format_color('===== HOUSING INVESTMENT ANALYSIS =====', 'bold')}\n")
    
    print(f"{format_color('INPUTS:', 'cyan')}")
    print(f"Purchase Price: {format_currency(inputs['purchase_price'], 'yellow')}")
    print(f"Down Payment: {format_currency(inputs['down_payment'], 'yellow')} ({inputs['down_payment']/inputs['purchase_price']*100:.1f}%)")
    print(f"Loan Amount: {format_currency(inputs['loan_amount'], 'yellow')} (Purchase Price - Down Payment)")
    
    print(f"\n{format_color('MORTGAGE PAYMENT CALCULATION:', 'cyan')}")
    print(f"  Loan Amount: {format_currency(inputs['loan_amount'], 'yellow')}")
    print(f"  Annual Interest Rate: {format_color(f'{inputs['loan_interest_rate']*100:.2f}%', 'purple')}")
    print(f"  Monthly Interest Rate: {format_color(f'{inputs['loan_interest_rate']/12*100:.4f}%', 'purple')}")
    print(f"  Loan Term: {format_color(f'{inputs['loan_term_years']} years ({inputs['loan_term_years']*12} months)', 'white')}")
    print(f"Monthly Mortgage Payment: {format_currency(inputs['monthly_payment'], 'green')}")
    
    print(f"\n{format_color('SCENARIO 1: BUY AND SELL AFTER HOLDING PERIOD', 'cyan')}")
    print("Monthly Mortgage Payment Breakdown:")
    print(f"  Monthly Payment: {format_currency(inputs['monthly_payment'], 'green')}")
    print(f"  Number of Months: {format_color(str(inputs['holding_period_years']*12), 'white')} months")
    print(f"Total Mortgage Payments: {format_currency(buy['mortgage_payments'], 'red')}")
    
    print("\nProperty Tax Breakdown:")
    print(f"  Annual Property Tax: {format_currency(buy['property_tax']/inputs['holding_period_years'], 'yellow')}")
    print(f"Total Property Tax: {format_currency(buy['property_tax'], 'red')}")
    
    print("\nHOA Breakdown:")
    print(f"  Monthly HOA: {format_currency(buy['hoa_fees']/(inputs['holding_period_years']*12), 'yellow')}")
    print(f"Total HOA Fees: {format_currency(buy['hoa_fees'], 'red')}")
    
    print(f"\n{format_color('Remaining Loan Balance:', 'cyan')} {format_currency(buy['remaining_balance'], 'red')}")
    
    print(f"\n{format_color('Net from Sale Calculation:', 'cyan')}")
    print(f"  Sale Price: {format_currency(inputs['sale_price'], 'green')}")
    print(f"  - Selling Costs: {format_currency(buy['selling_costs'], 'red')}")
    print(f"  - Remaining Balance: {format_currency(buy['remaining_balance'], 'red')}")
    print(f"  = Net from Sale: {format_currency(buy['net_from_sale'], 'green')}")
    
    print(f"\n{format_color('Equity Gain Calculation:', 'cyan')}")
    print(f"  Net from Sale: {format_currency(buy['net_from_sale'], 'green')}")
    print("  Money invested:")
    print(f"    - Down Payment: {format_currency(inputs['down_payment'], 'red')}")
    print(f"    - Total Mortgage Payments: {format_currency(buy['mortgage_payments'], 'red')}")
    print(f"    - Total Property Tax: {format_currency(buy['property_tax'], 'red')}")
    print(f"    - Total HOA: {format_currency(buy['hoa_fees'], 'red')}")
    total_invested = inputs['down_payment'] + buy['mortgage_payments'] + buy['property_tax'] + buy['hoa_fees']
    print(f"  Total Money Invested: {format_currency(total_invested, 'red')}")
    print(f"  Equity Gain: {format_currency(buy['equity_gain'], 'green' if buy['equity_gain'] > 0 else 'red')}")
    
    print(f"\n{format_color('Total Benefit Calculation:', 'cyan')}")
    print(f"  Equity Gain: {format_currency(buy['equity_gain'], 'green' if buy['equity_gain'] > 0 else 'red')}")
    print(f"  + Rent Savings: {format_currency(buy['rent_savings'], 'green')}")
    print(f"  = Total Benefit: {format_currency(buy['total_benefit'], 'green' if buy['total_benefit'] > 0 else 'red')}")
    
    print(f"\n{format_color('SCENARIO 2: RENT ONLY', 'cyan')}")
    print("Total Rent Paid Calculation:")
    print(f"  Monthly Rent: {format_currency(inputs['monthly_rent'], 'yellow')}")
    print(f"  × Number of Months: {format_color(str(inputs['holding_period_years']*12), 'white')} months")
    print(f"  = Total Rent Paid: {format_currency(rent['total_rent'], 'red')} ({format_currency(inputs['monthly_rent'], 'yellow')} × {inputs['holding_period_years']*12} months)")
    print(f"  Net Worth Change: {format_currency(rent['net_worth_change'], 'red')} (negative of total rent paid)")
    
    print(f"\n{format_color('SCENARIO 3: RENT AND INVEST DOWN PAYMENT', 'cyan')}")
    print("Rent Cost:")
    print(f"  Monthly Rent: {format_currency(inputs['monthly_rent'], 'yellow')}")
    print(f"  × Number of Months: {format_color(str(inputs['holding_period_years']*12), 'white')} months")
    print(f"  = Total Rent Paid: {format_currency(invest['total_rent'], 'red')} ({format_currency(inputs['monthly_rent'], 'yellow')} × {inputs['holding_period_years']*12} months)")
    
    print("\nInvestment Calculation:")
    print(f"  Initial Investment (Down Payment): {format_currency(inputs['down_payment'], 'yellow')}")
    print(f"  Annual Return Rate: {format_color(f'{inputs['stock_investment_return']*100:.1f}%', 'purple')}")
    print(f"  Investment Period: {format_color(str(inputs['holding_period_years']), 'white')} years")
    print(f"  Formula: Initial × (1 + Return Rate)^Years")
    print(f"  = {format_currency(inputs['down_payment'], 'yellow')} × (1 + {inputs['stock_investment_return']*100:.1f}%)^{inputs['holding_period_years']}")
    print(f"Investment Future Value: {format_currency(invest['investment_value'], 'green')}")
    print(f"Investment Gain: {format_currency(invest['investment_gain'], 'green')} (Future Value - Initial Investment)")
    print(f"Net Worth Change: {format_currency(invest['net_worth_change'], 'green' if invest['net_worth_change'] > 0 else 'red')} (Investment Gain - Total Rent)")
    
    print(f"\n{format_color('COMPARISON:', 'bold')}")
    buy_vs_rent = buy['total_benefit'] - rent['net_worth_change']
    buy_vs_invest = buy['total_benefit'] - invest['net_worth_change']
    invest_vs_rent = invest['net_worth_change'] - rent['net_worth_change']
    
    print(f"Buy vs. Rent Only Advantage: {format_currency(buy_vs_rent, 'green' if buy_vs_rent > 0 else 'red')}")
    print(f"Buy vs. Rent+Invest Advantage: {format_currency(buy_vs_invest, 'green' if buy_vs_invest > 0 else 'red')}")
    print(f"Rent+Invest vs. Rent Only Advantage: {format_currency(invest_vs_rent, 'green' if invest_vs_rent > 0 else 'red')}")
    
    best_option = max([
        ("Buy and Sell", buy['total_benefit']),
        ("Rent Only", rent['net_worth_change']),
        ("Rent and Invest", invest['net_worth_change'])
    ], key=lambda x: x[1])
    
    print(f"\n{format_color('Best financial option:', 'bold')} {format_color(best_option[0], 'green')} (Net benefit: {format_currency(best_option[1], 'green' if best_option[1] > 0 else 'red')})")

def plot_comparison(results):
    """Plot comparison of different scenarios"""
    labels = ['Buy & Sell', 'Rent Only', 'Rent & Invest']
    values = [
        results['buy_and_sell']['total_benefit'],
        results['rent_only']['net_worth_change'],
        results['rent_and_invest']['net_worth_change']
    ]
    
    colors = ['green', 'red', 'blue']
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, values, color=colors)
    
    plt.title('Housing Investment Strategy Comparison')
    plt.ylabel('Net Worth Change ($)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add values on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'${int(height):,}',
                 ha='center', va='bottom' if height > 0 else 'top', 
                 color='black' if height > 0 else 'white')
    
    plt.tight_layout()
    plt.show()

def enter_data():
     # Custom scenario - you can modify these values
    print("\n\n" + "="*60 + "\n")
    print("Enter your own values for analysis:")
    
    try:
        purchase_price = float(input("Purchase price ($): ") or "1085000")
        down_payment_percent = float(input("Down payment percentage (%): ") or "30") / 100
        loan_interest_rate = float(input("Loan interest rate (%): ") or "2.5") / 100
        loan_term_years = float(input("Loan term (years): ") or "30")
        holding_period_years = float(input("Holding period (years): ") or "5")
        property_tax_annual = float(input("Annual property tax ($): ") or "13440")
        hoa_monthly = float(input("Monthly HOA/maintenance ($): ") or "300")
        sale_price = float(input("Expected sale price ($): ") or "1400000")
        monthly_rent = float(input("Monthly rent alternative ($): ") or "3500")
        stock_investment_return = float(input("Annual stock investment return (%): ") or "10") / 100
        selling_cost_percent = float(input("Selling costs (%): ") or "7") / 100
        
        custom_results = analyze_housing_investment(
            purchase_price=purchase_price,
            down_payment_percent=down_payment_percent,
            loan_interest_rate=loan_interest_rate,
            loan_term_years=loan_term_years,
            holding_period_years=holding_period_years,
            property_tax_annual=property_tax_annual,
            hoa_monthly=hoa_monthly,
            sale_price=sale_price,
            monthly_rent=monthly_rent,
            stock_investment_return=stock_investment_return,
            selling_cost_percent=selling_cost_percent
        )
        
        print("\nCUSTOM SCENARIO ANALYSIS:")
        print_results(custom_results)
        
        # Uncomment to visualize:
        # plot_comparison(custom_results)
        
    except ValueError as e:
        print(f"Error with input: {e}")
        print("Using default values instead.")

def analyze_income_investment_scenario(monthly_income, monthly_expenses, holding_period_years, 
                                       stock_investment_return, purchase_scenario_results=None,
                                       expense_breakdown=None):
    """Add expense_breakdown parameter to track detailed expenses"""
    total_months = holding_period_years * 12
    
    # Calculate monthly savings (income minus expenses)
    monthly_savings = monthly_income - monthly_expenses
    total_savings = monthly_savings * total_months
    
    # Calculate future value using dollar-cost averaging formula
    # For monthly investments with compounding, we use a special formula:
    # FV = PMT × ((1 + r)^n - 1) / r
    # Where PMT is the monthly payment, r is the monthly rate, and n is the number of months
    monthly_rate = stock_investment_return / 12
    
    if monthly_rate == 0:
        investment_future_value = total_savings
    else:
        # Formula for regular contributions with compound interest
        investment_future_value = monthly_savings * ((1 + monthly_rate)**total_months - 1) / monthly_rate * (1 + monthly_rate)
    
    investment_gain = investment_future_value - total_savings
    
    # If we have purchase scenario results, include some comparative data
    comparative_data = {}
    if purchase_scenario_results:
        buy = purchase_scenario_results["buy_and_sell"]
        comparative_data = {
            "vs_buying_advantage": investment_future_value - buy["total_benefit"],
            "housing_benefit": buy["total_benefit"]
        }
    
    results = {
        "inputs": {
            "monthly_income": monthly_income,
            "monthly_expenses": monthly_expenses,
            "monthly_savings": monthly_savings,
            "holding_period_years": holding_period_years,
            "stock_investment_return": stock_investment_return,
            "expense_breakdown": expense_breakdown
        },
        "savings": {
            "monthly_amount": monthly_savings,
            "total_invested": total_savings,
            "investment_value": investment_future_value,
            "investment_gain": investment_gain,
            "net_worth_change": investment_future_value
        },
        "comparative": comparative_data
    }
    
    return results

def print_income_investment_results(results, purchase_scenario_results=None):
    """Print analysis results for income investment scenario"""
    inputs = results["inputs"]
    savings = results["savings"]
    comparative = results.get("comparative", {})
    
    print(f"\n{format_color('===== INCOME INVESTMENT ANALYSIS =====', 'bold')}\n")
    
    print(f"{format_color('MONTHLY CASH FLOW:', 'cyan')}")
    print(f"Monthly Income: {format_currency(inputs['monthly_income'], 'green')}")
    
    # Print detailed expense breakdown
    print(f"\n{format_color('MONTHLY EXPENSES BREAKDOWN:', 'cyan')}")
    if inputs.get('expense_breakdown'):
        for category, amount in inputs['expense_breakdown'].items():
            print(f"  {category}: {format_currency(amount, 'red')}")
    print(f"Total Monthly Expenses: {format_currency(inputs['monthly_expenses'], 'red')}")
    print(f"Monthly Savings Available for Investment: {format_currency(inputs['monthly_savings'], 'green')}")
    
    print(f"\n{format_color('INVESTMENT CALCULATION:', 'cyan')}")
    print(f"  Monthly Savings Invested: {format_currency(inputs['monthly_savings'], 'green')}")
    print(f"  Number of Months: {format_color(str(inputs['holding_period_years']*12), 'white')}")
    print(f"  Monthly Return Rate: {format_color(f'{inputs['stock_investment_return']/12*100:.4f}%', 'purple')}")
    print(f"  Formula: PMT × ((1 + r)^n - 1) / r × (1 + r)")
    print(f"    Where:")
    print(f"    PMT = Monthly Savings ({format_currency(inputs['monthly_savings'], 'green')})")
    print(f"    r = Monthly Return Rate ({inputs['stock_investment_return']/12*100:.4f}%)")
    print(f"    n = Number of Months ({inputs['holding_period_years']*12})")
    print(f"Total Amount Invested: {format_currency(savings['total_invested'], 'yellow')}")
    print(f"Investment Future Value: {format_currency(savings['investment_value'], 'green')}")
    print(f"Investment Gain: {format_currency(savings['investment_gain'], 'green')} (Future Value - Total Invested)")
    print(f"Net Worth Change: {format_currency(savings['net_worth_change'], 'green')}")
    
    if purchase_scenario_results:
        buy = purchase_scenario_results["buy_and_sell"]
        print(f"\n{format_color('COMPARISON TO HOUSING INVESTMENT:', 'cyan')}")
        print(f"Income Investment Outcome: {format_currency(savings['net_worth_change'], 'green')}")
        print(f"Housing Investment Outcome: {format_currency(buy['total_benefit'], 'green' if buy['total_benefit'] > 0 else 'red')}")
        advantage = savings['net_worth_change'] - buy['total_benefit']
        print(f"Advantage of Income Investment: {format_currency(advantage, 'green' if advantage > 0 else 'red')}")
        
        if advantage > 0:
            print(f"\n{format_color('CONCLUSION:', 'bold')} {format_color('Investing your income appears more profitable than buying a house', 'green')}")
        else:
            print(f"\n{format_color('CONCLUSION:', 'bold')} {format_color('Buying a house appears more profitable than just investing your income', 'green')}")

def plot_extended_comparison(housing_results, income_results):
    """Plot comparison of housing scenarios and income investment"""
    labels = ['Buy & Sell', 'Rent Only', 'Rent & Invest', 'Income Investment']
    values = [
        housing_results['buy_and_sell']['total_benefit'],
        housing_results['rent_only']['net_worth_change'],
        housing_results['rent_and_invest']['net_worth_change'],
        income_results['savings']['net_worth_change']
    ]
    
    colors = ['green', 'red', 'blue', 'purple']
    
    plt.figure(figsize=(12, 7))
    bars = plt.bar(labels, values, color=colors)
    
    plt.title('Investment Strategy Comparison')
    plt.ylabel('Net Worth Change ($)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add values on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'${int(height):,}',
                 ha='center', va='bottom' if height > 0 else 'top', 
                 color='black' if height > 0 else 'white')
    
    plt.tight_layout()
    plt.show()

def analyze_historical_scenario(initial_capital, monthly_income, purchase_price, down_payment_percent,
                             loan_interest_rate, loan_term_years, holding_period_years,
                             property_tax_annual, hoa_monthly, sale_price, monthly_rent,
                             stock_investment_return):
    """
    Analyze historical scenario with initial capital, comparing house purchase vs full stock investment
    """
    # Calculate house purchase scenario
    down_payment = purchase_price * down_payment_percent
    remaining_capital = initial_capital - down_payment
    
    # Calculate housing investment
    housing_results = analyze_housing_investment(
        purchase_price=purchase_price,
        down_payment_percent=down_payment_percent,
        loan_interest_rate=loan_interest_rate,
        loan_term_years=loan_term_years,
        holding_period_years=holding_period_years,
        property_tax_annual=property_tax_annual,
        hoa_monthly=hoa_monthly,
        sale_price=sale_price,
        monthly_rent=monthly_rent,
        stock_investment_return=stock_investment_return,
        selling_cost_percent=0.07
    )
    
    # Calculate stock returns on remaining capital after down payment
    remaining_stock_future_value = remaining_capital * (1 + stock_investment_return)**holding_period_years
    remaining_stock_gain = remaining_stock_future_value - remaining_capital
    
    # Calculate full stock investment scenario (no house purchase)
    full_stock_future_value = initial_capital * (1 + stock_investment_return)**holding_period_years
    full_stock_gain = full_stock_future_value - initial_capital
    
    # Calculate monthly expenses for both scenarios
    house_expense_breakdown = {
        "Mortgage Payment": housing_results['inputs']['monthly_payment'],
        "Property Tax": property_tax_annual / 12,
        "HOA/Maintenance": hoa_monthly,
        "Utilities": 300,
        "Internet & Phone": 150,
        "Groceries & Food": 800,
        "Transportation": 500,
        "Healthcare & Insurance": 400,
        "Entertainment": 600,
        "Personal Care": 400,
        "Emergency Fund": 500,
        "Miscellaneous": 350
    }
    
    rent_expense_breakdown = {
        "Rent": monthly_rent,
        "Utilities": 300,
        "Internet & Phone": 150,
        "Groceries & Food": 800,
        "Transportation": 500,
        "Healthcare & Insurance": 400,
        "Entertainment": 600,
        "Personal Care": 400,
        "Emergency Fund": 500,
        "Miscellaneous": 350
    }
    
    # Calculate monthly savings and investment for both scenarios
    house_monthly_expenses = sum(house_expense_breakdown.values())
    rent_monthly_expenses = sum(rent_expense_breakdown.values())
    
    # Calculate income investment results for both scenarios
    house_income_results = analyze_income_investment_scenario(
        monthly_income=monthly_income,
        monthly_expenses=house_monthly_expenses,
        holding_period_years=holding_period_years,
        stock_investment_return=stock_investment_return,
        expense_breakdown=house_expense_breakdown
    )
    
    rent_income_results = analyze_income_investment_scenario(
        monthly_income=monthly_income,
        monthly_expenses=rent_monthly_expenses,
        holding_period_years=holding_period_years,
        stock_investment_return=stock_investment_return,
        expense_breakdown=rent_expense_breakdown
    )
    
    return {
        "initial_capital": initial_capital,
        "monthly_income": monthly_income,
        "house_scenario": {
            "housing_results": housing_results,
            "remaining_capital_investment": {
                "amount": remaining_capital,
                "future_value": remaining_stock_future_value,
                "gain": remaining_stock_gain
            },
            "income_investment": house_income_results,
            "total_net_worth": (housing_results['buy_and_sell']['total_benefit'] + 
                              remaining_stock_future_value +
                              house_income_results['savings']['net_worth_change'])
        },
        "full_stock_scenario": {
            "initial_investment": {
                "amount": initial_capital,
                "future_value": full_stock_future_value,
                "gain": full_stock_gain
            },
            "income_investment": rent_income_results,
            "total_net_worth": (full_stock_future_value +
                              rent_income_results['savings']['net_worth_change'])
        }
    }

def print_historical_scenario_results(results):
    """Print analysis results for historical scenario"""
    print(f"\n{format_color('===== HISTORICAL SCENARIO ANALYSIS (5 YEARS AGO) =====', 'bold')}\n")
    
    print(f"{format_color('INITIAL CONDITIONS:', 'cyan')}")
    print(f"Initial Capital: {format_currency(results['initial_capital'], 'green')}")
    print(f"Monthly Income: {format_currency(results['monthly_income'], 'green')}")
    
    house = results['house_scenario']
    stock = results['full_stock_scenario']
    
    print(f"\n{format_color('SCENARIO 1: BUY HOUSE + INVEST REMAINING + SAVE INCOME', 'cyan')}")
    print("House Investment:")
    print(f"  Down Payment: {format_currency(house['housing_results']['inputs']['down_payment'], 'red')}")
    print(f"  House Total Benefit: {format_currency(house['housing_results']['buy_and_sell']['total_benefit'], 'green')}")
    
    print("\nRemaining Capital Investment in S&P 500:")
    print(f"  Amount Invested: {format_currency(house['remaining_capital_investment']['amount'], 'yellow')}")
    print(f"  Future Value: {format_currency(house['remaining_capital_investment']['future_value'], 'green')}")
    print(f"  Investment Gain: {format_currency(house['remaining_capital_investment']['gain'], 'green')}")
    
    print("\nMonthly Income Investment:")
    print(f"  Monthly Expenses: {format_currency(house['income_investment']['inputs']['monthly_expenses'], 'red')}")
    print(f"  Monthly Investment: {format_currency(house['income_investment']['inputs']['monthly_savings'], 'green')}")
    print(f"  Future Value: {format_currency(house['income_investment']['savings']['investment_value'], 'green')}")
    
    print(f"\n{format_color('Total Net Worth (House Scenario):', 'bold')} {format_currency(house['total_net_worth'], 'green')}")
    
    print(f"\n{format_color('SCENARIO 2: INVEST ALL IN S&P 500 + RENT + SAVE INCOME', 'cyan')}")
    print("Initial Capital Investment in S&P 500:")
    print(f"  Amount Invested: {format_currency(stock['initial_investment']['amount'], 'yellow')}")
    print(f"  Future Value: {format_currency(stock['initial_investment']['future_value'], 'green')}")
    print(f"  Investment Gain: {format_currency(stock['initial_investment']['gain'], 'green')}")
    
    print("\nMonthly Income Investment:")
    print(f"  Monthly Expenses: {format_currency(stock['income_investment']['inputs']['monthly_expenses'], 'red')}")
    print(f"  Monthly Investment: {format_currency(stock['income_investment']['inputs']['monthly_savings'], 'green')}")
    print(f"  Future Value: {format_currency(stock['income_investment']['savings']['investment_value'], 'green')}")
    
    print(f"\n{format_color('Total Net Worth (Full Stock Scenario):', 'bold')} {format_currency(stock['total_net_worth'], 'green')}")
    
    advantage = house['total_net_worth'] - stock['total_net_worth']
    better_option = "BUYING A HOUSE" if advantage > 0 else "INVESTING IN S&P 500"
    print(f"\n{format_color('CONCLUSION:', 'bold')}")
    print(f"Advantage of {better_option}: {format_currency(abs(advantage), 'green')}")
    print(f"The better financial decision 5 years ago would have been: {format_color(better_option, 'green')}")

# Example usage with the scenario from the conversation
if __name__ == "__main__":
    purchase_price = 1085000
    down_payment_percent = 0.20
    loan_interest_rate = 0.065
    loan_term_years = 30
    holding_period_years = 10
    property_tax_annual = 13440 # 1.2% of purchase price
    hoa_monthly = 300
    sale_price = 2000000 #1400000
    monthly_rent = 3500
    stock_investment_return = 0.10
    selling_cost_percent = 0.07
    # Original scenario with $3,500 monthly rent
    results_high_rent = analyze_housing_investment(
        purchase_price=purchase_price,
        down_payment_percent=down_payment_percent,
        loan_interest_rate=loan_interest_rate,
        loan_term_years=loan_term_years,
        holding_period_years=holding_period_years,
        property_tax_annual=property_tax_annual,
        hoa_monthly=hoa_monthly,
        sale_price=sale_price,
        monthly_rent=monthly_rent,
        stock_investment_return=stock_investment_return,
        selling_cost_percent=selling_cost_percent
    )
    
    print(f"ANALYSIS WITH ${monthly_rent} MONTHLY RENT")
    print_results(results_high_rent)
    
    # Alternative scenario with $1,300 monthly rent
    monthly_rent = 1300
    results_low_rent = analyze_housing_investment(
        purchase_price=purchase_price,
        down_payment_percent=down_payment_percent,
        loan_interest_rate=loan_interest_rate,
        loan_term_years=loan_term_years,
        holding_period_years=holding_period_years,
        property_tax_annual=property_tax_annual,
        hoa_monthly=hoa_monthly,
        sale_price=sale_price,
        monthly_rent=monthly_rent,
        stock_investment_return=stock_investment_return,
        selling_cost_percent=selling_cost_percent
    )
    
    print("\n\n" + "="*60 + "\n")
    print(f"ANALYSIS WITH ${monthly_rent} MONTHLY RENT")
    print_results(results_low_rent)
    
    # To visualize the comparison, uncomment the following:
    # plot_comparison(results_high_rent)
    # plot_comparison(results_low_rent)
    
    # Income investment scenario with $10,000 monthly income
    print("\n\n" + "="*60 + "\n")
    print(f"{format_color('INCOME INVESTMENT SCENARIO', 'bold')}")
    
    monthly_income = 10000
    
    # Detailed monthly expense breakdown
    expense_breakdown = {
        "Rent": 3500,
        "Utilities (Electric, Gas, Water)": 300,
        "Internet & Phone": 150,
        "Groceries & Food": 800,
        "Transportation (Gas, Insurance, Maintenance)": 500,
        "Healthcare & Insurance": 400,
        "Entertainment & Dining Out": 600,
        "Personal Care & Shopping": 400,
        "Emergency Fund Contribution": 500,
        "Miscellaneous": 350
    }
    
    total_monthly_expenses = sum(expense_breakdown.values())
    
    income_results = analyze_income_investment_scenario(
        monthly_income=monthly_income,
        monthly_expenses=total_monthly_expenses,
        holding_period_years=holding_period_years,
        stock_investment_return=stock_investment_return,
        purchase_scenario_results=results_high_rent,
        expense_breakdown=expense_breakdown
    )
    
    print_income_investment_results(income_results, results_high_rent)
    
    # Alternative with lower rent
    print("\n\n" + "="*60 + "\n")
    print(f"{format_color('INCOME INVESTMENT SCENARIO (WITH LOWER RENT)', 'bold')}")
    
    # Update expense breakdown with lower rent
    expense_breakdown["Rent"] = 1300
    total_monthly_expenses = sum(expense_breakdown.values())
    
    income_results_low_rent = analyze_income_investment_scenario(
        monthly_income=monthly_income,
        monthly_expenses=total_monthly_expenses,
        holding_period_years=holding_period_years,
        stock_investment_return=stock_investment_return,
        purchase_scenario_results=results_low_rent,
        expense_breakdown=expense_breakdown
    )
    
    print_income_investment_results(income_results_low_rent, results_low_rent)
    
    # To visualize the comparison, uncomment the following:
    # plot_extended_comparison(results_high_rent, income_results)
    
    # Historical scenario analysis
    initial_capital = 500000
    monthly_income = 10000
    historical_results = analyze_historical_scenario(
        initial_capital=initial_capital,
        monthly_income=monthly_income,
        purchase_price=purchase_price,
        down_payment_percent=down_payment_percent,
        loan_interest_rate=loan_interest_rate,
        loan_term_years=loan_term_years,
        holding_period_years=holding_period_years,
        property_tax_annual=property_tax_annual,
        hoa_monthly=hoa_monthly,
        sale_price=sale_price,
        monthly_rent=monthly_rent,
        stock_investment_return=stock_investment_return
    )
    
    print_historical_scenario_results(historical_results)
    
   