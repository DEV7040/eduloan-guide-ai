import React, { useState, useEffect } from 'react';
import { FileText, CheckSquare, Square, Printer, CheckCircle2, User, Users, Shield, FileCheck } from 'lucide-react';
import { fetchDocumentChecklist } from '../api';

export default function DocumentsTab() {
  const [destination, setDestination] = useState('india');
  const [coAppType, setCoAppType] = useState('salaried');
  const [loanAmount, setLoanAmount] = useState(1000000);
  const [hasCollateral, setHasCollateral] = useState(false);

  const [checklistData, setChecklistData] = useState(null);
  const [checkedItems, setCheckedItems] = useState({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function loadDocs() {
      setLoading(true);
      try {
        const res = await fetchDocumentChecklist({
          destination,
          loan_amount: Number(loanAmount),
          co_applicant_type: coAppType,
          has_collateral: hasCollateral
        });
        setChecklistData(res);
      } catch (e) {
        console.error("Failed to load documents", e);
      } finally {
        setLoading(false);
      }
    }
    loadDocs();
  }, [destination, coAppType, loanAmount, hasCollateral]);

  const toggleCheck = (id) => {
    setCheckedItems(prev => ({
      ...prev,
      [id]: !prev[id]
    }));
  };

  // Calculate readiness percentage
  const totalItems = checklistData ? checklistData.total_documents_count : 0;
  const collectedCount = Object.values(checkedItems).filter(Boolean).length;
  const progressPct = totalItems > 0 ? Math.round((collectedCount / totalItems) * 100) : 0;

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h2 style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '10px' }}>
            <FileText size={24} color="var(--primary)" />
            Personalized Document Checklist & Readiness Tracker
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem' }}>
            Filter based on your study destination and co-applicant profession to generate a bank-ready dossier.
          </p>
        </div>

        <button
          onClick={() => window.print()}
          className="btn-secondary"
          style={{ display: 'flex', alignItems: 'center', gap: '6px' }}
        >
          <Printer size={16} />
          <span>Print / Save Checklist</span>
        </button>
      </div>

      {/* Filter Bar */}
      <div style={{ background: '#ffffff', padding: '16px 20px', borderRadius: 'var(--radius-lg)', border: '1px solid var(--border)', marginBottom: '24px', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px' }}>
        <div>
          <label style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>
            STUDY DESTINATION
          </label>
          <select
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
            style={{ width: '100%', padding: '8px 12px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border)' }}
          >
            <option value="india">Studies in India</option>
            <option value="abroad">Studies Abroad (Overseas)</option>
          </select>
        </div>

        <div>
          <label style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>
            CO-APPLICANT PROFESSION
          </label>
          <select
            value={coAppType}
            onChange={(e) => setCoAppType(e.target.value)}
            style={{ width: '100%', padding: '8px 12px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border)' }}
          >
            <option value="salaried">Salaried Employee (MNC / Govt / Private)</option>
            <option value="self_employed">Self-Employed / Business Owner</option>
            <option value="farmer_agriculturist">Farmer / Agriculturist</option>
          </select>
        </div>

        <div>
          <label style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>
            LOAN AMOUNT CATEGORY
          </label>
          <select
            value={loanAmount}
            onChange={(e) => setLoanAmount(Number(e.target.value))}
            style={{ width: '100%', padding: '8px 12px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border)' }}
          >
            <option value={500000}>Up to ₹7.5 Lakhs (Collateral-Free CGFSEL)</option>
            <option value={2000000}>Above ₹7.5 Lakhs (Tangible Collateral)</option>
          </select>
        </div>
      </div>

      {/* Progress Bar */}
      <div style={{ background: '#ffffff', padding: '16px 20px', borderRadius: 'var(--radius-lg)', border: '1px solid var(--border)', marginBottom: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
          <span style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-main)' }}>
            Dossier Readiness: {collectedCount} of {totalItems} documents gathered
          </span>
          <span style={{ fontSize: '0.9rem', fontWeight: 800, color: progressPct === 100 ? 'var(--accent)' : 'var(--primary)' }}>
            {progressPct}% Ready
          </span>
        </div>
        <div style={{ height: '8px', background: 'var(--bg-card-subtle)', borderRadius: '9999px', overflow: 'hidden' }}>
          <div
            style={{
              width: `${progressPct}%`,
              height: '100%',
              background: progressPct === 100 ? 'var(--accent)' : 'var(--primary)',
              transition: 'width 0.3s'
            }}
          />
        </div>
      </div>

      {/* Categorized Document Groups */}
      {checklistData && checklistData.categories.map((cat, idx) => {
        if (!cat.items || cat.items.length === 0) return null;

        return (
          <div key={idx} style={{ background: '#ffffff', borderRadius: 'var(--radius-lg)', border: '1px solid var(--border)', padding: '20px', marginBottom: '20px' }}>
            <h3 style={{ fontSize: '1rem', fontWeight: 800, color: 'var(--primary)', marginBottom: '4px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <FileCheck size={18} />
              {cat.category_title}
            </h3>
            {cat.note && (
              <div style={{ fontSize: '0.78rem', color: 'var(--warning)', fontWeight: 600, marginBottom: '14px' }}>
                ℹ️ {cat.note}
              </div>
            )}

            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginTop: '12px' }}>
              {cat.items.map((item) => {
                const isChecked = !!checkedItems[item.id];
                return (
                  <div
                    key={item.id}
                    onClick={() => toggleCheck(item.id)}
                    style={{
                      display: 'flex',
                      alignItems: 'flex-start',
                      gap: '12px',
                      padding: '12px 14px',
                      borderRadius: 'var(--radius-sm)',
                      background: isChecked ? 'var(--accent-light)' : 'var(--bg-card-subtle)',
                      border: '1px solid',
                      borderColor: isChecked ? 'var(--accent-border)' : 'var(--border)',
                      cursor: 'pointer',
                      transition: 'all 0.2s'
                    }}
                  >
                    <div style={{ marginTop: '2px', color: isChecked ? 'var(--accent)' : 'var(--text-muted)' }}>
                      {isChecked ? <CheckSquare size={18} /> : <Square size={18} />}
                    </div>

                    <div style={{ flex: 1 }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <span style={{ fontSize: '0.88rem', fontWeight: 700, color: isChecked ? 'var(--accent)' : 'var(--text-main)', textDecoration: isChecked ? 'line-through' : 'none' }}>
                          {item.name}
                        </span>
                        {item.mandatory && (
                          <span style={{ fontSize: '0.7rem', color: 'var(--danger)', fontWeight: 700, background: 'var(--danger-light)', padding: '1px 6px', borderRadius: '4px' }}>
                            Mandatory
                          </span>
                        )}
                      </div>
                      <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                        {item.details}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        );
      })}
    </div>
  );
}
