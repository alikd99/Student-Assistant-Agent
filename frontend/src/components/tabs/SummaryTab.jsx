import { useState } from 'react'
import { summarize } from '../../lib/api'

export default function SummaryTab({ docId }) {
  const [lang, setLang]       = useState('ar')
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState(null)

  const generate = async () => {
    if (!docId || loading) return
    setLoading(true); setError(null); setSummary(null)
    try { const d = await summarize(docId, lang); setSummary(d.summary) }
    catch (e) { setError(e.message) }
    finally { setLoading(false) }
  }

  return (
    <div style={{ height: '100%', overflowY: 'auto', direction: 'rtl', padding: '32px 40px' }}>

      {/* Controls row */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 28, flexWrap: 'wrap', gap: 12 }}>
        <div>
          <h2 style={{ fontSize: 22, fontWeight: 700, color: '#ececec', marginBottom: 4 }}>ملخص الملف</h2>
          <p style={{ fontSize: 14, color: '#8e8ea0' }}>يلخص المحتوى الدراسي تلقائيًا باستخدام الذكاء الاصطناعي</p>
        </div>
        <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
          <div style={{ display: 'flex', background: '#2f2f2f', borderRadius: 10, padding: 4, gap: 4, border: '1px solid #3f3f3f' }}>
            {[['ar', '🇸🇦 عربي'], ['en', '🇺🇸 English']].map(([v, l]) => (
              <button key={v} onClick={() => setLang(v)} style={{
                padding: '8px 20px', borderRadius: 7, border: 'none', cursor: 'pointer',
                fontFamily: 'Cairo, sans-serif', fontSize: 14, fontWeight: 600,
                background: lang === v ? '#19c37d' : 'transparent',
                color: lang === v ? '#fff' : '#8e8ea0', transition: 'all 0.15s',
              }}>{l}</button>
            ))}
          </div>
          <button onClick={generate} disabled={!docId || loading} style={{
            padding: '10px 26px', borderRadius: 10, border: 'none', cursor: 'pointer',
            background: (!docId || loading) ? '#2f2f2f' : '#19c37d',
            color: (!docId || loading) ? '#8e8ea0' : '#fff',
            fontFamily: 'Cairo, sans-serif', fontSize: 15, fontWeight: 700, transition: 'all 0.15s',
          }}>
            {loading ? '⏳ جاري التلخيص...' : '📝 توليد الملخص'}
          </button>
        </div>
      </div>

      {error && (
        <div style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.25)', borderRadius: 12, padding: '16px 20px', color: '#fca5a5', fontSize: 15, marginBottom: 20 }}>
          {error}
        </div>
      )}

      {summary && (
        <div style={{
          background: '#2a2a2a', border: '1px solid #3f3f3f', borderRadius: 14,
          padding: '28px 32px', fontSize: 16, lineHeight: 2, color: '#d1d5db',
          direction: lang === 'ar' ? 'rtl' : 'ltr', whiteSpace: 'pre-wrap',
        }}>
          {summary}
        </div>
      )}

      {!summary && !loading && !error && (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '60vh', color: '#8e8ea0', gap: 12 }}>
          <div style={{ fontSize: 52 }}>📄</div>
          <p style={{ fontSize: 16 }}>{docId ? 'اضغط "توليد الملخص" للبدء' : 'ارفع ملفًا أولًا من الشريط الجانبي'}</p>
        </div>
      )}
    </div>
  )
}
