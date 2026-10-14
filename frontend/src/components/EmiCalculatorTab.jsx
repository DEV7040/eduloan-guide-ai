import React, { useState, useEffect } from 'react';
import { Calculator, Award, Info, ChevronDown, ChevronUp, CheckCircle, TrendingDown } from 'lucide-react';
import { calculateEmi } from '../api';

export default function EmiCalculatorTab() {
  const [principal, setPrincipal] = useState(1500000); // 15 Lakhs
  const [rate, setRate] = useState(9.15); // SBI / BoB average rate
  const [tenureYears, setTenureYears] = useState(10);
  const [moratoriumYears, setMoratoriumYears] = useState(2.5); // 2 yr study + 6m grace
  const [moratoriumTreatment, setMoratoriumTreatment] = useState('capitalize');
  const [isFemale, setIsFemale] = useState(false);
  const [showSchedule, setShowSchedule] = useState(false);

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function updateCalculation() {
      setLoading(true);
      try {
        const data = await calculateEmi({
          principal: Number(principal),
          annual_rate: Number(rate),
          tenure_years: Number(tenureYears),
          moratorium_years: Number(moratoriumYears),
          moratorium_treatment: moratoriumTreatment,
          is_female: isFemale
        });
        setResult(data);
      } catch (err) {
        console.error("Calculation failed", err);
      } finally {
        setLoading(false);
      }
    }
    updateCalculation();
  }, [principal, rate, tenureYears, moratoriumYears, moratoriumTreatment, isFemale]);

  const presetAmounts = [
    { label: '₹4 Lakhs (No Margin)', val: 400000 },
    { label: '₹7.5 Lakhs (CGFSEL Max)', val: 750000 },
    { label: '₹15 Lakhs (Domestic MBA/Engg)', val: 1500000 },
    { label: '₹35 Lakhs (Abroad Unsecured)', val: 3500000 },
    { label: '₹60 Lakhs (US/UK Secured)', val: 6000000 },
  ];

  const formatINR = (val) => {
    if (val === undefined || val === null) return '₹0';
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(val);
  };

  const principalRatio = result
    ? Math.round((result.requested_principal / (result.total_amount_payable || 1)) * 100)
    : 50;

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Calculator size={24} color="var(--primary)" />
          Education Loan EMI & Moratorium Calculator
        </h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem' }}>
          Unlike standard home/car loans, education loans feature a <strong>moratorium period</strong> (course duration + 6-12 months grace). Calculate the exact repayment impact of interest capitalization.
        </p>
      </div>

      <div className="calc-grid">
        {/* Controls Column */}
        <div className="calc-panel">
          {/* Quick Presets */}
          <div style={{ marginBottom: '18px' }}>
            <span style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--text-muted)' }}>QUICK LOAN PRESETS:</span>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginTop: '6px' }}>
              {presetAmounts.map((p, idx) => (
                <button
                  key={idx}
                  onClick={() => setPrincipal(p.val)}
                  className={`prompt-pill ${principal === p.val ? 'active' : ''}`}
                  style={{
                    backgroundColor: principal === p.val ? 'var(--primary-light)' : undefined,
                    borderColor: principal === p.val ? 'var(--primary)' : undefined,
                    color: principal === p.val ? 'var(--primary)' : undefined
                  }}
                >
                  {p.label}
                </button>
              ))}
            </div>
          </div>

          {/* Principal Amount */}
          <div className="calc-group">
            <div className="calc-label-row">
              <span className="calc-label">Loan Principal Amount (₹)</span>
              <span className="calc-val-pill">{formatINR(principal)}</span>
            </div>
            <input
              type="range"
              min="50000"
              max="15000000"
              step="50000"
              value={principal}
              onChange={(e) => setPrincipal(Number(e.target.value))}
              className="calc-slider"
            />
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.74rem', color: 'var(--text-light)', marginTop: '4px' }}>
              <span>₹50,000</span>
              <span>₹75 Lakhs</span>
              <span>₹1.50 Crore</span>
            </div>
          </div>

          {/* Annual Interest Rate */}
          <div className="calc-group">
            <div className="calc-label-row">
              <span className="calc-label">Annual Interest Rate (% p.a.)</span>
              <span className="calc-val-pill">
                {rate}% {isFemale && <span style={{ color: 'var(--accent)', fontSize: '0.75rem' }}>(-0.5% Female Concession)</span>}
              </span>
            </div>
            <input
              type="range"
              min="7.5"
              max="15.0"
              step="0.05"
              value={rate}
              onChange={(e) => setRate(Number(e.target.value))}
              className="calc-slider"
            />
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.74rem', color: 'var(--text-light)', marginTop: '4px' }}>
              <span>7.5% (Premier IIT/IIM)</span>
              <span>9.5% (Public Bank avg)</span>
              <span>15.0% (NBFC Unsecured)</span>
            </div>
          </div>

          {/* Repayment Tenure */}
          <div className="calc-group">
            <div className="calc-label-row">
              <span className="calc-label">Repayment Tenure (After Moratorium)</span>
              <span className="calc-val-pill">{tenureYears} Years ({tenureYears * 12} Months)</span>
            </div>
            <input
              type="range"
              min="1"
              max="15"
              step="1"
              value={tenureYears}
              onChange={(e) => setTenureYears(Number(e.target.value))}
              className="calc-slider"
            />
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.74rem', color: 'var(--text-light)', marginTop: '4px' }}>
              <span>1 Year</span>
              <span>7 Years</span>
              <span>15 Years (Max)</span>
            </div>
          </div>

          {/* Moratorium Duration */}
          <div className="calc-group">
            <div className="calc-label-row">
              <span className="calc-label">Moratorium Period (Course + Grace Period)</span>
              <span className="calc-val-pill">{moratoriumYears} Years</span>
            </div>
            <input
              type="range"
              min="0.5"
              max="5.0"
              step="0.5"
              value={moratoriumYears}
              onChange={(e) => setMoratoriumYears(Number(e.target.value))}
              className="calc-slider"
            />
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.74rem', color: 'var(--text-light)', marginTop: '4px' }}>
              <span>6 Months</span>
              <span>2.5 Yrs (BTech/Masters)</span>
              <span>5 Years (MBBS)</span>
            </div>
          </div>

          {/* Moratorium Treatment Options */}
          <div className="calc-group">
            <span className="calc-label">Moratorium Interest Treatment</span>
            <div className="calc-toggle-btn-group">
              <div
                className={`toggle-option ${moratoriumTreatment === 'capitalize' ? 'active' : ''}`}
                onClick={() => setMoratoriumTreatment('capitalize')}
              >
                <strong>Capitalize to Principal</strong>
                <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                  No payment during study; interest adds to principal
                </div>
              </div>
              <div
                className={`toggle-option ${moratoriumTreatment === 'pay_simple_interest' ? 'active' : ''}`}
                onClick={() => setMoratoriumTreatment('pay_simple_interest')}
              >
                <strong>Pay Simple Interest Monthly</strong>
                <div style={{ fontSize: '0.74rem', color: 'var(--accent)', marginTop: '2px' }}>
                  Earns ~1% interest discount from banks!
                </div>
              </div>
            </div>
          </div>

          {/* Girl Child Concession Checkbox */}
          <div style={{ marginTop: '16px', padding: '12px', background: 'var(--accent-light)', border: '1px solid var(--accent-border)', borderRadius: 'var(--radius-sm)' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontSize: '0.86rem', fontWeight: 600, color: 'var(--accent)' }}>
              <input
                type="checkbox"
                checked={isFemale}
                onChange={(e) => setIsFemale(e.target.checked)}
                style={{ width: '16px', height: '16px' }}
              />
              <span>👩‍🎓 Apply Girl Student 0.50% Interest Concession (SBI, BoB, Canara, PNB)</span>
            </label>
          </div>
        </div>

        {/* Results Column */}
        <div className="calc-panel">
          {result && (
            <>
              {/* Highlight EMI Card */}
              <div className="highlight-metric-card">
                <div className="label">Estimated Monthly Repayment (EMI)</div>
                <div className="amount">{formatINR(result.monthly_emi)}</div>
                <div style={{ fontSize: '0.82rem', opacity: 0.9 }}>
                  Payable for {result.tenure_months} months starting after {result.moratorium_years} years
                </div>
              </div>

              {/* Sub-metrics Grid */}
              <div className="metric-subgrid">
                <div className="submetric-box">
                  <div className="label">Original Principal</div>
                  <div className="val">{formatINR(result.requested_principal)}</div>
                </div>
                <div className="submetric-box">
                  <div className="label">Moratorium Accrued Interest</div>
                  <div className="val" style={{ color: 'var(--warning)' }}>{formatINR(result.moratorium_interest_accrued)}</div>
                </div>
                <div className="submetric-box">
                  <div className="label">Total Interest Paid</div>
                  <div className="val" style={{ color: 'var(--danger)' }}>{formatINR(result.total_interest_paid)}</div>
                </div>
                <div className="submetric-box">
                  <div className="label">Total Repayment Outflow</div>
                  <div className="val" style={{ color: 'var(--primary)' }}>{formatINR(result.total_amount_payable)}</div>
                </div>
              </div>

              {/* Ratio Visualizer */}
              <div style={{ marginBottom: '20px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', fontWeight: 700, marginBottom: '6px' }}>
                  <span>Principal: {principalRatio}%</span>
                  <span>Total Interest: {100 - principalRatio}%</span>
                </div>
                <div style={{ height: '10px', background: 'var(--border)', borderRadius: '9999px', overflow: 'hidden', display: 'flex' }}>
                  <div style={{ width: `${principalRatio}%`, background: 'var(--primary)' }}></div>
                  <div style={{ width: `${100 - principalRatio}%`, background: 'var(--warning)' }}></div>
                </div>
              </div>

              {/* Potential Savings Banner */}
              {result.estimated_savings_with_prompt_service > 0 && (
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '12px', background: 'var(--accent-light)', border: '1px solid var(--accent-border)', borderRadius: 'var(--radius-sm)', marginBottom: '20px' }}>
                  <TrendingDown size={22} color="var(--accent)" />
                  <div style={{ fontSize: '0.82rem' }}>
                    <strong style={{ color: 'var(--accent)' }}>Prompt Payment Tip:</strong> Paying simple interest during college can save approx{' '}
                    <strong>{formatINR(result.estimated_savings_with_prompt_service)}</strong> over the loan lifetime!
                  </div>
                </div>
              )}

              {/* Tax Deduction Benefit Note */}
              <div style={{ display: 'flex', alignItems: 'flex-start', gap: '8px', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '16px' }}>
                <Info size={16} color="var(--primary)" style={{ flexShrink: 0, marginTop: '2px' }} />
                <span>
                  <strong>Section 80E Tax Deduction:</strong> The entire interest portion ({formatINR(result.total_interest_paid)}) is eligible for income tax deduction without any upper limit for up to 8 continuous financial years.
                </span>
              </div>

              {/* Collapsible Amortization Schedule */}
              <button
                onClick={() => setShowSchedule(!showSchedule)}
                className="btn-secondary"
                style={{ width: '100%', justifyContent: 'space-between' }}
              >
                <span>Year-by-Year Repayment Schedule</span>
                {showSchedule ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
              </button>

              {showSchedule && result.yearly_schedule && (
                <div style={{ marginTop: '12px', maxHeight: '240px', overflowY: 'auto', border: '1px solid var(--border)', borderRadius: 'var(--radius-sm)' }}>
                  <table style={{ width: '100%', fontSize: '0.78rem', borderCollapse: 'collapse' }}>
                    <thead style={{ background: 'var(--bg-card-subtle)', position: 'sticky', top: 0 }}>
                      <tr>
                        <th style={{ padding: '6px 10px', textAlign: 'left' }}>Year</th>
                        <th style={{ padding: '6px 10px', textAlign: 'right' }}>Principal Paid</th>
                        <th style={{ padding: '6px 10px', textAlign: 'right' }}>Interest Paid</th>
                        <th style={{ padding: '6px 10px', textAlign: 'right' }}>Ending Balance</th>
                      </tr>
                    </thead>
                    <tbody>
                      {result.yearly_schedule.map((item) => (
                        <tr key={item.year} style={{ borderBottom: '1px solid var(--border)' }}>
                          <td style={{ padding: '6px 10px', fontWeight: 600 }}>Year {item.year}</td>
                          <td style={{ padding: '6px 10px', textAlign: 'right' }}>{formatINR(item.principal_paid)}</td>
                          <td style={{ padding: '6px 10px', textAlign: 'right', color: 'var(--warning)' }}>{formatINR(item.interest_paid)}</td>
                          <td style={{ padding: '6px 10px', textAlign: 'right', fontWeight: 700 }}>{formatINR(item.ending_balance)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
