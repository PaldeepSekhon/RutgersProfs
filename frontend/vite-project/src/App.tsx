import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import QuestionInput from "./components/QuestionInput";
import ResponseDisplay from "./components/ResponseDisplay";
import "./index.css";

function App() {
  const [response, setResponse] = useState("");

  // Function to handle submission and fetch response
  const handleQuestionSubmit = async (question: string) => {
    try {
      const response = await fetch("/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: question }),
      });
      if (!response.ok) throw new Error("Network response was not ok");
      const data = await response.json();
      setResponse(data);
    } catch (error) {
      console.error(
        "There has been a problem with your fetch operation:",
        error
      );
      setResponse("Failed to fetch response.");
    }
  };

  return (
    <Router>
      <div className="App">
        <header>
          <h1>Find your Professor</h1>
        </header>
        <Routes>
          <Route
            path="/"
            element={
              <>
                <QuestionInput onSubmitQuestion={handleQuestionSubmit} />
                <ResponseDisplay response={response} />
              </>
            }
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
