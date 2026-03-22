import { useState } from 'react'
import Sidebar from './components/Sidebar'
import QATab from './components/tabs/QATab'
import SummaryTab from './components/tabs/SummaryTab'
import FlashcardsTab from './components/tabs/FlashcardsTab'
import ExamTab from './components/tabs/ExamTab'

const TABS = [
  { id: 'qa',      label: '💬 سؤال وجواب' },
  { id: 'summary', label: '📝 ملخص' },
  { id: 'flash',   label: '🃏 بطاقات' },
  { id: 'exam',    label: '📋 اختبار' },
]

export default function App() {
  const [doc, setDoc]         = useState(null)
  const [tab, setTab]         = useState('qa')

  return (
    <div style={{ display: 'flex', height: '100vh', background: '#212121', color: '#ececec', fontFamily: 'Cairo, Segoe UI, sans-serif', direction: 'ltr', overflow: 'hidden' }}>
      <Sidebar selectedDoc={doc} onSelectDoc={setDoc} />

      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden', direction: 'rtl' }}>
        {/* Tab bar — only show when doc is selected */}
        {doc && (
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '10px 20px', borderBottom: '1px solid #2f2f2f', flexShrink: 0 }}>
            <span style={{ fontSize: 14, color: '#8e8ea0', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', maxWidth: 300 }}>
              📄 {doc.filename}
            </span>
            <div style={{ display: 'flex', gap: 4 }}>
              {TABS.map(t => (
                <button key={t.id} onClick={() => setTab(t.id)} style={{
                  padding: '7px 16px', borderRadius: 8, border: 'none', cursor: 'pointer',
                  fontFamily: 'Cairo, sans-serif', fontSize: 13, fontWeight: 600,
                  background: tab === t.id ? '#2f2f2f' : 'transparent',
                  color: tab === t.id ? '#ececec' : '#8e8ea0',
                  transition: 'all 0.15s',
                }}>
                  {t.label}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Main content */}
        <div style={{ flex: 1, overflow: 'hidden' }}>
          {tab === 'qa'      && <QATab         docId={doc?.doc_id} noDoc={!doc} />}
          {tab === 'summary' && <SummaryTab    docId={doc?.doc_id} />}
          {tab === 'flash'   && <FlashcardsTab docId={doc?.doc_id} />}
          {tab === 'exam'    && <ExamTab       docId={doc?.doc_id} />}
        </div>
      </div>
    </div>
  )
}
