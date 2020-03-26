import React, {useState, useEffect} from 'react'
import Quote from "../Quote";
import axios from 'axios'

function Event_Stats() {
  const [quote, setQuote] = useState('quote')


  const getQuote = () => {
    
    axios.get('http://localhost:8100/event/stats')
      .then(json => {
          json
        
      })
  }

  useEffect(() => {
    setTimeout(getQuote, 3000)
  }, [quote])


  return (
    <Quote quote={quote} quoter={""} />
  )
}

export default Event_Stats