import { useState, useEffect } from 'react'
import { uploadFile, fetchDocuments } from '../lib/api'

export default function Sidebar({ selectedDoc, onSelectDoc }) {
  const [docs, setDocs]           = useState([])
  const [uploading, setUploading] = useState(false)
  const [msg, setMsg]             = useState(null)

  const loadDocs = async () => {
    try {
      const d = await fetchDocuments()
      setDocs(d.documents || [])
      return d.documents || []
    } catch (e) {
      console.error('Failed to load documents:', e)
      return []
    }
  }

  useEffect(() => { loadDocs() }, [])

  const handleFile = async (file) => {
    if (!file) return
    setUploading(true); setMsg(null)
    try {
      const data = await uploadFile(file)
      setMsg({ ok: true, text: data.status === 'skipped' ? 'الملف موجود مسبقًا' : `✅ تم رفع ${data.chunks_added} جزء` })
      const fresh = await loadDocs()
      const up = fresh.find(d => d.doc_id === data.doc_id)
      if (up) onSelectDoc(up)
    } catch (e) {
      setMsg({ ok: false, text: '❌ ' + e.message })
    } finally { setUploading(false) }
  }

  return (
    <div style={{
      width: 260, display: 'flex', flexDirection: 'column',
      background: '#171717', height: '100vh', direction: 'rtl',
      borderLeft: '1px solid #2f2f2f', flexShrink: 0,
    }}>
      {/* Logo */}
      <div style={{ padding: '18px 16px', display: 'flex', alignItems: 'center', gap: 10 }}>
        <div style={{ width: 36, height: 36, borderRadius: 10, background: '#2f2f2f', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 18 }}>
          🎓
        </div>
        <span style={{ fontSize: 15, fontWeight: 700, color: '#ececec' }}>مساعد الطالب</span>
      </div>

      {/* Upload button */}
      <div style={{ padding: '0 10px 8px' }}>
        <label style={{
          display: 'flex', alignItems: 'center', gap: 10,
          padding: '10px 14px', borderRadius: 10, cursor: 'pointer',
          color: '#ececec', fontSize: 14, fontWeight: 500,
          transition: 'background 0.15s',
          background: uploading ? '#2f2f2f' : 'transparent',
        }}
          onMouseEnter={e => e.currentTarget.style.background = '#2f2f2f'}
          onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
        >
          <span style={{ fontSize: 18 }}>{uploading ? '⏳' : '+'}</span>
          <span>{uploading ? 'جاري الرفع...' : 'رفع ملف جديد'}</span>
          <input type="file" accept=".pdf,.pptx,.docx" style={{ display: 'none' }}
            onChange={e => handleFile(e.target.files[0])} disabled={uploading} />
        </label>

        {msg && (
          <div style={{
            margin: '4px 4px 0', padding: '7px 12px', borderRadius: 8, fontSize: 12,
            background: msg.ok ? 'rgba(34,197,94,0.1)' : 'rgba(239,68,68,0.1)',
            color: msg.ok ? '#86efac' : '#fca5a5',
          }}>
            {msg.text}
          </div>
        )}
      </div>

      {/* Divider */}
      <div style={{ height: 1, background: '#2f2f2f', margin: '4px 0' }} />

      {/* Files list */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '8px 10px' }}>
        {docs.length > 0 && (
          <p style={{ fontSize: 11, color: '#8e8ea0', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.07em', padding: '6px 8px 8px' }}>
            الملفات
          </p>
        )}
        {docs.map(doc => (
          <button key={doc.doc_id} onClick={() => onSelectDoc(doc)} style={{
            width: '100%', display: 'flex', alignItems: 'center', gap: 10,
            padding: '9px 12px', borderRadius: 8, border: 'none', cursor: 'pointer',
            textAlign: 'right', fontFamily: 'Cairo, sans-serif', fontSize: 14,
            background: selectedDoc?.doc_id === doc.doc_id ? '#2f2f2f' : 'transparent',
            color: selectedDoc?.doc_id === doc.doc_id ? '#ececec' : '#8e8ea0',
            transition: 'all 0.15s', marginBottom: 2,
          }}
            onMouseEnter={e => { if (selectedDoc?.doc_id !== doc.doc_id) e.currentTarget.style.background = '#212121' }}
            onMouseLeave={e => { if (selectedDoc?.doc_id !== doc.doc_id) e.currentTarget.style.background = 'transparent' }}
          >
            <span style={{ fontSize: 15, flexShrink: 0 }}>📄</span>
            <span style={{ flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              {doc.filename}
            </span>
          </button>
        ))}
      </div>
    </div>
  )
}
