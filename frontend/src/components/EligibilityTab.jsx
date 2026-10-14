import React, { useState, useEffect } from 'react';
import { CheckCircle2, AlertTriangle, ShieldCheck, ArrowRight, ExternalLink, Award, Sparkles, Building2 } from 'lucide-react';
import { checkEligibility } from '../api';

export default function EligibilityTab({ onNavigateTab }) {
  const [destination, setDestination] = useState('india');
  const [instituteTier, setInstituteTier] = useState('tier1_iim_iit');
  const [amount, setAmount] = useState(1500000);
  const [familyIncome, setFamilyIncome] = useState(600000);
  const [cibilScore, setCibilScore] = useState(740);
  const [hasCollateral, setHasCollateral] = useState(false);
  const [hasAdmission, setHasAdmission] = useState(true);
  const [isFemale, setIsFemale] = useState(false);

  const [evaluation, setEvaluation] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function evaluate() {
      setLoading(true);
      try {
        const res = await checkEligibility({
          destination,
          amount: Number(amount),
          family_income: Number(familyIncome),
          institute_tier: instituteTier,
          cibil_score: Number(cibilScore),
          has_collateral: hasCollateral,
          collateral_value: hasCollateral ? amount : 0,
          has_admission: hasAdmission,
          is_female: isFemale
        });
        setEvaluation(res);
      } catch (e) {
        console.error("Eligibility check failed", e);
      } finally {
        setLoading(false);
      }
    }
    evaluate();
  }, [destination, instituteTier, amount, familyIncome, cibilScore, hasCollateral, hasAdmission, isFemale]);

  const formatINR = (val) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(val || 0);
  };

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <ShieldCheck size={24} color="var(--accent)" />
          Preliminary Loan Eligibility & Subsidy Checker
        </h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem' }}>
          Assess your approval probability against standard RBI and Indian Banks' Association (IBA) lending criteria before applying.
        </p>
      </div>

      <div className="calc-grid">
        {/* Form Panel */}
        <div className="calc-panel">
          <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '16px', color: 'var(--primary)' }}>
            1. Student & Course Profile
          </h3>

          {/* Destination */}
          <div className="calc-group">
            <span className="calc-label">Study Destination</span>
            <div className="calc-toggle-btn-group">
              <div
                className={`toggle-option ${destination === 'india' ? 'active' : ''}`}
                onClick={() => {
                  setDestination('india');
                  setInstituteTier('tier1_iim_iit');
                }}
              >
                🇮🇳 Studies in India
              </div>
              <div
                className={`toggle-option ${destination === 'abroad' ? 'active' : ''}`}
                onClick={() => {
                  setDestination('abroad');
                  setInstituteTier('abroad_top200');
                }}
              >
                🌍 Studies Abroad (Overseas)
              </div>
            </div>
          </div>

          {/* College Tier */}
          <div className="calc-group">
            <span className="calc-label">Institution Category / Tier</span>
            <select
              value={instituteTier}
              onChange={(e) => setInstituteTier(e.target.value)}
              style={{
                width: '100%',
                padding: '10px 12px',
                borderRadius: 'var(--radius-sm)',
                border: '1px solid var(--border)',
                fontFamily: 'inherit',
                fontSize: '0.86rem',
                marginTop: '6px'
              }}
            >
              {destination === 'india' ? (
                <>
                  <option value="tier1_iim_iit">Tier 1: IITs, IIMs, NITs, AIIMS, BITS (SBI Scholar List AA/A)</option>
                  <option value="tier2_accredited">Tier 2: UGC / AICTE / NBA Accredited University / College</option>
                  <option value="tier3_other">Tier 3: Recognized Private College / State University</option>
                </>
              ) : (
                <>
                  <option value="abroad_top200">Global Top 200 QS / THE Ranked Universities (Ivy League, Russell Group)</option>
                  <option value="abroad_general">Accredited Global University (US, UK, Canada, Germany, Australia)</option>
                </>
              )}
            </select>
          </div>

          {/* Loan Amount */}
          <div className="calc-group">
            <div className="calc-label-row">
              <span className="calc-label">Required Loan Amount</span>
              <span className="calc-val-pill">{formatINR(amount)}</span>
            </div>
            <input
              type="range"
              min="100000"
              max="15000000"
              step="50000"
              value={amount}
              onChange={(e) => setAmount(Number(e.target.value))}
              className="calc-slider"
            />
          </div>

          <h3 style={{ fontSize: '1rem', fontWeight: 700, margin: '20px 0 16px', color: 'var(--primary)' }}>
            2. Financial & Co-Applicant Background
          </h3>

          {/* Annual Family Income */}
          <div className="calc-group">
            <div className="calc-label-row">
              <span className="calc-label">Annual Gross Family Income</span>
              <span className="calc-val-pill">{formatINR(familyIncome)}</span>
            </div>
            <input
              type="range"
              min="100000"
              max="2500000"
              step="50000"
              value={familyIncome}
              onChange={(e) => setFamilyIncome(Number(e.target.value))}
              className="calc-slider"
            />
            {familyIncome <= 450000 && destination === 'india' && (
              <div style={{ fontSize: '0.75rem', color: 'var(--accent)', fontWeight: 600, marginTop: '4px' }}>
                🎉 Eligible for 100% Central Sector Interest Subsidy (CSIS) during study period!
              </div>
            )}
          </div>

          {/* Co-applicant CIBIL */}
          <div className="calc-group">
            <div className="calc-label-row">
              <span className="calc-label">Co-Applicant CIBIL Score</span>
              <span className="calc-val-pill">{cibilScore}</span>
            </div>
            <input
              type="range"
              min="600"
              max="850"
              step="5"
              value={cibilScore}
              onChange={(e) => setCibilScore(Number(e.target.value))}
              className="calc-slider"
            />
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.74rem', color: 'var(--text-light)', marginTop: '4px' }}>
              <span>600 (Needs co-guarantor)</span>
              <span>720 (Standard Public Bank)</span>
              <span>850 (Prime Tier)</span>
            </div>
          </div>

          {/* Toggles */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginTop: '16px' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.86rem', cursor: 'pointer' }}>
              <input
                type="checkbox"
                checked={hasCollateral}
                onChange={(e) => setHasCollateral(e.target.checked)}
                style={{ width: '16px', height: '16px' }}
              />
              <span>Can provide tangible collateral (House / Flat / Land / Fixed Deposit)</span>
            </label>

            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.86rem', cursor: 'pointer' }}>
              <input
                type="checkbox"
                checked={hasAdmission}
                onChange={(e) => setHasAdmission(e.target.checked)}
                style={{ width: '16px', height: '16px' }}
              />
              <span>Already received confirmed admission offer letter</span>
            </label>

            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.86rem', cursor: 'pointer' }}>
              <input
                type="checkbox"
                checked={isFemale}
                onChange={(e) => setIsFemale(e.target.checked)}
                style={{ width: '16px', height: '16px' }}
              />
              <span>Applicant is Female (qualifies for 0.50% interest concession)</span>
            </label>
          </div>
        </div>

        {/* Results Panel */}
        <div className="calc-panel">
          {evaluation && (
            <>
              {/* Score Meter */}
              <div style={{
                background: evaluation.eligibility_score >= 75 ? 'linear-gradient(135deg, #059669, #10b981)' : 'linear-gradient(135deg, #d97706, #f59e0b)',
                color: '#ffffff',
                padding: '24px',
                borderRadius: 'var(--radius-lg)',
                marginBottom: '20px',
                boxShadow: '0 8px 16px rgba(0,0,0,0.1)'
              }}>
                <div style={{ fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.05em', opacity: 0.9 }}>
                  Preliminary Approval Probability
                </div>
                <div style={{ display: 'flex', alignItems: 'baseline', gap: '10px', margin: '8px 0' }}>
                  <span style={{ fontSize: '2.5rem', fontWeight: 800 }}>{evaluation.eligibility_score}%</span>
                  <span style={{ fontSize: '1rem', fontWeight: 600 }}>{evaluation.status}</span>
                </div>
                <div style={{ fontSize: '0.82rem', opacity: 0.95 }}>
                  {evaluation.collateral_free_eligible
                    ? "✨ 100% Eligible for Collateral-Free funding under CGFSEL / Premier Institute criteria!"
                    : "Tangible collateral or co-borrower income strengthening required."}
                </div>
              </div>

              {/* Margin Money & Terms */}
              <div className="metric-subgrid">
                <div className="submetric-box">
                  <div className="label">Margin Money Required</div>
                  <div className="val">{evaluation.margin_money_percentage}%</div>
                  <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                    Student share: {formatINR(evaluation.margin_money_amount)}
                  </div>
                </div>
                <div className="submetric-box">
                  <div className="label">Collateral Requirement</div>
                  <div className="val" style={{ color: evaluation.collateral_free_eligible ? 'var(--accent)' : 'var(--warning)', fontSize: '0.98rem' }}>
                    {evaluation.collateral_free_eligible ? "Zero Collateral" : "Tangible Security"}
                  </div>
                  <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                    {evaluation.collateral_free_eligible ? "Covered by CGFSEL guarantee" : "Property mortgage or FD lien"}
                  </div>
                </div>
              </div>

              {/* Strengths & Reasons */}
              <div style={{ marginBottom: '16px' }}>
                <span style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-main)', display: 'block', marginBottom: '8px' }}>
                  Profile Strengths & Eligibility Insights:
                </span>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                  {evaluation.strengths.map((str, i) => (
                    <div key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: '8px', fontSize: '0.8rem', color: 'var(--text-main)' }}>
                      <CheckCircle2 size={16} color="var(--accent)" style={{ flexShrink: 0, marginTop: '2px' }} />
                      <span>{str}</span>
                    </div>
                  ))}
                  {evaluation.attention_points.map((pt, i) => (
                    <div key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: '8px', fontSize: '0.8rem', color: 'var(--warning)' }}>
                      <AlertTriangle size={16} color="var(--warning)" style={{ flexShrink: 0, marginTop: '2px' }} />
                      <span>{pt}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Applicable Subsidies */}
              {evaluation.applicable_subsidies && evaluation.applicable_subsidies.length > 0 && (
                <div style={{ padding: '14px', background: 'var(--accent-light)', border: '1px solid var(--accent-border)', borderRadius: 'var(--radius-md)', marginBottom: '18px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.84rem', fontWeight: 700, color: 'var(--accent)', marginBottom: '6px' }}>
                    <Award size={16} />
                    <span>Eligible Government Subsidies & Benefits:</span>
                  </div>
                  {evaluation.applicable_subsidies.map((sub, i) => (
                    <div key={i} style={{ fontSize: '0.78rem', marginBottom: '4px' }}>
                      <strong>{sub.name}:</strong> {sub.benefit} ({sub.authority})
                    </div>
                  ))}
                </div>
              )}

              {/* Top Matching Banks */}
              <div>
                <span style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-main)', display: 'block', marginBottom: '10px' }}>
                  Top Recommended Banks for Your Profile:
                </span>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  {evaluation.matching_banks.slice(0, 3).map((b) => (
                    <div
                      key={b.id}
                      style={{
                        padding: '10px 14px',
                        border: '1px solid var(--border)',
                        borderRadius: 'var(--radius-sm)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        background: '#ffffff'
                      }}
                    >
                      <div>
                        <div style={{ fontWeight: 700, fontSize: '0.86rem' }}>{b.bank_name}</div>
                        <div style={{ fontSize: '0.76rem', color: 'var(--text-muted)' }}>{b.product_name} • Rate: <strong>{b.indicative_rate}</strong></div>
                      </div>
                      <a
                        href={b.official_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn-secondary"
                        style={{ padding: '5px 10px', fontSize: '0.76rem' }}
                      >
                        <span>Apply</span>
                        <ExternalLink size={12} />
                      </a>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
