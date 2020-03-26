import React, {useState, useEffect} from 'react'
import logo from './logo.jpg';
import './App.css';
import Value from "./Value"
import axios from 'axios'

document.title = 'League Champion Stats'


function App() {

  const [value, setValue] = useState('value1')
  const [value2, setValue2] = useState('value2')
  const [value3, setValue3] = useState('value3')
  const [value4, setValue4] = useState('value4')
  const [value5, setValue5] = useState('value5')



  const getValue = () => {
    axios.get('http://127.0.0.1:8100/event/stats')
      .then(json => {
        console.log(json.data)
        setValue(json.data.num_champion_ionia)
        setValue2(json.data.num_champion_piltover)
      })
    axios.get('http://127.0.0.1:8110/ionia/history?Offset=8')
    .then(json => {
      setValue3(json.data.champ_name)
    })
    axios.get('http://127.0.0.1:8110/piltover/history')
    .then(json => {
      console.log(json.data)
      setValue4(json.data.champ_name)
    })
    setValue5(Date())
  }



  useEffect(() => {
    getValue();
    setInterval(getValue, 2000)
  }, [value])


  return (
    <div style={{border: "2px solid black", textAlign: "center", width: 500, margin: "auto"}}>
      <img alt="League Logo" height="100" width="100" src={require('./logo.jpg')}></img>
      <Value value={value} name={"Ionian Champion count"} />
      <Value value={value2} name={"Piltover Champion count"} />
      <Value value={value3} name={"8th Champ name"} />
      <Value value={value4} name={"First Piltover champion"} />
      <Value value={value5} name={"Last Updated"} />
    </div>
  )
}

export default App
