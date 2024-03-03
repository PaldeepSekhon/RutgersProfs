import React, { useState } from "react";

type ResponseDisplayProps = {
  response: string;
};

const ResponseDisplay: React.FC<ResponseDisplayProps> = ({ response }) => {
  return (
    <div className="response-display">{response && <p>{response}</p>}</div>
  );
};

export default ResponseDisplay;
