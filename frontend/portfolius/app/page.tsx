'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import axios from 'axios'

export default function Home() {
  const router = useRouter()
  const [file, setFile] = useState(null)
  const [jobDescription, setJobDescription] = useState('')

  const handleSubmit = async () => {
    if (!file) {
      console.error('No file selected')
      return
    }
    try {
      const formData = new FormData()
      formData.append('file', file)
      const parseRes = await axios.post('http://localhost:8000/resume/parse', formData)

      const scoreRes = await axios.post('http://localhost:8000/resume/score', {
      resume_text: parseRes.data.text,
      job_description: jobDescription
      })

      sessionStorage.setItem('score_result', JSON.stringify(scoreRes.data))
      sessionStorage.setItem('resume_text', parseRes.data.text)
      sessionStorage.setItem('job_description', jobDescription)
      router.push('/dashboard')
    } catch (error) {
      console.error('Error submitting data:', error)
    }
  }

  return (
    <main>
      <input onChange={(e) => setFile(e.target.files?.[0])} type="file" id="file-input" name="file-input"/>
      <label htmlFor="file-input">Upload Resume</label>
      <textarea onChange={(e) => setJobDescription(e.target.value)} placeholder="Enter job description"></textarea>
      <button onClick={handleSubmit}>Submit</button>
    </main>
  )
}