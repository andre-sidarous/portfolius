'use client'

import { useEffect, useState } from 'react'

export default function ResultPage() {
    const [data, setData] = useState<{ final_assessment: string }>({ final_assessment: '' })
    useEffect(() => {
        const final_result = sessionStorage.getItem('final_grade')
        const data = JSON.parse(final_result || '{}')
        setData(data)
    }, [])

    return (
        <div className="flex flex-col items-center justify-center h-screen">
            <h1 className="text-2xl font-bold">Interview Results</h1>
            <p className="text-lg">Your interview has been completed.</p>
            <p className="text-lg">Final Result: {data.final_assessment}</p>
        </div>
    )
}