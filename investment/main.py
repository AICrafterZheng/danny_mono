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


# Example usage with the scenario from the conversation
if __name__ == "__main__":
    purchase_price = 1085000
    down_payment_percent = 0.30
    loan_interest_rate = 0.025
    loan_term_years = 30
    holding_period_years = 5
    property_tax_annual = 13440 # 1.2% of purchase price
    hoa_monthly = 300
    sale_price = 1400000
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
    
   