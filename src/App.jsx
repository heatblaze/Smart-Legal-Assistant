import React, { useState } from "react";
import DocumentUploader from "./components/elements/DocumentUploader";
import SummaryView from "./components/elements/SummaryView";
import QnAChat from "./components/elements/QnAChat";
import RiskHighlights from "./components/elements/RiskHighlights";

function App() {
  const [summaries, setSummaries] = useState([
    "Clause 1: The agreement is valid for 2 years.",
    "Clause 2: Termination requires 30 days notice."
  ]);
  const [risks, setRisks] = useState([
    "Missing indemnification clause.",
    "Ambiguous definition of 'confidential information'."
  ]);
  const [chatHistory, setChatHistory] = useState([]);

  const handleUpload = (file) => {
    alert(`File "${file.name}" uploaded! (Integrate backend here)`);
  };

  const handleAsk = (question) => {
    setChatHistory((prev) => [
      ...prev,
      { question, answer: "Sample answer from AI (integrate backend here)." }
    ]);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-start py-12 px-2 bg-gradient-to-br from-[#101624] to-[#1a2233]">
      <h1 className="text-4xl md:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-tr from-cyan-400 to-blue-600 mb-8 leading-tight pb-2" style={{ marginBottom: '1em' }}>
        A GODDAMN BEST LAWYER!
      </h1>
      <p className="text-cyan-100 text-lg md:text-2xl text-center mb-8 font-medium drop-shadow">
        Hello, Harvey Specter from PSL. Got a case? I will fight if it's a winner.
      </p>
      <DocumentUploader onUpload={handleUpload} />
      <SummaryView summaries={summaries} />
      <RiskHighlights risks={risks} />
      <QnAChat onAsk={handleAsk} chatHistory={chatHistory} />
    </div>
  );
}

export default App;
