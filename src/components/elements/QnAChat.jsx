import React, { useState } from "react";
import Card from "../ui/Card";
import Input from "../ui/Input";
import Button from "../ui/Button";

export default function QnAChat({ contextText = "" }) {
  const [question, setQuestion] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim()) return;
    setLoading(true);
    try {
      const response = await fetch("/qa", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, context: contextText }),
      });
      const data = await response.json();
      setChatHistory(prev => [
        ...prev,
        { question, answer: data.answer }
      ]);
    } catch (error) {
      setChatHistory(prev => [
        ...prev,
        { question, answer: "Error: Could not fetch answer." }
      ]);
    }
    setQuestion("");
    setLoading(false);
  };

  return (
    <Card className="w-full max-w-lg mt-8">
      <h2 className="text-xl font-semibold text-cyan-200 mb-2">Ask Legal Questions</h2>
      <div className="flex gap-2 mb-4">
        <Input
          type="text"
          placeholder="Type your question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleAsk()}
          disabled={loading}
        />
        <Button onClick={handleAsk} disabled={loading}>
          {loading ? "Asking..." : "Ask"}
        </Button>
      </div>
      <div className="max-h-64 overflow-y-auto space-y-2">
        {chatHistory.map((item, idx) => (
          <div key={idx}>
            <div className="text-cyan-300 font-semibold">Q: {item.question}</div>
            <div className="text-white ml-2">A: {item.answer}</div>
          </div>
        ))}
      </div>
    </Card>
  );
}
