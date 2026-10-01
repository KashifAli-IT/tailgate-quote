import { useEffect, useState } from "react"
import "./App.css"

function App() {
  const [isListening, setIsListening] = useState(false)
  const [backendStatus, setBackendStatus] = useState("Checking...")
  
  useEffect(() => {
    fetch("http://127.0.0.1:8000/health")
      .then((response) => response.json())
      .then(() => setBackendStatus("Backend Connected"))
      .catch(() => setBackendStatus("Backend Offline"))
  }, [])

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>Tailgate Quote</h1>
          <p>Talk through the job. Get the quote. Verify every number.</p>
        </div>

        <span className="connection-status">{backendStatus}</span>
      </header>

      <main className="dashboard">
        <section className="panel voice-panel">
          <div className="panel-header">
            <div>
              <h2>Voice Assistant</h2>
              <p>Talk naturally about the job.</p>
            </div>

            <span className="status">
              {isListening ? "Listening" : "Ready"}
            </span>
          </div>

          <div className="voice-area">
            <button
              className="voice-button"
              onClick={() => setIsListening(!isListening)}
            >
              {isListening ? "Stop Listening" : "Start Listening"}
            </button>

            <p>
              {isListening
                ? "Listening for the technician..."
                : "Voice session is ready."}
            </p>
          </div>

          <div className="transcript">
            <h3>Live Transcript</h3>
            <p className="muted">
              {isListening
                ? "Waiting for speech..."
                : "No conversation yet."}
            </p>
          </div>
        </section>

        <section className="panel quote-panel">
          <div className="panel-header">
            <div>
              <h2>Quote Preview</h2>
              <p>Review the generated quote before sending.</p>
            </div>

            <span className="quote-status">DRAFT</span>
          </div>

          <div className="quote-empty">
            <h3>No quote created yet</h3>
            <p>
              Start a voice session to capture the job requirements and
              generate a quote.
            </p>
          </div>
        </section>

        <section className="panel evidence-panel">
          <div className="panel-header">
            <div>
              <h2>Proof of Hearing</h2>
              <p>See how the AI understood the technician.</p>
            </div>
          </div>

          <div className="evidence-empty">
            <p className="muted">Evidence will appear here.</p>
          </div>
        </section>
      </main>
    </div>
  )
}

export default App