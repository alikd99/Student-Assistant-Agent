const BASE = '/api'

async function req(method, path, body, isForm = false) {
  const opts = { method }
  if (body) {
    if (isForm) {
      opts.body = body
    } else {
      opts.headers = { 'Content-Type': 'application/json' }
      opts.body = JSON.stringify(body)
    }
  }
  const res = await fetch(BASE + path, opts)
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || `HTTP ${res.status}`)
  }
  return res.json()
}

export const uploadFile  = (file) => {
  const fd = new FormData()
  fd.append('file', file)
  return req('POST', '/upload', fd, true)
}

export const fetchDocuments       = ()               => req('GET',  '/documents')
export const askQuestion          = (question, docId) => req('POST', '/ask',            { question, doc_id: docId })
export const summarize            = (docId, language) => req('POST', '/summarize',       { doc_id: docId, language })
export const generateFlashcards   = (docId)           => req('POST', '/flashcards',      { doc_id: docId })
export const generateExamQuestions= (docId)           => req('POST', '/exam-questions',  { doc_id: docId })
