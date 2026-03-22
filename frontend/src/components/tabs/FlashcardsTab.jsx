import { useState } from 'react'
import { generateFlashcards } from '../../lib/api'

function FlipCard({ card, index }) {
  const [flipped, setFlipped] = useState(false)
  return (
    <div onClick={() => setFlipped(f => !f)} style={{ cursor: 'pointer', perspective: 1000, height: 200 }}>
      <div style={{ width: '100%', height: '100%', position: 'relative', transformStyle: 'preserve-3d', transition: 'transform 0.45s', transform: flipped ? 'rotateY(180deg)' : 'rotateY(0)' }}>
        <div style={{ position: 'absolute', inset: 0, backfaceVisibility: 'hidden', background: '#2f2f2f', border: '1px solid #3f3f3f', borderTop: '3px solid #ab68ff', borderRadius: 14, padding: '20px 22px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <span style={{ fontSize: 12, fontWeight: 700, color: '#ab68ff', textTransform: 'uppercase', letterSpacing: '0.07em' }}>سؤال {index}</span>
          <p style={{ fontSize: 15, color: '#ececec', lineHeight: 1.7, fontWeight: 500 }}>{card.q}</p>
          <p style={{ fontSize: 12, color: '#8e8ea0' }}>اضغط للإجابة ↩</p>
        </div>
        <div style={{ position: 'absolute', inset: 0, backfaceVisibility: 'hidden', transform: 'rotateY(180deg)', background: '#1a2e1a', border: '1px solid #2d5a2d', borderTop: '3px solid #19c37d', borderRadius: 14, padding: '20px 22px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <span style={{ fontSize: 12, fontWeight: 700, color: '#19c37d', textTransform: 'uppercase', letterSpacing: '0.07em' }}>إجابة {index}</span>
          <p style={{ fontSize: 15, color: '#ececec', lineHeight: 1.7 }}>{card.a}</p>
          <p style={{ fontSize: 12, color: '#8e8ea0' }}>اضغط للعودة ↩</p>
        </div>
      </div>
    </div>
  )
}

export default function FlashcardsTab({ docId }) {
  const [cards, setCards]     = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState(null)

  const generate = async () => {
    if (!docId || loading) return
    setLoading(true); setError(null); setCards([])
    try { const d = await generateFlashcards(docId); setCards(d.cards || []) }
    catch (e) { setError(e.message) }
    finally { setLoading(false) }
  }

  return (
    <div style={{ height: '100%', overflowY: 'auto', direction: 'rtl', padding: '32px 40px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 28, flexWrap: 'wrap', gap: 12 }}>
        <div>
          <h2 style={{ fontSize: 22, fontWeight: 700, color: '#ececec', marginBottom: 4 }}>البطاقات التعليمية</h2>
          <p style={{ fontSize: 14, color: '#8e8ea0' }}>اضغط على البطاقة لرؤية الإجابة</p>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          {cards.length > 0 && <span style={{ fontSize: 14, padding: '6px 14px', borderRadius: 20, background: 'rgba(171,104,255,0.15)', color: '#ab68ff', border: '1px solid rgba(171,104,255,0.3)' }}>{cards.length} بطاقة</span>}
          <button onClick={generate} disabled={!docId || loading} style={{
            padding: '10px 26px', borderRadius: 10, border: 'none', cursor: 'pointer',
            background: (!docId || loading) ? '#2f2f2f' : '#ab68ff',
            color: (!docId || loading) ? '#8e8ea0' : '#fff',
            fontFamily: 'Cairo, sans-serif', fontSize: 15, fontWeight: 700,
          }}>
            {loading ? '⏳ جاري الإنشاء...' : '🃏 توليد البطاقات'}
          </button>
        </div>
      </div>

      {error && <div style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.25)', borderRadius: 12, padding: '16px 20px', color: '#fca5a5', fontSize: 15, marginBottom: 20 }}>{error}</div>}

      {cards.length > 0 && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: 16 }}>
          {cards.map((c, i) => <FlipCard key={i} card={c} index={i + 1} />)}
        </div>
      )}

      {cards.length === 0 && !loading && !error && (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '60vh', color: '#8e8ea0', gap: 12 }}>
          <div style={{ fontSize: 52 }}>🃏</div>
          <p style={{ fontSize: 16 }}>{docId ? 'اضغط "توليد البطاقات" للبدء' : 'ارفع ملفًا أولًا'}</p>
        </div>
      )}
    </div>
  )
}
