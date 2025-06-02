import React, { useState } from "react";
import Card from "../ui/Card";
import Button from "../ui/Button";

const SummaryView = () => {
  const [summaries, setSummaries] = useState([]);
  const [inputText, setInputText] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSummarize = async () => {
    if (!inputText.trim()) return;
    setLoading(true);
    try {
      const response = await fetch("/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: inputText }),
      });
      const data = await response.json();
      setSummaries([data.summary]);
    } catch (error) {
      setSummaries(["Error: Could not fetch summary."]);
    }
    setLoading(false);
  };

  return (
    <div className="w-full max-w-2xl mt-8">
      <h2 className="text-xl font-semibold text-cyan-200 mb-4">Key Clauses Summary</h2>
      <textarea
        className="w-full p-2 mb-4 rounded"
        rows={6}
        placeholder="Paste your legal document here"
        value={inputText}
        onChange={e => setInputText(e.target.value)}
      />
      <Button glow className="mb-4" onClick={handleSummarize} disabled={loading}>
        {loading ? "Summarizing..." : "Summarize"}
      </Button>
      <div className="grid gap-4 mb-4">
        {summaries && summaries.length > 0 && summaries.map((summary, idx) => (
          <Card key={idx}>
            <div className="text-white">{summary}</div>
          </Card>
        ))}
      </div>
      {summaries.length > 0 && (
        <Button glow className="mt-4" onClick={() => {
          // Download summary as text file
          const blob = new Blob([summaries.join("\n\n")], { type: "text/plain" });
          const url = URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = "summary.txt";
          a.click();
          URL.revokeObjectURL(url);
        }}>
          Download Summary
        </Button>
      )}
    </div>
  );
};

export default SummaryView;
