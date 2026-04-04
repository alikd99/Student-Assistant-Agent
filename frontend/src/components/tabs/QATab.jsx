import { useState, useRef, useEffect, forwardRef } from 'react'
import { askQuestion } from '../../lib/api'

const SUGGESTIONS = [
  'ما هي الأفكار الرئيسية في هذا الملف؟',
  'لخّص لي المحتوى باختصار',
  'ما المفاهيم الأساسية التي يجب حفظها؟',
  'اشرح لي أصعب جزء في هذا الملف',
]

function Bubble({ role, text, sources }) {
  const isUser = role === 'user'
  return (
    <div style={{ padding: '20px 40px', background: isUser ? 'transparent' : '#2a2a2a', borderBottom: '1px solid #2f2f2f', direction: 'rtl' }}>
      <div style={{ display: 'flex', gap: 16, alignItems: 'flex-start' }}>
        <div style={{ width: 38, height: 38, borderRadius: '50%', flexShrink: 0, background: isUser ? '#19c37d' : '#ab68ff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 16, fontWeight: 700, color: '#fff' }}>
          {isUser ? 'أ' : '🤖'}
        </div>
        <div style={{ flex: 1, paddingTop: 4 }}>
          <p style={{ fontSize: 14, fontWeight: 700, color: '#8e8ea0', marginBottom: 8 }}>{isUser ? 'أنت' : 'المساعد'}</p>
          <div style={{ fontSize: 16, lineHeight: 1.85, color: '#ececec', whiteSpace: 'pre-wrap' }}>{text}</div>
          {sources?.length > 0 && (
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginTop: 12 }}>
              {sources.map((s, i) => (
                <span key={i} style={{ fontSize: 12, padding: '4px 12px', borderRadius: 20, background: '#3f3f3f', color: '#8e8ea0', border: '1px solid #4f4f4f' }}>
                  📄 {s.filename} · ص{s.page_num}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default function QATab({ docId, noDoc }) {
  const [messages, setMessages] = useState([])
  const [input, setInput]       = useState('')
  const [loading, setLoading]   = useState(false)
  const textareaRef = useRef(null)
  const bottomRef   = useRef(null)

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [messages, loading])

  const send = async (text) => {
    const q = (text || input).trim()
    if (!q || !docId || loading) return
    setInput('')
    if (textareaRef.current) { textareaRef.current.style.height = '52px' }
    setMessages(m => [...m, { role: 'user', text: q }])
    setLoading(true)
    try {
      const data = await askQuestion(q, docId)
      setMessages(m => [...m, { role: 'ai', text: data.answer, sources: data.sources }])
    } catch (e) {
      setMessages(m => [...m, { role: 'ai', text: '❌ ' + e.message }])
    } finally { setLoading(false) }
  }

  const isEmpty = messages.length === 0

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div style={{ flex: 1, overflowY: 'auto' }}>
        {isEmpty ? (
          /* ── Welcome ── */
          <div style={{ height: '100%', display: 'flex', flexDirection: 'column', direction: 'rtl' }}>
            {/* Top section */}
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '60px 40px 20px' }}>
              <div style={{ fontSize: 56, marginBottom: 20 }}>📚</div>
              <h1 style={{ fontSize: 34, fontWeight: 700, color: '#ececec', marginBottom: 12, textAlign: 'center' }}>
                {noDoc ? 'مرحبًا 👋' : 'كيف يمكنني مساعدتك؟'}
              </h1>
              <p style={{ fontSize: 17, color: '#8e8ea0', textAlign: 'center', maxWidth: 500 }}>
                {noDoc
                  ? 'ارفع ملفًا دراسيًا من الشريط الجانبي للبدء'
                  : 'اسأل أي سؤال عن محتوى الملف وسأجيبك فورًا'}
              </p>
            </div>

            {/* Input + suggestions — anchored to bottom half */}
            <div style={{ padding: '20px 40px 48px', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 16 }}>
              <div style={{ width: '100%', maxWidth: 700 }}>
                <InputBar ref={textareaRef} value={input} onChange={setInput} onSend={() => send()} loading={loading} disabled={!docId} />
              </div>
              {docId && (
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 10, justifyContent: 'center', maxWidth: 700 }}>
                  {SUGGESTIONS.map((s, i) => (
                    <button key={i} onClick={() => send(s)} style={{
                      padding: '11px 22px', borderRadius: 24, border: '1px solid #3f3f3f',
                      background: '#2f2f2f', color: '#d1d5db', cursor: 'pointer',
                      fontFamily: 'Cairo, sans-serif', fontSize: 14, transition: 'background 0.15s',
                    }}
                      onMouseEnter={e => e.currentTarget.style.background = '#3f3f3f'}
                      onMouseLeave={e => e.currentTarget.style.background = '#2f2f2f'}
                    >{s}</button>
                  ))}
                </div>
              )}
            </div>
          </div>
        ) : (
          <>
            {messages.map((m, i) => <Bubble key={i} role={m.role} text={m.text} sources={m.sources} />)}
            {loading && (
              <div style={{ padding: '20px 40px', background: '#2a2a2a', direction: 'rtl' }}>
                <div style={{ display: 'flex', gap: 16, alignItems: 'center' }}>
                  <div style={{ width: 38, height: 38, borderRadius: '50%', background: '#ab68ff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 16, color: '#fff', flexShrink: 0 }}>🤖</div>
                  <div style={{ display: 'flex', gap: 6, alignItems: 'center', paddingTop: 4 }}>
                    {[0,1,2].map(i => (
                      <div key={i} style={{ width: 9, height: 9, borderRadius: '50%', background: '#8e8ea0', animation: `bounce 1.2s ${i*0.2}s ease-in-out infinite` }} />
                    ))}
                  </div>
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </>
        )}
      </div>

      {!isEmpty && (
        <div style={{ borderTop: '1px solid #2f2f2f', padding: '16px 40px 20px', background: '#212121', flexShrink: 0 }}>
          <InputBar ref={textareaRef} value={input} onChange={setInput} onSend={() => send()} loading={loading} disabled={!docId} onClear={() => setMessages([])} />
        </div>
      )}

      <style>{`@keyframes bounce{0%,60%,100%{transform:translateY(0)}30%{transform:translateY(-7px)}}`}</style>
    </div>
  )
}

const InputBar = forwardRef(function InputBar({ value, onChange, onSend, loading, disabled, onClear }, ref) {
  return (
    <div style={{ background: '#2f2f2f', borderRadius: 16, border: '1px solid #3f3f3f', display: 'flex', alignItems: 'flex-end', padding: '10px 12px', gap: 8, direction: 'rtl' }}>
      {onClear && (
        <button onClick={onClear} title="محادثة جديدة" style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#8e8ea0', fontSize: 20, padding: '6px 8px', borderRadius: 8, flexShrink: 0, lineHeight: 1 }}
          onMouseEnter={e => e.currentTarget.style.color = '#ececec'}
          onMouseLeave={e => e.currentTarget.style.color = '#8e8ea0'}
        >✕</button>
      )}
      <textarea
        ref={ref} rows={1} value={value}
        onChange={e => { onChange(e.target.value); e.target.style.height = 'auto'; e.target.style.height = Math.min(e.target.scrollHeight, 160) + 'px' }}
        onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); onSend() } }}
        disabled={disabled || loading}
        placeholder={disabled ? 'ارفع ملفًا أولًا...' : 'اسأل أي شيء... (Enter للإرسال)'}
        style={{ flex: 1, background: 'transparent', border: 'none', outline: 'none', resize: 'none', color: '#ececec', fontFamily: 'Cairo, sans-serif', fontSize: 16, direction: 'rtl', lineHeight: 1.6, padding: '6px 4px', minHeight: 40, maxHeight: 160, overflowY: 'auto' }}
      />
      <button onClick={onSend} disabled={!value.trim() || disabled || loading} style={{ width: 40, height: 40, borderRadius: 10, border: 'none', cursor: 'pointer', flexShrink: 0, background: (!value.trim() || disabled || loading) ? '#3f3f3f' : '#19c37d', color: (!value.trim() || disabled || loading) ? '#8e8ea0' : '#fff', fontSize: 20, display: 'flex', alignItems: 'center', justifyContent: 'center', transition: 'all 0.15s' }}>↑</button>
    </div>
  )
})
