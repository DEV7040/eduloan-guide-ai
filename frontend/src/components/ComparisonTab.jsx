import React, { useState, useEffect } from 'react';
import { Scale, ExternalLink, Check, ShieldCheck, Filter } from 'lucide-react';
import { fetchLoans } from '../api';

export default function ComparisonTab() {
  const [loans, setLoans] = useState([]);
  const [filterDest, setFilterDest] = useState('all');
  const [filterCollateral, setFilterCollateral] = useState(false);
  const [loading, setLoading] = useState(false);
  const [selectedIds, setSelectedIds] = useState(['sbi-student-loan', 'hdfc-credila']);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const filters = {};
        if (filterDest !== 'all') filters.destination = filterDest;
        if (filterCollateral) filters.collateral_free = true;
        const res = await fetchLoans(filters);
        setLoans(res.loans || []);
      } catch (e) {
        console.error("Failed to load loans", e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [filterDest, filterCollateral]);

  const toggleSelect = (id) => {
    if (selectedIds.includes(id)) {
      if (selectedIds.length > 1) {
        setSelectedIds(selectedIds.filter(x => x !== id));
      }
    } else {
      if (selectedIds.length >= 3) {
        setSelectedIds([selectedIds[1], selectedIds[2], id]);
      } else {
        setSelectedIds([...selectedIds, id]);
      }
    }
  };

  const selectedLoans = loans.filter(l => selectedIds.includes(l.id));

  return (
    <div>
      <div style={{ marginBottom: '20px' }}>
        <h2 style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Scale size={24} color="var(--primary)" />
          Education Loan Comparison & Finder
        </h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem' }}>
          Compare interest rates, collateral thresholds, margin money, and girl student concessions across verified Indian banks.
        </p>
      </div>

      {/* Filter Row */}
      <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', justifyContent: 'space-between', gap: '12px', background: '#ffffff', padding: '14px 20px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border)', marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
          <span style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '4px' }}>
            <Filter size={14} /> Filter:
          </span>
          <button
            className={`prompt-pill ${filterDest === 'all' ? 'active' : ''}`}
            onClick={() => setFilterDest('all')}
          >
            All Loans
          </button>
          <button
            className={`prompt-pill ${filterDest === 'india' ? 'active' : ''}`}
            onClick={() => setFilterDest('india')}
          >
            🇮🇳 India Studies
          </button>
          <button
            className={`prompt-pill ${filterDest === 'abroad' ? 'active' : ''}`}
            onClick={() => setFilterDest('abroad')}
          >
            🌍 Overseas (Abroad)
          </button>
          <button
            className={`prompt-pill ${filterCollateral ? 'active' : ''}`}
            onClick={() => setFilterCollateral(!filterCollateral)}
            style={{ borderColor: filterCollateral ? 'var(--accent)' : undefined, color: filterCollateral ? 'var(--accent)' : undefined }}
          >
            🛡️ Collateral-Free Eligible Only
          </button>
        </div>

        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
          Showing <strong>{loans.length}</strong> verified lenders
        </div>
      </div>

      {/* Side-by-Side Head to Head Matrix */}
      {selectedLoans.length >= 2 && (
        <div style={{ background: '#ffffff', border: '2px solid var(--primary-border)', borderRadius: 'var(--radius-lg)', padding: '20px', marginBottom: '32px', boxShadow: 'var(--shadow-sm)' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
            <h3 style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--primary)', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Scale size={18} /> Side-by-Side Head-to-Head Comparison ({selectedLoans.length} Selected)
            </h3>
            <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Click cards below to change selection</span>
          </div>

          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.84rem' }}>
              <thead>
                <tr style={{ background: 'var(--bg-card-subtle)' }}>
                  <th style={{ padding: '10px 14px', textAlign: 'left', border: '1px solid var(--border)', width: '22%' }}>Features</th>
                  {selectedLoans.map(l => (
                    <th key={l.id} style={{ padding: '10px 14px', textAlign: 'left', border: '1px solid var(--border)' }}>
                      <div style={{ fontWeight: 800, color: 'var(--primary)', fontSize: '0.92rem' }}>{l.bank_name}</div>
                      <div style={{ fontSize: '0.76rem', color: 'var(--text-muted)' }}>{l.product_name}</div>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td style={{ padding: '10px 14px', fontWeight: 700, border: '1px solid var(--border)', background: '#fafafa' }}>Indicative Rate</td>
                  {selectedLoans.map(l => (
                    <td key={l.id} style={{ padding: '10px 14px', border: '1px solid var(--border)', fontWeight: 700, color: 'var(--primary)' }}>
                      {l.indicative_rate_min}% - {l.indicative_rate_max}% p.a.
                      <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: 400 }}>{l.rate_benchmark}</div>
                    </td>
                  ))}
                </tr>
                <tr>
                  <td style={{ padding: '10px 14px', fontWeight: 700, border: '1px solid var(--border)', background: '#fafafa' }}>Collateral Requirement</td>
                  {selectedLoans.map(l => (
                    <td key={l.id} style={{ padding: '10px 14px', border: '1px solid var(--border)', fontSize: '0.8rem' }}>
                      {l.collateral_requirement}
                    </td>
                  ))}
                </tr>
                <tr>
                  <td style={{ padding: '10px 14px', fontWeight: 700, border: '1px solid var(--border)', background: '#fafafa' }}>Margin Money</td>
                  {selectedLoans.map(l => (
                    <td key={l.id} style={{ padding: '10px 14px', border: '1px solid var(--border)' }}>
                      {l.margin_money}
                    </td>
                  ))}
                </tr>
                <tr>
                  <td style={{ padding: '10px 14px', fontWeight: 700, border: '1px solid var(--border)', background: '#fafafa' }}>Moratorium Period</td>
                  {selectedLoans.map(l => (
                    <td key={l.id} style={{ padding: '10px 14px', border: '1px solid var(--border)' }}>
                      {l.moratorium_period}
                    </td>
                  ))}
                </tr>
                <tr>
                  <td style={{ padding: '10px 14px', fontWeight: 700, border: '1px solid var(--border)', background: '#fafafa' }}>Girl Student Concession</td>
                  {selectedLoans.map(l => (
                    <td key={l.id} style={{ padding: '10px 14px', border: '1px solid var(--border)', color: 'var(--accent)', fontWeight: 600 }}>
                      {l.girl_student_concession}
                    </td>
                  ))}
                </tr>
                <tr>
                  <td style={{ padding: '10px 14px', fontWeight: 700, border: '1px solid var(--border)', background: '#fafafa' }}>Official Application</td>
                  {selectedLoans.map(l => (
                    <td key={l.id} style={{ padding: '10px 14px', border: '1px solid var(--border)' }}>
                      <a
                        href={l.official_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn-apply"
                        style={{ padding: '6px 12px', fontSize: '0.78rem' }}
                      >
                        <span>Visit Official Portal</span>
                        <ExternalLink size={12} />
                      </a>
                    </td>
                  ))}
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Grid of All Matching Loans */}
      <div className="cards-grid">
        {loans.map(loan => {
          const isSelected = selectedIds.includes(loan.id);
          const tagClass = loan.category === 'public_bank' ? 'tag-public' : loan.category === 'nbfc' ? 'tag-nbfc' : 'tag-private';

          return (
            <div
              key={loan.id}
              className="item-card"
              style={{
                borderColor: isSelected ? 'var(--primary)' : 'var(--border)',
                borderWidth: isSelected ? '2px' : '1px'
              }}
            >
              <div>
                <div className="item-badge-row">
                  <span className={`category-tag ${tagClass}`}>
                    {loan.category.replace('_', ' ')}
                  </span>
                  <button
                    onClick={() => toggleSelect(loan.id)}
                    style={{
                      background: isSelected ? 'var(--primary)' : 'var(--bg-card-subtle)',
                      color: isSelected ? '#ffffff' : 'var(--text-main)',
                      border: '1px solid var(--border)',
                      padding: '4px 8px',
                      borderRadius: '4px',
                      fontSize: '0.72rem',
                      fontWeight: 700,
                      cursor: 'pointer'
                    }}
                  >
                    {isSelected ? '✓ Selected to Compare' : '+ Compare'}
                  </button>
                </div>

                <h3>{loan.product_name}</h3>
                <div className="bank-name">{loan.bank_name}</div>

                <div className="rate-box">
                  <div>
                    <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Indicative Rate</div>
                    <div className="rate-text">{loan.indicative_rate_min}% - {loan.indicative_rate_max}%</div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Max Tenure</div>
                    <div style={{ fontWeight: 700 }}>{loan.max_tenure_years} Years</div>
                  </div>
                </div>

                <ul className="features-list">
                  {loan.key_highlights.map((h, i) => (
                    <li key={i}>
                      <Check size={14} color="var(--accent)" style={{ flexShrink: 0, marginTop: '2px' }} />
                      <span>{h}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <div style={{ fontSize: '0.76rem', color: 'var(--text-muted)', marginBottom: '12px' }}>
                  <strong>Collateral:</strong> {loan.collateral_requirement}
                </div>
                <a
                  href={loan.official_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-apply"
                >
                  <span>Check Bank Details</span>
                  <ExternalLink size={14} />
                </a>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
