'use client'

import { useState } from 'react'

const handleSubmit = async (file: File | null, jobDescription: string) => {
  if (!file) {
    console.error('No file selected')
    return
  }
}

export default function Home() {
  const [file, setFile] = useState(null)
  const [jobDescription, setJobDescription] = useState('')

  return (
    <main>
      <input onChange={(e) => setFile(e.target.files?.[0])} type="file" id="file-input" name="file-input"/>
      <label htmlFor="file-input">Upload Resume</label>
      <textarea onChange={(e) => setJobDescription(e.target.value)} placeholder="Enter job description"></textarea>
      <button type="submit">Submit</button>
    </main>
  )
}