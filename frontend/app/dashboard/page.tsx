'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function Dashboard() {
    const [scoreResult, setScoreResult] = useState(null)
    const router = useRouter()

    useEffect(() => {
        const result = sessionStorage.getItem('score_result')
        if (result) {
            setScoreResult(JSON.parse(result))
        }
    }, [])

    return (
        <main>
            <h1>Dashboard</h1>
            {scoreResult ? (
                <div>
                    <h2>Score Result</h2>
                    <p>Score: {scoreResult.ats_score}</p>
                    <p>Strengths: {scoreResult.strengths.map((s, i) => <li key={i}>{s}</li>)}</p>
                    <p>Weaknesses: {scoreResult.gaps.map((g, i) => <li key={i}>{g}</li>)}</p>
                    <p>Recommendations: {scoreResult.rewrite_suggestions.map((r, i) => <li key={i}>{r}</li>)}</p>
                </div>
            ) : (
                <p>No score result available. Please submit your resume and job description first.</p>
            )}
            <button onClick={() => {
                router.push('/interview')
            }}>
                Take Interview
            </button>
        </main>
    )
}