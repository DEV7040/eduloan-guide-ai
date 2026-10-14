import React, { useState, useEffect } from 'react';
import { Landmark, ExternalLink, ShieldCheck, CheckCircle, Award, HelpCircle } from 'lucide-react';
import { fetchSchemes } from '../api';

export default function SchemesTab() {
  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const res = await fetchSchemes();
        setSchemes(res.schemes || []);
      } catch (e) {
        console.error("Failed to load schemes", e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Landmark size={24} color="var(--primary)" />
          Government Schemes, Subsidies & Official Portals
        </h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem' }}>
          Verified financial assistance, moratorium interest waivers, and single-window application portals mandated by the Government of India.
        </p>
      </div>

      <div className="cards-grid">
        {schemes.map((scheme) => (
          <div key={scheme.id} className="item-card">
            <div>
              <div className="item-badge-row">
                <span className="category-tag tag-subsidy">{scheme.type}</span>
                <span style={{ fontSize: '0.74rem', color: 'var(--text-muted)', fontWeight: 600 }}>{scheme.nodal_bank}</span>
              </div>

              <h3>{scheme.name}</h3>
              <div className="bank-name">{scheme.authority}</div>

              <div style={{ background: 'var(--primary-light)', padding: '12px', borderRadius: 'var(--radius-sm)', marginBottom: '14px', border: '1px solid var(--primary-border)' }}>
                <div style={{ fontSize: '0.74rem', fontWeight: 700, color: 'var(--primary)', textTransform: 'uppercase' }}>Key Benefit</div>
                <div style={{ fontSize: '0.84rem', fontWeight: 600, color: 'var(--text-main)', marginTop: '2px' }}>
                  {scheme.benefits}
                </div>
              </div>

              <div style={{ marginBottom: '14px', fontSize: '0.82rem' }}>
                <div style={{ marginBottom: '6px' }}>
                  <strong>Eligibility:</strong> {scheme.eligibility_summary}
                </div>
                <div style={{ marginBottom: '6px' }}>
                  <strong>Income Ceiling:</strong> <span style={{ color: 'var(--accent)', fontWeight: 700 }}>{scheme.income_ceiling}</span>
                </div>
                <div style={{ marginBottom: '6px' }}>
                  <strong>Course Scope:</strong> {scheme.course_scope}
                </div>
              </div>

              <ul className="features-list">
                {scheme.key_notes.map((note, i) => (
                  <li key={i}>
                    <CheckCircle size={14} color="var(--accent)" style={{ flexShrink: 0, marginTop: '2px' }} />
                    <span>{note}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <div style={{ fontSize: '0.76rem', color: 'var(--text-muted)', marginBottom: '10px' }}>
                <strong>Application Path:</strong> {scheme.how_to_apply}
              </div>
              <a
                href={scheme.official_url}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-apply"
              >
                <span>Visit Official Scheme Portal</span>
                <ExternalLink size={14} />
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
