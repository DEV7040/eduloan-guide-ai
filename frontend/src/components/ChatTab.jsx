import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, Sparkles, ExternalLink, ShieldCheck, HelpCircle, Loader2 } from 'lucide-react';
import { sendChatMessage, fetchInitialGreeting } from '../api';

export default function ChatTab({ language, apiKey, onNavigateTab }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Initialize with official greeting
  useEffect(() => {
    async function loadGreeting() {
      try {
        const data = await fetchInitialGreeting(language);
        setMessages([
          { role: 'assistant', content: data.greeting }
        ]);
      } catch (e) {
        setMessages([
          {
            role: 'assistant',
            content: "Hello! Welcome to EduLoan Guide AI 🎓. Are you planning to study in India or abroad? I'll help you explore suitable education loans, check eligibility, compare options, and estimate your EMI."
          }
        ]);
      }
    }
    loadGreeting();
  }, [language]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (textToSend) => {
    const text = (textToSend || input).trim();
    if (!text || loading) return;

    const newMsgs = [...messages, { role: 'user', content: text }];
    setMessages(newMsgs);
    setInput('');
    setLoading(true);

    try {
      const data = await sendChatMessage(newMsgs, apiKey, language);
      if (data && data.response) {
        setMessages([...newMsgs, { role: 'assistant', content: data.response }]);
      } else {
        setMessages([...newMsgs, { role: 'assistant', content: 'Unable to reach service. Please verify your connection or try again.' }]);
      }
    } catch (err) {
      setMessages([...newMsgs, { role: 'assistant', content: 'Network error communicating with EduLoan Guide AI server.' }]);
    } finally {
      setLoading(false);
    }
  };

  // Basic markdown formatter for structured chat text
  const renderMessageContent = (content) => {
    // Process markdown headers, bold, bullet points, blockquotes, links
    const lines = content.split('\n');
    return lines.map((line, idx) => {
      // Header 3
      if (line.startsWith('### ')) {
        return <h3 key={idx} style={{ marginTop: '8px', marginBottom: '4px' }}>{line.replace('### ', '')}</h3>;
      }
      // Blockquote
      if (line.startsWith('> ')) {
        return <blockquote key={idx}>{line.replace('> ', '')}</blockquote>;
      }
      // Bullet list item
      if (line.trim().startsWith('- ') || line.trim().startsWith('* ')) {
        const itemText = line.trim().replace(/^[-*]\s+/, '');
        return <li key={idx} dangerouslySetInnerHTML={{ __html: formatInline(itemText) }} />;
      }
      // Numbered list item
      if (/^\d+\.\s/.test(line.trim())) {
        return <div key={idx} style={{ marginLeft: '10px', marginTop: '3px' }} dangerouslySetInnerHTML={{ __html: formatInline(line) }} />;
      }
      // Markdown Table row
      if (line.trim().startsWith('|')) {
        return <div key={idx} style={{ fontFamily: 'monospace', fontSize: '0.8rem', background: '#f8fafc', padding: '2px 4px' }}>{line}</div>;
      }
      if (!line.trim()) {
        return <div key={idx} style={{ height: '6px' }} />;
      }
      return <p key={idx} dangerouslySetInnerHTML={{ __html: formatInline(line) }} />;
    });
  };

  const formatInline = (str) => {
    return str
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');
  };

  const quickPrompts = [
    { label: '🇮🇳 Study in India', query: 'I am planning to study in India. What are the top education loans and collateral rules?' },
    { label: '🌍 Study Abroad', query: 'I want to study abroad (MS/MBA). How can I get a loan without mortgaging property?' },
    { label: '🧮 Calculate EMI (₹15L)', query: 'Calculate EMI for ₹15 Lakhs education loan for 10 years at 9% interest' },
    { label: '🏛️ CSIS Subsidy Info', query: 'Am I eligible for the Central Sector Interest Subsidy (CSIS)? What are the income limits?' },
    { label: '⚖️ SBI vs HDFC Credila', query: 'Compare SBI Education Loan vs HDFC Credila for abroad studies' },
    { label: '📑 Document Checklist', query: 'What documents are required for an education loan in India?' }
  ];

  return (
    <div className="chat-layout">
      {/* Main Chat Area */}
      <div className="chat-card">
        <div className="chat-card-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Bot size={20} color="var(--primary)" />
            <span style={{ fontWeight: 700, fontSize: '0.92rem' }}>EduLoan Guide AI Advisor</span>
          </div>
          <div className="chat-status-pill">
            <span className="status-dot"></span>
            <span>Verified Knowledge Online</span>
          </div>
        </div>

        {/* Message Feed */}
        <div className="chat-messages">
          {messages.map((msg, i) => (
            <div key={i} className={`message-row ${msg.role}`}>
              <div className={`message-avatar ${msg.role}`}>
                {msg.role === 'assistant' ? <Bot size={20} /> : <User size={20} />}
              </div>
              <div className="message-bubble">
                {renderMessageContent(msg.content)}
              </div>
            </div>
          ))}

          {loading && (
            <div className="message-row assistant">
              <div className="message-avatar assistant">
                <Bot size={20} />
              </div>
              <div className="message-bubble" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Loader2 size={16} className="animate-spin" />
                <span>EduLoan AI is reviewing verified guidelines...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Quick Suggestion Pills */}
        <div className="quick-prompts-bar">
          <span style={{ fontSize: '0.76rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '4px', fontWeight: 600 }}>
            <Sparkles size={14} color="var(--warning)" /> Quick Ask:
          </span>
          {quickPrompts.map((p, idx) => (
            <button
              key={idx}
              className="prompt-pill"
              onClick={() => handleSend(p.query)}
              disabled={loading}
            >
              {p.label}
            </button>
          ))}
        </div>

        {/* Chat Input */}
        <form
          className="chat-input-area"
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
        >
          <input
            type="text"
            placeholder={
              language === 'hi'
                ? "एजुकेशन लोन, ब्याज दर या कॉलेज के बारे में कुछ भी पूछें..."
                : language === 'mr'
                ? "शैक्षणिक कर्ज, व्याजदर किंवा महाविद्यालयाबद्दल विचारा..."
                : "Ask about education loans, eligibility, SBI vs HDFC, CSIS subsidy, or documents..."
            }
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
          />
          <button type="submit" className="send-btn" disabled={loading || !input.trim()}>
            <Send size={16} />
            <span>Send</span>
          </button>
        </form>
      </div>

      {/* Right Sidebar: Direct Links & Action Shortcuts */}
      <div className="chat-sidebar">
        <div className="sidebar-card">
          <div className="sidebar-title">
            <ShieldCheck size={18} color="var(--accent)" />
            <span>Verified Official Portals</span>
          </div>
          <a
            href="https://www.vidyalakshmi.co.in"
            target="_blank"
            rel="noopener noreferrer"
            className="portal-link-item"
          >
            <span>Vidya Lakshmi Portal</span>
            <ExternalLink size={14} />
          </a>
          <a
            href="https://www.jansamarth.in"
            target="_blank"
            rel="noopener noreferrer"
            className="portal-link-item"
          >
            <span>Jan Samarth Portal</span>
            <ExternalLink size={14} />
          </a>
          <a
            href="https://www.ncgtc.in/en/cgfsel"
            target="_blank"
            rel="noopener noreferrer"
            className="portal-link-item"
          >
            <span>NCGTC (CGFSEL Scheme)</span>
            <ExternalLink size={14} />
          </a>
          <a
            href="https://sbi.co.in/web/personal-banking/loans/education-loans"
            target="_blank"
            rel="noopener noreferrer"
            className="portal-link-item"
          >
            <span>SBI Education Loans</span>
            <ExternalLink size={14} />
          </a>
        </div>

        <div className="sidebar-card" style={{ background: 'var(--primary-light)', borderColor: 'var(--primary-border)' }}>
          <div className="sidebar-title" style={{ color: 'var(--primary)' }}>
            <HelpCircle size={18} />
            <span>Direct Tools</span>
          </div>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-main)', marginBottom: '12px' }}>
            Jump directly to dedicated interactive tools:
          </p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <button
              onClick={() => onNavigateTab('calculator')}
              className="btn-secondary"
              style={{ width: '100%', justifyContent: 'center' }}
            >
              🧮 Interactive EMI Calculator
            </button>
            <button
              onClick={() => onNavigateTab('eligibility')}
              className="btn-secondary"
              style={{ width: '100%', justifyContent: 'center' }}
            >
              🎯 Preliminary Eligibility Checker
            </button>
            <button
              onClick={() => onNavigateTab('comparison')}
              className="btn-secondary"
              style={{ width: '100%', justifyContent: 'center' }}
            >
              ⚖️ Side-by-Side Bank Comparison
            </button>
          </div>
        </div>

        <div className="sidebar-card" style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
          <strong style={{ color: 'var(--text-main)' }}>Rules & Guarantees:</strong>
          <ul style={{ paddingLeft: '16px', marginTop: '6px' }}>
            <li>Rates are indicative based on RBI repo linked benchmarks.</li>
            <li>No loan approval is guaranteed without bank credit appraisal.</li>
            <li>Zero collateral mandated for loans ≤ ₹7.5L under CGFSEL.</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
