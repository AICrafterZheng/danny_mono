// Calculate monthly mortgage payment
export const calculateMortgagePayment = (principal, annualRate, years) => {
  const monthlyRate = annualRate / 12;
  const numPayments = years * 12;
  
  if (monthlyRate === 0) {
    return principal / numPayments;
  }
  
  return principal * (monthlyRate * Math.pow(1 + monthlyRate, numPayments)) / 
         (Math.pow(1 + monthlyRate, numPayments) - 1);
};

// Calculate remaining principal after a certain number of months
export const calculateRemainingPrincipal = (principal, annualRate, years, monthsPaid) => {
  if (monthsPaid >= years * 12) {
    return 0;
  }

  const monthlyRate = annualRate / 12;
  const monthlyPayment = calculateMortgagePayment(principal, annualRate, years);

  if (monthlyRate === 0) {
    // For 0% interest rate, it's just linear reduction
    return principal - (monthlyPayment * monthsPaid);
  }

  // The remaining balance formula is:
  // P * (1 + r)^n - PMT * ((1 + r)^n - 1) / r
  // where:
  // P = original principal
  // r = monthly interest rate
  // n = number of months paid
  // PMT = monthly payment
  const remainingBalance = principal * Math.pow(1 + monthlyRate, monthsPaid) -
    monthlyPayment * ((Math.pow(1 + monthlyRate, monthsPaid) - 1) / monthlyRate);

  return remainingBalance;
};

// Main calculation function
export const calculateInvestmentScenarios = ({
  initialCapital,
  monthlyIncome,
  purchasePrice,
  downPaymentPercent,
  loanInterestRate,
  loanTermYears,
  holdingPeriodYears,
  propertyTaxPercent,
  hoaMonthly,
  maintenanceMonthly,
  insuranceMonthly,
  salePrice,
  sellingCostPercent,
  monthlyRent,
  imputedRent,
  stockInvestmentReturnPercent,
  otherMonthlyExpenses,
}) => {
  // Calculate house purchase scenario
  const downPayment = purchasePrice * downPaymentPercent;
  const remainingCapital = initialCapital - downPayment;
  const loanAmount = purchasePrice - downPayment;
  const monthlyPayment = calculateMortgagePayment(loanAmount, loanInterestRate, loanTermYears);
  const totalMonths = holdingPeriodYears * 12;
  
  // Calculate housing costs and benefits
  const annualPropertyTax = purchasePrice * propertyTaxPercent;
  const monthlyPropertyTax = annualPropertyTax / 12;
  const totalMortgagePayments = monthlyPayment * totalMonths;
  const totalPropertyTax = annualPropertyTax * holdingPeriodYears;
  const totalHoa = hoaMonthly * totalMonths;
  const totalMaintenance = maintenanceMonthly * totalMonths;
  const totalInsurance = insuranceMonthly * totalMonths;
  const remainingBalance = calculateRemainingPrincipal(loanAmount, loanInterestRate, loanTermYears, totalMonths);
  const sellingCosts = salePrice * sellingCostPercent;
  
  // Calculate total monthly expenses for both scenarios
  const houseMonthlyExpenses = monthlyPayment + monthlyPropertyTax + hoaMonthly + maintenanceMonthly + insuranceMonthly + otherMonthlyExpenses;
  const rentMonthlyExpenses = monthlyRent + otherMonthlyExpenses;
  
  // House scenario calculations
  const houseCosts = totalMortgagePayments + totalPropertyTax + totalHoa + totalMaintenance + totalInsurance;
  const netFromSale = salePrice - sellingCosts - remainingBalance;
  const houseEquityGain = netFromSale;  // Pure equity without costs
  const rentSavings = monthlyRent * totalMonths;
  const houseTotalBenefit = houseEquityGain + rentSavings - houseCosts;  // Deduct costs here

  // Calculate stock returns on remaining capital
  const remainingStockFutureValue = remainingCapital * Math.pow(1 + stockInvestmentReturnPercent, holdingPeriodYears);
  const remainingStockGain = remainingStockFutureValue - remainingCapital;

  // Calculate full stock investment scenario
  const fullStockFutureValue = initialCapital * Math.pow(1 + stockInvestmentReturnPercent, holdingPeriodYears);
  const fullStockGain = fullStockFutureValue - initialCapital;

  // Calculate income investment returns using monthly contributions
  const calculateFutureValueWithMonthlyContributions = (monthlyContribution, years, annualRate) => {
    const monthlyRate = annualRate / 12;
    const months = years * 12;
    if (monthlyRate === 0) {
      return monthlyContribution * months;
    }
    return monthlyContribution * ((Math.pow(1 + monthlyRate, months) - 1) / monthlyRate) * (1 + monthlyRate);
  };

  return {
    house_scenario: {
      housing_results: {
        inputs: {
          down_payment: downPayment,
          monthly_payment: monthlyPayment,
          annual_property_tax: annualPropertyTax,
          imputed_rent: imputedRent,
        },
        buy_and_sell: {
          total_benefit: houseTotalBenefit,
          equity_gain: houseEquityGain,
          rent_savings: rentSavings,
        },
      },
      remaining_capital_investment: {
        amount: remainingCapital,
        future_value: remainingStockFutureValue,
        gain: remainingStockGain,
      },
      income_investment: {
        inputs: {
          monthly_expenses: houseMonthlyExpenses,
          monthly_savings: monthlyIncome - houseMonthlyExpenses,
        },
        savings: {
          investment_value: calculateFutureValueWithMonthlyContributions(
            monthlyIncome - houseMonthlyExpenses,
            holdingPeriodYears,
            stockInvestmentReturnPercent
          ),
        },
      },
      total_net_worth: houseEquityGain + remainingStockFutureValue + calculateFutureValueWithMonthlyContributions(
        monthlyIncome - houseMonthlyExpenses,
        holdingPeriodYears,
        stockInvestmentReturnPercent
      ),
    },
    full_stock_scenario: {
      initial_investment: {
        amount: initialCapital,
        future_value: fullStockFutureValue,
        gain: fullStockGain,
      },
      income_investment: {
        inputs: {
          monthly_expenses: rentMonthlyExpenses,
          monthly_savings: monthlyIncome - rentMonthlyExpenses,
        },
        savings: {
          investment_value: calculateFutureValueWithMonthlyContributions(
            monthlyIncome - rentMonthlyExpenses,
            holdingPeriodYears,
            stockInvestmentReturnPercent
          ),
        },
      },
      total_net_worth: fullStockFutureValue + calculateFutureValueWithMonthlyContributions(
        monthlyIncome - rentMonthlyExpenses,
        holdingPeriodYears,
        stockInvestmentReturnPercent
      ),
    },
  };
}; 