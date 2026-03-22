import { useState } from 'react'
import { generateExamQuestions } from '../../lib/api'

const LETTERS = ['أ', 'ب', 'ج', 'د']

function MCQCard({ q, index }) {
  const [selected, setSelected] = useState(null)
  return (
    <div style={{ background: '#2f2f2f', border: '1px solid #3f3f3f', borderRadius: 14, padding: '20px 24px', marginBottom: 14 }}>
      <p style={{ fontSize: 16, fontWeight: 600, color: '#ececec', marginBottom: 16, lineHeight: 1.7 }}>
        <span style={{ color: '#2563eb', marginLeft: 8 }}>{index}.</span>{q.question}
      </p>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        {q.options?.map((opt, j) => {
          const isCorrect = j === q.correct_index, isSelected = selected === j
          let bg = '#212121', border = '1px solid #3f3f3f', color = '#94a3b8'
          if (selected !== null) {
            if (isCorrect)       { bg = '#1a2e1a'; border = '1px solid #2d5a2d'; color = '#86efac' }
            else if (isSelected) { bg = '#2e1a1a'; border = '1px solid #5a2d2d'; color = '#fca5a5' }
          }
          return (
            <div key={j} onClick={() => selected === null && setSelected(j)} style={{ display: 'flex', alignItems: 'center', gap: 14, padding: '12px 18px', borderRadius: 10, cursor: selected === null ? 'pointer' : 'default', background: bg, border, color, fontSize: 15, transition: 'all 0.15s' }}>
              <span style={{ fontWeight: 700, minWidth: 22, textAlign: 'center', flexShrink: 0 }}>{LETTERS[j] ?? j + 1}</span>
              <span style={{ flex: 1 }}>{opt}</span>
              {selected !== null && isCorrect  && <span style={{ fontSize: 18 }}>✅</span>}
              {selected !== null && isSelected && !isCorrect && <span style={{ fontSize: 18 }}>❌</span>}
            </div>
          )
        })}
      </div>
      {selected !== null && <button onClick={() => setSelected(null)} style={{ marginTop: 10, fontSize: 13, color: '#8e8ea0', background: 'none', border: 'none', cursor: 'pointer', fontFamily: 'Cairo, sans-serif' }}>↺ إعادة المحاولة</button>}
    </div>
  )
}

function TFCard({ q, index }) {
  const [selected, setSelected] = useState(null)
  return (
    <div style={{ background: '#2f2f2f', border: '1px solid #3f3f3f', borderRadius: 14, padding: '16px 24px', marginBottom: 10, display: 'flex', alignItems: 'center', gap: 18 }}>
      <span style={{ color: '#2563eb', fontWeight: 700, fontSize: 16, flexShrink: 0 }}>{index}.</span>
      <p style={{ flex: 1, fontSize: 15, color: '#d1d5db', lineHeight: 1.7 }}>{q.question}</p>
      <div style={{ display: 'flex', gap: 8, flexShrink: 0 }}>
        {[true, false].map(val => {
          const isSelected = selected === val, isCorrect = val === q.answer
          let bg = 'transparent', border = '1px solid #3f3f3f', color = '#8e8ea0'
          if (selected !== null) {
            if (isSelected && isCorrect)  { bg = '#1a2e1a'; border = '1px solid #22c55e'; color = '#86efac' }
            else if (isSelected)          { bg = '#2e1a1a'; border = '1px solid #ef4444'; color = '#fca5a5' }
            else if (isCorrect)           { border = '1px solid rgba(34,197,94,0.3)'; color = '#86efac' }
          }
          return (
            <button key={String(val)} onClick={() => selected === null && setSelected(val)} style={{ padding: '8px 20px', borderRadius: 10, cursor: selected === null ? 'pointer' : 'default', fontFamily: 'Cairo, sans-serif', fontSize: 14, fontWeight: 700, background: bg, border, color, transition: 'all 0.15s' }}>
              {val ? 'صح ✓' : 'خطأ ✗'}
            </button>
          )
        })}
      </div>
    </div>
  )
}

export default function ExamTab({ docId }) {
  const [data, setData]       = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState(null)

  const generate = async () => {
    if (!docId || loading) return
    setLoading(true); setError(null); setData(null)
    try { setData(await generateExamQuestions(docId)) }
    catch (e) { setError(e.message) }
    finally { setLoading(false) }
  }

  const mcqs = data?.mcq || [], tfs = data?.true_false || []

  return (
    <div style={{ height: '100%', overflowY: 'auto', direction: 'rtl', padding: '32px 40px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 28, flexWrap: 'wrap', gap: 12 }}>
        <div>
          <h2 style={{ fontSize: 22, fontWeight: 700, color: '#ececec', marginBottom: 4 }}>أسئلة الاختبار</h2>
          <p style={{ fontSize: 14, color: '#8e8ea0' }}>اختبر نفسك — اضغط على إجابتك</p>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          {data && <>
            <span style={{ fontSize: 13, padding: '5px 14px', borderRadius: 20, background: 'rgba(37,99,235,0.15)', color: '#60a5fa', border: '1px solid rgba(37,99,235,0.3)' }}>{mcqs.length} اختيار متعدد</span>
            <span style={{ fontSize: 13, padding: '5px 14px', borderRadius: 20, background: '#2f2f2f', color: '#8e8ea0', border: '1px solid #3f3f3f' }}>{tfs.length} صح/خطأ</span>
          </>}
          <button onClick={generate} disabled={!docId || loading} style={{
            padding: '10px 26px', borderRadius: 10, border: 'none', cursor: 'pointer',
            background: (!docId || loading) ? '#2f2f2f' : '#2563eb',
            color: (!docId || loading) ? '#8e8ea0' : '#fff',
            fontFamily: 'Cairo, sans-serif', fontSize: 15, fontWeight: 700,
          }}>
            {loading ? '⏳ جاري الإنشاء...' : '📋 توليد الأسئلة'}
          </button>
        </div>
      </div>

      {error && <div style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.25)', borderRadius: 12, padding: '16px 20px', color: '#fca5a5', fontSize: 15, marginBottom: 20 }}>{error}</div>}

      {mcqs.length > 0 && <>
        <p style={{ fontSize: 13, fontWeight: 700, color: '#8e8ea0', textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: 14 }}>📌 اختيار متعدد</p>
        {mcqs.map((q, i) => <MCQCard key={i} q={q} index={i + 1} />)}
      </>}

      {tfs.length > 0 && <div style={{ marginTop: 28 }}>
        <p style={{ fontSize: 13, fontWeight: 700, color: '#8e8ea0', textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: 14 }}>✔️ صح / خطأ</p>
        {tfs.map((q, i) => <TFCard key={i} q={q} index={i + 1} />)}
      </div>}

      {!data && !loading && !error && (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '60vh', color: '#8e8ea0', gap: 12 }}>
          <div style={{ fontSize: 52 }}>📋</div>
          <p style={{ fontSize: 16 }}>{docId ? 'اضغط "توليد الأسئلة" للبدء' : 'ارفع ملفًا أولًا'}</p>
        </div>
      )}
    </div>
  )
}
