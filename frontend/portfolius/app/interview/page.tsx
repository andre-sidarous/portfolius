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

    const router = useRouter()
    
    async function handleAnswer() {
        const res = await axios.post('http://localhost:8000/interview/answer', {
            question: questions[currentQuestion],
            answer: answer,
            job_description: sessionStorage.getItem('job_description')
        })
        const newGrade = res.data.grade
        setGrades([...grades, newGrade])
        setGrade(newGrade)

        if (currentQuestion + 1 >= questions.length) {
            const res = await axios.post('http://localhost:8000/interview/final', {
                grades: [...grades, newGrade]
            })
            const finalGrade = res.data.final_grade
            sessionStorage.setItem('final_grade', JSON.stringify(res.data))
            router.push('/interview/result')
        } else {
            setCurrentQuestion(currentQuestion + 1)
            setAnswer('')
        }
    }

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
            <h1>{questions[currentQuestion]}</h1>
            <textarea value={answer} onChange={(e) => setAnswer(e.target.value)}></textarea>
            <button type="submit" onClick={handleAnswer}></button>
        </main>
    )
}