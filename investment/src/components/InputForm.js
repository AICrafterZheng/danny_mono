  <div className="input-section">
    <div className="input-group">
      <label>HOA Monthly</label>
      <CurrencyInput
        value={inputs.hoaMonthly}
        onValueChange={(value) => handleInputChange('hoaMonthly', value)}
        prefix="$"
        decimalsLimit={2}
      />
    </div>

    <div className="input-group">
      <label>Maintenance Monthly</label>
      <CurrencyInput
        value={inputs.maintenanceMonthly}
        onValueChange={(value) => handleInputChange('maintenanceMonthly', value)}
        prefix="$"
        decimalsLimit={2}
      />
    </div>

    <div className="input-group">
      <label>Insurance Monthly</label>
      <CurrencyInput
        value={inputs.insuranceMonthly}
        onValueChange={(value) => handleInputChange('insuranceMonthly', value)}
        prefix="$"
        decimalsLimit={2}
      />
    </div>

    <div className="input-group">
      <label>Monthly Rent (Full Stock Scenario)</label>
      <CurrencyInput
        value={inputs.monthlyRent}
        onValueChange={(value) => handleInputChange('monthlyRent', value)}
        prefix="$"
        decimalsLimit={2}
      />
    </div>
  </div> 