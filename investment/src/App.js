import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { calculateInvestmentScenarios, calculateMortgagePayment } from './utils/calculations';

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
};

const formatPercent = (value) => {
  return `${(value * 100).toFixed(2)}%`;
};

const CalcDetail = ({ label, value, calculation }) => (
  <div className="mb-2">
    <div className="flex justify-between items-center">
      <span className="font-medium">{label}:</span>
      <span className="text-blue-600">{formatCurrency(value)}</span>
    </div>
    {calculation && (
      <div className="text-sm text-gray-600 mt-1 pl-4">
        {calculation}
      </div>
    )}
  </div>
);

function App() {
  const [inputs, setInputs] = useState({
    initialCapital: 217000,
    monthlyIncome: 10000,
    purchasePrice: 1085000,
    downPaymentPercent: 0.20,
    loanInterestRate: 0.025,
    loanTermYears: 30,
    holdingPeriodYears: 5,
    propertyTaxPercent: 0.01,
    hoaMonthly: 300,
    maintenanceMonthly: 50,
    insuranceMonthly: 20,
    salePrice: 1400000,
    sellingCostPercent: 0.07,
    monthlyRent: 3500,
    imputedRent: 3500,
    stockInvestmentReturnPercent: 0.10,
    otherMonthlyExpenses: 3570,
    capitalGainsTaxPercent: 0.20
  });

  const [results, setResults] = useState(null);
  const [validationError, setValidationError] = useState('');

  // Validation check
  useEffect(() => {
    const requiredDownPayment = inputs.purchasePrice * inputs.downPaymentPercent;
    if (inputs.initialCapital < requiredDownPayment) {
      setValidationError(`Initial capital must be at least ${formatCurrency(requiredDownPayment)} to cover the down payment`);
    } else {
      setValidationError('');
    }
  }, [inputs.purchasePrice, inputs.downPaymentPercent, inputs.initialCapital]);

  const handleInputChange = (key, value) => {
    // Handle empty input
    if (value === '' || value === null || value === undefined) {
      setInputs(prev => ({
        ...prev,
        [key]: ''
      }));
      return;
    }

    // Convert to number and check if it's valid
    const numValue = parseFloat(value);
    if (isNaN(numValue)) return;
    
    if (key === 'purchasePrice' || key === 'downPaymentPercent') {
      const newDownPayment = key === 'purchasePrice' ? 
        numValue * inputs.downPaymentPercent :
        inputs.purchasePrice * numValue;
      
      if (inputs.initialCapital < newDownPayment) {
        setInputs(prev => ({
          ...prev,
          [key]: numValue,
          initialCapital: newDownPayment
        }));
        return;
      }
    }

    setInputs(prev => ({
      ...prev,
      [key]: numValue,
    }));
  };

  const calculateResults = React.useCallback(() => {
    const calculatedResults = calculateInvestmentScenarios(inputs);
    setResults(calculatedResults);
  }, [inputs]);

  useEffect(() => {
    calculateResults();
  }, [calculateResults]);

  const chartData = results ? [
    {
      name: 'House + Stock',
      'House Value': results.house_scenario.housing_results.buy_and_sell.total_benefit,
      'Remaining Capital': results.house_scenario.remaining_capital_investment.future_value,
      'Income Investment': results.house_scenario.income_investment.savings.investment_value,
    },
    {
      name: 'Full Stock',
      'Initial Investment': results.full_stock_scenario.initial_investment.future_value,
      'Income Investment': results.full_stock_scenario.income_investment.savings.investment_value,
    },
  ] : [];

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Investment Analysis Calculator</h1>
        
        {/* Input Form */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Input Parameters</h2>
          {validationError && (
            <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
              {validationError}
            </div>
          )}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {Object.entries(inputs).map(([key, value]) => (
              <div key={key} className="flex flex-col">
                <label className="text-sm font-medium text-gray-700 mb-1">
                  {key === 'stockInvestmentReturnPercent' ? 
                    'Stock Investment Return Percent (e.g. S&P 500)' :
                    key === 'otherMonthlyExpenses' ?
                    'Other Monthly Expenses (e.g. Utilities, Food, Transportation, Entertainment)' :
                    key === 'imputedRent' ?
                    'Imputed Rent (Monthly rental value if you owned the house)' :
                    key === 'monthlyRent' ?
                    'Monthly Rent (What you would pay to rent)' :
                    key
                      .replace(/([A-Z])/g, ' $1')
                      .split(' ')
                      .map(word => word.toLowerCase() === 'hoa' ? 'HOA' : word.charAt(0).toUpperCase() + word.slice(1))
                      .join(' ')
                      .trim()
                  }
                  {(key.includes('Percent') || key === 'loanInterestRate' || key === 'stockInvestmentReturnPercent') && ' (%)'}
                  {key === 'initialCapital' && (
                    <span className="text-xs text-gray-500 ml-1">
                      (min: {formatCurrency(inputs.purchasePrice * inputs.downPaymentPercent)})
                    </span>
                  )}
                </label>
                <input
                  type="number"
                  inputMode="decimal"
                  step={key.includes('Percent') || key === 'loanInterestRate' ? '0.001' : '1'}
                  value={key.includes('Percent') || key === 'loanInterestRate' ? 
                    (value === '' ? '' : Number((value * 100).toFixed(2))) : 
                    (value === '' ? '' : value)
                  }
                  onChange={(e) => {
                    const inputValue = e.target.value;
                    if (inputValue === '') {
                      handleInputChange(key, '');
                      return;
                    }
                    const numValue = key.includes('Percent') || key === 'loanInterestRate' 
                      ? parseFloat(inputValue) / 100 
                      : parseFloat(inputValue);
                    if (!isNaN(numValue)) {
                      handleInputChange(key, numValue);
                    }
                  }}
                  className={`border ${validationError && key === 'initialCapital' ? 'border-red-500' : 'border-gray-300'} rounded-md px-3 py-2`}
                  min={key === 'initialCapital' ? inputs.purchasePrice * inputs.downPaymentPercent : undefined}
                />
              </div>
            ))}
          </div>
        </div>

        {results && (
          <>
            {/* Results */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
              {/* House Scenario */}
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-xl font-semibold mb-4">House + Stock Investment</h2>
                <div className="space-y-6">
                  <div className="pb-4 border-b">
                    <CalcDetail 
                      label="Total Net Worth (After Tax)"
                      value={results.house_scenario.total_net_worth}
                      calculation={`House Equity (${formatCurrency(results.house_scenario.housing_results.buy_and_sell.equity_gain)}) 
                        - House Capital Gains Tax (${formatCurrency(results.house_scenario.housing_results.buy_and_sell.capital_gains_tax)})
                        + Remaining Capital Future Value (${formatCurrency(results.house_scenario.remaining_capital_investment.future_value)})
                        - Stock Capital Gains Tax (${formatCurrency(results.house_scenario.remaining_capital_investment.capital_gains_tax)})
                        + Income Investment Future Value (${formatCurrency(results.house_scenario.income_investment.savings.investment_value)})
                        - Income Investment Capital Gains Tax (${formatCurrency(results.house_scenario.income_investment.savings.capital_gains_tax)})`}
                    />
                  </div>
                  <div>
                    <h3 className="font-medium text-lg mb-3">House Investment</h3>
                    <CalcDetail 
                      label="Down Payment"
                      value={results.house_scenario.housing_results.inputs.down_payment}
                      calculation={`Purchase Price (${formatCurrency(inputs.purchasePrice)}) × Down Payment Rate (${formatPercent(inputs.downPaymentPercent)})`}
                    />
                    <CalcDetail 
                      label="Monthly Mortgage Payment"
                      value={results.house_scenario.housing_results.inputs.monthly_payment}
                      calculation={`Based on: Loan Amount (${formatCurrency(inputs.purchasePrice - results.house_scenario.housing_results.inputs.down_payment)}), Interest Rate (${formatPercent(inputs.loanInterestRate)}), Term (${inputs.loanTermYears} years)`}
                    />
                    <CalcDetail 
                      label="Annual Property Tax"
                      value={results.house_scenario.housing_results.inputs.annual_property_tax}
                      calculation={`Purchase Price (${formatCurrency(inputs.purchasePrice)}) × Tax Rate (${formatPercent(inputs.propertyTaxPercent)})`}
                    />
                    <CalcDetail 
                      label="Equity Gain"
                      value={results.house_scenario.housing_results.buy_and_sell.equity_gain}
                      calculation={`Sale Price (${formatCurrency(inputs.salePrice)}) - Selling Costs (${formatCurrency(inputs.salePrice * inputs.sellingCostPercent)}) - Remaining Loan Balance - Down Payment`}
                    />
                    <CalcDetail 
                      label="Home Sale Exclusion"
                      value={results.house_scenario.housing_results.buy_and_sell.tax_exemption}
                      calculation={`Married couple's tax-free gain (up to $500,000)`}
                    />
                    <CalcDetail 
                      label="Taxable Gain"
                      value={results.house_scenario.housing_results.buy_and_sell.taxable_gain}
                      calculation={`Equity Gain (${formatCurrency(results.house_scenario.housing_results.buy_and_sell.equity_gain)}) - Home Sale Exclusion (${formatCurrency(results.house_scenario.housing_results.buy_and_sell.tax_exemption)})`}
                    />
                    <CalcDetail 
                      label="Capital Gains Tax"
                      value={results.house_scenario.housing_results.buy_and_sell.capital_gains_tax}
                      calculation={`Taxable Gain (${formatCurrency(results.house_scenario.housing_results.buy_and_sell.taxable_gain)}) × Long-term Capital Gains Tax Rate (based on income)`}
                    />
                    <CalcDetail 
                      label="Total Housing Costs"
                      value={
                        calculateMortgagePayment(
                          inputs.purchasePrice * (1 - inputs.downPaymentPercent),
                          inputs.loanInterestRate,
                          inputs.loanTermYears
                        ) * inputs.holdingPeriodYears * 12 +
                        inputs.purchasePrice * inputs.propertyTaxPercent * inputs.holdingPeriodYears +
                        inputs.hoaMonthly * inputs.holdingPeriodYears * 12 +
                        inputs.maintenanceMonthly * inputs.holdingPeriodYears * 12 +
                        inputs.insuranceMonthly * inputs.holdingPeriodYears * 12
                      }
                      calculation={
                        <>
                          • Total Mortgage Payments: {formatCurrency(
                            calculateMortgagePayment(
                              inputs.purchasePrice * (1 - inputs.downPaymentPercent),
                              inputs.loanInterestRate,
                              inputs.loanTermYears
                            ) * inputs.holdingPeriodYears * 12
                          )}
                          <br />• Total Property Tax: {formatCurrency(inputs.purchasePrice * inputs.propertyTaxPercent * inputs.holdingPeriodYears)}
                          <br />• Total HOA: {formatCurrency(inputs.hoaMonthly * inputs.holdingPeriodYears * 12)}
                          <br />• Total Maintenance: {formatCurrency(inputs.maintenanceMonthly * inputs.holdingPeriodYears * 12)}
                          <br />• Total Insurance: {formatCurrency(inputs.insuranceMonthly * inputs.holdingPeriodYears * 12)}
                        </>
                      }
                    />
                    <CalcDetail 
                      label="Total Benefit"
                      value={results.house_scenario.housing_results.buy_and_sell.total_benefit}
                      calculation={
                        <>
                          Equity Gain: {formatCurrency(results.house_scenario.housing_results.buy_and_sell.equity_gain)}
                          <br />+ Imputed Rent Savings ({formatCurrency(results.house_scenario.housing_results.inputs.imputed_rent)} × {inputs.holdingPeriodYears * 12} months = {formatCurrency(results.house_scenario.housing_results.buy_and_sell.rent_savings)})
                          <br />- Total Housing Costs ({formatCurrency(
                            calculateMortgagePayment(
                              inputs.purchasePrice * (1 - inputs.downPaymentPercent),
                              inputs.loanInterestRate,
                              inputs.loanTermYears
                            ) * inputs.holdingPeriodYears * 12 +
                            inputs.purchasePrice * inputs.propertyTaxPercent * inputs.holdingPeriodYears +
                            inputs.hoaMonthly * inputs.holdingPeriodYears * 12 +
                            inputs.maintenanceMonthly * inputs.holdingPeriodYears * 12 +
                            inputs.insuranceMonthly * inputs.holdingPeriodYears * 12
                          )})
                          <br />= Total Benefit: {formatCurrency(results.house_scenario.housing_results.buy_and_sell.total_benefit)}
                        </>
                        
                      }
                    />
                  </div>
                  <div>
                    <h3 className="font-medium text-lg mb-3">Remaining Capital Investment</h3>
                    <CalcDetail 
                      label="Initial Amount"
                      value={results.house_scenario.remaining_capital_investment.amount}
                      calculation={`Initial Capital (${formatCurrency(inputs.initialCapital)}) - Down Payment (${formatCurrency(results.house_scenario.housing_results.inputs.down_payment)})`}
                    />
                    <CalcDetail 
                      label="Investment Gain"
                      value={results.house_scenario.remaining_capital_investment.gain}
                      calculation={`Future Value Before Tax - Initial Amount`}
                    />
                    <CalcDetail 
                      label="Capital Gains Tax Rate"
                      value={results.house_scenario.remaining_capital_investment.tax_rate}
                      calculation={`Long-term capital gains tax rate based on annual income (${formatCurrency(inputs.monthlyIncome * 12)})`}
                    />
                    <CalcDetail 
                      label="Capital Gains Tax"
                      value={results.house_scenario.remaining_capital_investment.capital_gains_tax}
                      calculation={`Investment Gain (${formatCurrency(results.house_scenario.remaining_capital_investment.gain)}) × Tax Rate (${formatPercent(results.house_scenario.remaining_capital_investment.tax_rate)})`}
                    />
                    <CalcDetail 
                      label="Future Value (After Tax)"
                      value={results.house_scenario.remaining_capital_investment.future_value}
                      calculation={`Initial Amount (${formatCurrency(results.house_scenario.remaining_capital_investment.amount)}) × (1 + ${formatPercent(inputs.stockInvestmentReturnPercent)})^${inputs.holdingPeriodYears} years - Capital Gains Tax`}
                    />
                  </div>
                  <div>
                    <h3 className="font-medium text-lg mb-3">Monthly Income Investment</h3>
                    <CalcDetail 
                      label="Monthly Expenses"
                      value={results.house_scenario.income_investment.inputs.monthly_expenses}
                      calculation={
                        <>
                          Housing Related: {formatCurrency(
                            results.house_scenario.housing_results.inputs.monthly_payment +
                            results.house_scenario.housing_results.inputs.annual_property_tax / 12 +
                            inputs.hoaMonthly +
                            inputs.maintenanceMonthly +
                            inputs.insuranceMonthly
                          )}
                          <br />&nbsp;&nbsp;• Mortgage Payment: {formatCurrency(results.house_scenario.housing_results.inputs.monthly_payment)}
                          <br />&nbsp;&nbsp;• Property Tax (Monthly): {formatCurrency(results.house_scenario.housing_results.inputs.annual_property_tax / 12)}
                          <br />&nbsp;&nbsp;• HOA: {formatCurrency(inputs.hoaMonthly)}
                          <br />&nbsp;&nbsp;• Maintenance: {formatCurrency(inputs.maintenanceMonthly)}
                          <br />&nbsp;&nbsp;• House Insurance: {formatCurrency(inputs.insuranceMonthly)}
                          <br />Other Monthly Expenses (e.g. Utilities, Food, Transportation, Entertainment): {formatCurrency(inputs.otherMonthlyExpenses)}
                        </>
                      }
                    />
                    <CalcDetail 
                      label="Monthly Savings"
                      value={inputs.monthlyIncome - (
                        results.house_scenario.housing_results.inputs.monthly_payment +
                        results.house_scenario.housing_results.inputs.annual_property_tax / 12 +
                        inputs.hoaMonthly +
                        inputs.maintenanceMonthly +
                        inputs.insuranceMonthly +
                        inputs.otherMonthlyExpenses
                      )}
                      calculation={`Monthly Income (${formatCurrency(inputs.monthlyIncome)}) - Total Monthly Expenses (${formatCurrency(
                        results.house_scenario.housing_results.inputs.monthly_payment +
                        results.house_scenario.housing_results.inputs.annual_property_tax / 12 +
                        inputs.hoaMonthly +
                        inputs.maintenanceMonthly +
                        inputs.insuranceMonthly +
                        inputs.otherMonthlyExpenses
                      )})`}
                    />
                    <CalcDetail 
                      label="Total Investment Gain"
                      value={results.house_scenario.income_investment.savings.gain}
                      calculation={`Future Value Before Tax - Total Contributions`}
                    />
                    <CalcDetail 
                      label="Capital Gains Tax Rate"
                      value={results.house_scenario.income_investment.savings.tax_rate}
                      calculation={`Long-term capital gains tax rate based on annual income (${formatCurrency(inputs.monthlyIncome * 12)})`}
                    />
                    <CalcDetail 
                      label="Capital Gains Tax"
                      value={results.house_scenario.income_investment.savings.capital_gains_tax}
                      calculation={`Investment Gain (${formatCurrency(results.house_scenario.income_investment.savings.gain)}) × Tax Rate (${formatPercent(results.house_scenario.income_investment.savings.tax_rate)})`}
                    />
                    <CalcDetail 
                      label="Investment Future Value (After Tax)"
                      value={results.house_scenario.income_investment.savings.investment_value}
                      calculation={`Future Value - Capital Gains Tax`}
                    />
                  </div>
                </div>
              </div>

              {/* Full Stock Scenario */}
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-xl font-semibold mb-4">Rent + Stock Investment</h2>
                <div className="space-y-6">
                  <div className="pb-4 border-b">
                    <CalcDetail 
                      label="Total Net Worth (After Tax)"
                      value={results.full_stock_scenario.total_net_worth}
                      calculation={`Initial Investment Future Value (${formatCurrency(results.full_stock_scenario.initial_investment.future_value)})
                        - Initial Investment Capital Gains Tax (${formatCurrency(results.full_stock_scenario.initial_investment.capital_gains_tax)})
                        + Income Investment Future Value (${formatCurrency(results.full_stock_scenario.income_investment.savings.investment_value)})
                        - Income Investment Capital Gains Tax (${formatCurrency(results.full_stock_scenario.income_investment.savings.capital_gains_tax)})`}
                    />
                  </div>
                  <div>
                    <h3 className="font-medium text-lg mb-3">Initial Investment</h3>
                    <CalcDetail 
                      label="Initial Amount"
                      value={results.full_stock_scenario.initial_investment.amount}
                      calculation={`Full Initial Capital (${formatCurrency(inputs.initialCapital)})`}
                    />
                    <CalcDetail 
                      label="Investment Gain"
                      value={results.full_stock_scenario.initial_investment.gain}
                      calculation={`Future Value Before Tax - Initial Amount`}
                    />
                    <CalcDetail 
                      label="Capital Gains Tax Rate"
                      value={results.full_stock_scenario.initial_investment.tax_rate}
                      calculation={`Long-term capital gains tax rate based on annual income (${formatCurrency(inputs.monthlyIncome * 12)})`}
                    />
                    <CalcDetail 
                      label="Capital Gains Tax"
                      value={results.full_stock_scenario.initial_investment.capital_gains_tax}
                      calculation={`Investment Gain (${formatCurrency(results.full_stock_scenario.initial_investment.gain)}) × Tax Rate (${formatPercent(results.full_stock_scenario.initial_investment.tax_rate)})`}
                    />
                    <CalcDetail 
                      label="Future Value (After Tax)"
                      value={results.full_stock_scenario.initial_investment.future_value}
                      calculation={`Initial Amount × (1 + ${formatPercent(inputs.stockInvestmentReturnPercent)})^${inputs.holdingPeriodYears} years - Capital Gains Tax`}
                    />
                  </div>
                  <div>
                    <h3 className="font-medium text-lg mb-3">Monthly Income Investment</h3>
                    <CalcDetail 
                      label="Monthly Expenses"
                      value={results.full_stock_scenario.income_investment.inputs.monthly_expenses}
                      calculation={
                        <>
                          Housing Related (Rent): {formatCurrency(inputs.monthlyRent)}
                          <br />Other Monthly Expenses (e.g. Utilities, Food, Transportation, Entertainment): {formatCurrency(inputs.otherMonthlyExpenses)}
                        </>
                      }
                    />
                    <CalcDetail 
                      label="Monthly Savings"
                      value={results.full_stock_scenario.income_investment.inputs.monthly_savings}
                      calculation={`Monthly Income (${formatCurrency(inputs.monthlyIncome)}) - Monthly Expenses`}
                    />
                    <CalcDetail 
                      label="Total Investment Gain"
                      value={results.full_stock_scenario.income_investment.savings.gain}
                      calculation={`Future Value Before Tax - Total Contributions`}
                    />
                    <CalcDetail 
                      label="Capital Gains Tax Rate"
                      value={results.full_stock_scenario.income_investment.savings.tax_rate}
                      calculation={`Long-term capital gains tax rate based on annual income (${formatCurrency(inputs.monthlyIncome * 12)})`}
                    />
                    <CalcDetail 
                      label="Capital Gains Tax"
                      value={results.full_stock_scenario.income_investment.savings.capital_gains_tax}
                      calculation={`Investment Gain (${formatCurrency(results.full_stock_scenario.income_investment.savings.gain)}) × Tax Rate (${formatPercent(results.full_stock_scenario.income_investment.savings.tax_rate)})`}
                    />
                    <CalcDetail 
                      label="Investment Future Value (After Tax)"
                      value={results.full_stock_scenario.income_investment.savings.investment_value}
                      calculation={`Future Value - Capital Gains Tax`}
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Chart */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold mb-4">Comparison Chart</h2>
              <div className="h-96">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip formatter={(value) => formatCurrency(value)} />
                    <Legend />
                    <Bar dataKey="House Value" fill="#4f46e5" />
                    <Bar dataKey="Remaining Capital" fill="#10b981" />
                    <Bar dataKey="Income Investment" fill="#f59e0b" />
                    <Bar dataKey="Initial Investment" fill="#3b82f6" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;