'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import axios from 'axios'

export default function Interview() {
    const [questions, setQuestions] = useState([])
    const [currentQuestion, setCurrentQuestion] = useState(0)
    const [answer, setAnswer] = useState('')
    const [grades, setGrades] = useState([])
    const [grade, setGrade] = useState(null)

    useEffect(() => {
        const fetchQuestions = async () => {
            try {
                const resumeText = sessionStorage.getItem('resume_text')
                const jobDescription = sessionStorage.getItem('job_description')
                const res = await axios.post('http://localhost:8000/interview/start', {
                    resume_text: resumeText,
                    job_description: jobDescription
                })
                setQuestions(res.data.questions)
            } catch (error) {
                console.error('Error fetching questions:', error)
            }
        }
        fetchQuestions()
    }, [])

    return (
        <main>

        </main>
    )
}