import React, { useState } from "react";

type QuestionInputProps = {
  onSubmitQuestion: (question: string) => Promise<void>;
};

const QuestionInput: React.FC<QuestionInputProps> = ({ onSubmitQuestion }) => {
  const [question, setQuestion] = useState("");

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    await onSubmitQuestion(question); // Use the passed function for submission
    setQuestion(""); // Reset the input field after submission
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Type your question here..."
        />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default QuestionInput;
