import { useEffect, useState } from "react"
import "./App.css"

function App() {
  const [isListening, setIsListening] = useState(false)
  const [backendStatus, setBackendStatus] = useState("Checking...")
  const [quote, setQuote] = useState<any>(null)

  useEffect(() => {
    fetch("http://127.0.0.1:8000/health")
      .then((response) => response.json())
      .then(() => setBackendStatus("Backend Connected"))
      .catch(() => setBackendStatus("Backend Offline"))
    
    fetch("http://127.0.0.1:8000/quotes/Q-0001")
      .then((response) => response.json())
      .then((data) => setQuote(data))
      .catch(() => setQuote(null)) 
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

            <span className="quote-status">{quote?.status ?? "DRAFT"}</span>
          </div>

          <div className="quote-empty">
            {quote ? (
              <>
                <h3>{quote.customer_name}</h3>
                <p>Quote ID: {quote.quote_id}</p>
                <p>Status: {quote.status}</p>
                {quote.items?.map((item: any) => (
                  <div key={item.sku}>
                    <p>
                      {item.sku} — {item.quantity} {item.price_evidence?.unit}
                    </p>
                    <p>${item.subtotal.toFixed(2)}</p>
                  </div>
                ))}

                <p>Total: ${quote.total.toFixed(2)}</p>
              </>
            ) : (
              <>
                <h3>No quote created yet</h3>
                <p>Loading quote...</p>
              </>
            )}
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
            {quote?.items?.map((item: any) => (
              <div key={item.sku}>
                <p>
                  <strong>Source:</strong> {item.evidence?.source_text}
                </p>

                <p>
                  <strong>Quantity:</strong> {item.evidence?.quantity_evidence}
                </p>
            
                <p>
                  <strong>Product:</strong> {item.evidence?.product_evidence}
                </p>
            
                <p>
                  <strong>Price:</strong> {item.price_evidence?.sku} — $
                  {item.price_evidence?.unit_price.toFixed(2)} /{" "}
                  {item.price_evidence?.unit}
                </p>
            
                <p>
                  <strong>Calculation:</strong> {item.calculation}
                </p>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  )
}

export default App