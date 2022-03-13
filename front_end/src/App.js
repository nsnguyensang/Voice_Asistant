import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition'
import { Container, Typography, Button } from '@mui/material'
import { useState } from 'react'
import BasicCard from './components/BasicCard'
import { useSpeechSynthesis } from 'react-speech-kit'

function App() {
  const [questions, setQuestions] = useState([])
  const { speak } = useSpeechSynthesis()

  const {
    transcript,
    listening,
    browserSupportsSpeechRecognition,
    resetTranscript
  } = useSpeechRecognition();

  const startListening = async () => {
    await SpeechRecognition.startListening({ continuous: true });
    resetTranscript()
  };

  const stopListening = async () => {
    console.log("listening "+transcript)
    SpeechRecognition.stopListening()
    let currQuestion = transcript
    resetTranscript()
    let data = {'answer': 'I don\'t know'}
    try { 
      data = await fetch(`http://127.0.0.1:8000/?question="${currQuestion}"`).then(res=>res.json())
    } catch (err) {
      console.log(err)
    }
    setQuestions([...questions, {bot: 1, content:data['answer']}, {bot: 0, content: currQuestion}])
    speak({text: data['answer']})
  }
  if (!browserSupportsSpeechRecognition) {
    return <span>Browser doesn't support speech recognition.</span>;
  }

  return (
    <Container>
      <Typography variant="h6"  sx={{mb: 1}}>{listening ? 'I\'m hearing....' : 'Hi, my name is Hannah.'}</Typography>
      <Button variant="contained"
        onTouchStart={startListening}
        onMouseDown={startListening}
        onTouchEnd={stopListening}
        onMouseUp={stopListening}
        sx={{mb: 2, color :"black", backgroundColor: "blanchedalmond"}}
      >Hold to talk</Button>
      <BasicCard user={`Question: ` + transcript}></BasicCard>
      {questions.slice(0).reverse().map((question) => {
        if (question.content !== "\n\n" && question.content.length !== 0) {
          return question.bot === 0 
          ? <BasicCard user="User" content={question.content} color="error.main"></BasicCard>
          : <BasicCard user="Hannad" content={question.content} color="green"></BasicCard>
      }})} 
    </Container>
  )
}

export default App