import React from "react";
import Card from "../ui/Card";
import Button from "../ui/Button";

const RiskHighlights = ({ risks }) => {
  if (!risks || risks.length === 0) return null;
  return (
    <div className="w-full max-w-2xl mt-8">
      <h2 className="text-xl font-semibold text-pink-400 mb-4">Potential Legal Risks</h2>
      <div className="grid gap-4 mb-4">
        {risks.map((risk, idx) => (
          <Card key={idx} className="border-pink-500 border-l-4">
            <div className="text-pink-200">{risk}</div>
          </Card>
        ))}
      </div>
      {/* Add the glowing button here */}
      <Button glow>Download Risks</Button>
    </div>
  );
};

export default RiskHighlights;
