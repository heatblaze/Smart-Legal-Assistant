import React, { useRef } from "react";
import Card from "../ui/Card";
import Input from "../ui/Input";
import Button from "../ui/Button";

export default function DocumentUploader({ onUpload }) {
  const fileInput = useRef();

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      onUpload(e.target.files[0]);
    }
  };

  return (
    <Card className="flex flex-col items-center gap-4 w-full max-w-md">
      <h2 className="text-2xl font-bold text-cyan-300 mb-2">Upload Legal Document</h2>
      <Input
        type="file"
        accept=".pdf,.txt"
        onChange={handleFileChange}
        className="mb-2"
        ref={fileInput}
      />
      <Button onClick={() => fileInput.current && fileInput.current.click()}>
        Select File
      </Button>
    </Card>
  );
}

