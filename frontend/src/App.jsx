import React, { useState } from 'react';
import {
  GraduationCap,
  MessageSquare,
  Calculator,
  ShieldCheck,
  Scale,
  Landmark,
  FileText,
  Settings,
  Globe,
  ExternalLink
} from 'lucide-react';

import ChatTab from './components/ChatTab';
import EmiCalculatorTab from './components/EmiCalculatorTab';
import EligibilityTab from './components/EligibilityTab';
import ComparisonTab from './components/ComparisonTab';
import SchemesTab from './components/SchemesTab';
import DocumentsTab from './components/DocumentsTab';
import SettingsModal from './components/SettingsModal';

export default function App() {
  const [activeTab, setActiveTab] = useState('chat'); // 'chat' | 'calculator' | 'eligibility' | 'comparison' | 'schemes' | 'documents'
  const [language, setLanguage] = useState('en'); // 'en' | 'hi' | 'mr'
  const [apiKey, setApiKey] = useState(() => localStorage.getItem('eduloan_gemini_key') || '');
  const [showSettings, setShowSettings] = useState(false);

  const handleSaveApiKey = (newKey) => {
    setApiKey(newKey);
    localStorage.setItem('eduloan_gemini_key', newKey);
  };

  const tabs = [
    { id: 'chat', label: 'AI Advisor Chat', icon: MessageSquare },
    { id: 'calculator', label: 'EMI & Moratorium Calculator', icon: Calculator },
    { id: 'eligibility', label: 'Eligibility & Subsidy Checker', icon: ShieldCheck },
    { id: 'comparison', label: 'Bank & Loan Comparison', icon: Scale },
    { id: 'schemes', label: 'Govt Schemes & Subsidies', icon: Landmark },
    { id: 'documents', label: 'Document Checklist', icon: FileText },
  ];

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header">
        <div className="header-inner">
          <div className="brand-section">
            <div className="brand-icon">
              <GraduationCap size={24} />
            </div>
            <div className="brand-text">
              <h1>
                <span>EduLoan Guide AI</span>
                <span className="gov-badge">IBA & RBI Model Scheme</span>
              </h1>
              <p>Intelligent Education Loan & Scheme Assistant for Indian Students</p>
            </div>
          </div>

          <div className="header-actions">
            {/* Language Switcher */}
            <div className="lang-switch">
              <button
                className={`lang-btn ${language === 'en' ? 'active' : ''}`}
                onClick={() => setLanguage('en')}
              >
                EN
              </button>
              <button
                className={`lang-btn ${language === 'hi' ? 'active' : ''}`}
                onClick={() => setLanguage('hi')}
              >
                हिंदी
              </button>
              <button
                className={`lang-btn ${language === 'mr' ? 'active' : ''}`}
                onClick={() => setLanguage('mr')}
              >
                मराठी
              </button>
            </div>

            {/* Settings button */}
            <button
              onClick={() => setShowSettings(true)}
              className="btn-secondary"
              title="Configure API key / Settings"
            >
              <Settings size={16} />
              <span>Settings</span>
            </button>
          </div>
        </div>

        {/* Tab Navigation Bar */}
        <div className="tabs-bar">
          <div className="tabs-inner">
            {tabs.map((t) => {
              const Icon = t.icon;
              const isActive = activeTab === t.id;
              return (
                <button
                  key={t.id}
                  className={`tab-button ${isActive ? 'active' : ''}`}
                  onClick={() => setActiveTab(t.id)}
                >
                  <Icon size={18} />
                  <span>{t.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="main-content">
        {activeTab === 'chat' && (
          <ChatTab
            language={language}
            apiKey={apiKey}
            onNavigateTab={setActiveTab}
          />
        )}
        {activeTab === 'calculator' && <EmiCalculatorTab />}
        {activeTab === 'eligibility' && <EligibilityTab onNavigateTab={setActiveTab} />}
        {activeTab === 'comparison' && <ComparisonTab />}
        {activeTab === 'schemes' && <SchemesTab />}
        {activeTab === 'documents' && <DocumentsTab />}
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <div style={{ maxWidth: '1000px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <div>
            <strong>EduLoan Guide AI 🎓</strong> • Helping students across India access transparent, verified higher education funding.
          </div>
          <div style={{ fontSize: '0.76rem', color: 'var(--text-light)' }}>
            Disclaimer: EduLoan Guide AI calculates financial estimates based on Indian Banks' Association (IBA) guidelines and standard bank tariff sheets. Loan sanction, interest rates, and concessions are subject to final discretion and credit appraisal by individual banks and lending institutions. Never share passwords, OTPs, or confidential banking credentials.
          </div>
        </div>
      </footer>

      {/* Settings Modal */}
      <SettingsModal
        isOpen={showSettings}
        onClose={() => setShowSettings(false)}
        apiKey={apiKey}
        onSaveApiKey={handleSaveApiKey}
      />
    </div>
  );
}
