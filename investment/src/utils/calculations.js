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

// Calculate long-term capital gains tax based on 2024 tax brackets
const calculateLongTermCapitalGainsTax = (gain, taxableIncome) => {
  // 2024 Long-term capital gains tax brackets (married filing jointly)
  const BRACKETS = {
    ZERO_PERCENT_LIMIT: 94050,      // 0% for income up to $94,050
    FIFTEEN_PERCENT_LIMIT: 583750,  // 15% for income $94,051-$583,750
    // 20% for income above $583,750
  };

  if (taxableIncome <= BRACKETS.ZERO_PERCENT_LIMIT) {
    return 0;
  } else if (taxableIncome <= BRACKETS.FIFTEEN_PERCENT_LIMIT) {
    return gain * 0.15;
  } else {
    return gain * 0.20;
  }
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
  otherMonthlyExpenses
}) => {
  // Calculate annual taxable income (rough estimate for tax bracket determination)
  const annualTaxableIncome = monthlyIncome * 12;

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
  
  // House scenario calculations with $500,000 exclusion for married couples
  const houseCosts = totalMortgagePayments + totalPropertyTax + totalHoa + totalMaintenance + totalInsurance;
  const netFromSale = salePrice - sellingCosts - remainingBalance;
  const houseEquityGain = netFromSale - downPayment;  // Total gain before exclusion
  const taxableHouseGain = Math.max(0, houseEquityGain - 500000);  // Apply $500,000 exclusion
  const houseCapitalGainsTax = calculateLongTermCapitalGainsTax(taxableHouseGain, annualTaxableIncome);
  const rentSavings = imputedRent * totalMonths;
  const houseTotalBenefit = netFromSale + rentSavings - houseCosts - houseCapitalGainsTax;

  // Calculate stock returns on remaining capital
  const remainingStockFutureValue = remainingCapital * Math.pow(1 + stockInvestmentReturnPercent, holdingPeriodYears);
  const remainingStockGain = remainingStockFutureValue - remainingCapital;
  const remainingStockCapitalGainsTax = calculateLongTermCapitalGainsTax(remainingStockGain, annualTaxableIncome);

  // Calculate full stock investment scenario
  const fullStockFutureValue = initialCapital * Math.pow(1 + stockInvestmentReturnPercent, holdingPeriodYears);
  const fullStockGain = fullStockFutureValue - initialCapital;
  const fullStockCapitalGainsTax = calculateLongTermCapitalGainsTax(fullStockGain, annualTaxableIncome);

  // Calculate income investment returns using monthly contributions
  const calculateFutureValueWithMonthlyContributions = (monthlyContribution, years, annualRate) => {
    const monthlyRate = annualRate / 12;
    const months = years * 12;
    if (monthlyRate === 0) {
      return monthlyContribution * months;
    }
    return monthlyContribution * ((Math.pow(1 + monthlyRate, months) - 1) / monthlyRate) * (1 + monthlyRate);
  };

  // Calculate income investment values and their capital gains taxes
  const houseScenarioIncomeFV = calculateFutureValueWithMonthlyContributions(
    monthlyIncome - houseMonthlyExpenses,
    holdingPeriodYears,
    stockInvestmentReturnPercent
  );
  const houseScenarioIncomeGain = houseScenarioIncomeFV - ((monthlyIncome - houseMonthlyExpenses) * totalMonths);
  const houseScenarioIncomeCapitalGainsTax = calculateLongTermCapitalGainsTax(houseScenarioIncomeGain, annualTaxableIncome);

  const fullStockScenarioIncomeFV = calculateFutureValueWithMonthlyContributions(
    monthlyIncome - rentMonthlyExpenses,
    holdingPeriodYears,
    stockInvestmentReturnPercent
  );
  const fullStockScenarioIncomeGain = fullStockScenarioIncomeFV - ((monthlyIncome - rentMonthlyExpenses) * totalMonths);
  const fullStockScenarioIncomeCapitalGainsTax = calculateLongTermCapitalGainsTax(fullStockScenarioIncomeGain, annualTaxableIncome);

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
          taxable_gain: taxableHouseGain,
          capital_gains_tax: houseCapitalGainsTax,
          tax_exemption: Math.min(500000, houseEquityGain),
          rent_savings: rentSavings,
        },
      },
      remaining_capital_investment: {
        amount: remainingCapital,
        future_value: remainingStockFutureValue - remainingStockCapitalGainsTax,
        gain: remainingStockGain,
        capital_gains_tax: remainingStockCapitalGainsTax,
        tax_rate: annualTaxableIncome > 583750 ? 0.20 : (annualTaxableIncome > 94050 ? 0.15 : 0)
      },
      income_investment: {
        inputs: {
          monthly_expenses: houseMonthlyExpenses,
          monthly_savings: monthlyIncome - houseMonthlyExpenses,
        },
        savings: {
          investment_value: houseScenarioIncomeFV - houseScenarioIncomeCapitalGainsTax,
          gain: houseScenarioIncomeGain,
          capital_gains_tax: houseScenarioIncomeCapitalGainsTax,
          tax_rate: annualTaxableIncome > 583750 ? 0.20 : (annualTaxableIncome > 94050 ? 0.15 : 0)
        },
      },
      total_net_worth: houseTotalBenefit + 
                      (remainingStockFutureValue - remainingStockCapitalGainsTax) + 
                      (houseScenarioIncomeFV - houseScenarioIncomeCapitalGainsTax)
    },
    full_stock_scenario: {
      initial_investment: {
        amount: initialCapital,
        future_value: fullStockFutureValue - fullStockCapitalGainsTax,
        gain: fullStockGain,
        capital_gains_tax: fullStockCapitalGainsTax,
        tax_rate: annualTaxableIncome > 583750 ? 0.20 : (annualTaxableIncome > 94050 ? 0.15 : 0)
      },
      income_investment: {
        inputs: {
          monthly_expenses: rentMonthlyExpenses,
          monthly_savings: monthlyIncome - rentMonthlyExpenses,
        },
        savings: {
          investment_value: fullStockScenarioIncomeFV - fullStockScenarioIncomeCapitalGainsTax,
          gain: fullStockScenarioIncomeGain,
          capital_gains_tax: fullStockScenarioIncomeCapitalGainsTax,
          tax_rate: annualTaxableIncome > 583750 ? 0.20 : (annualTaxableIncome > 94050 ? 0.15 : 0)
        },
      },
      total_net_worth: (fullStockFutureValue - fullStockCapitalGainsTax) + 
                      (fullStockScenarioIncomeFV - fullStockScenarioIncomeCapitalGainsTax)
    },
  };
}; 