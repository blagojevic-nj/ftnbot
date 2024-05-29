import { useState } from "react";

export const Result = ({ result, deleteContext, updateContext }) => {
  const [context, setContext] = useState(result.context);

  return (
    <div className="result">
      <p
        contentEditable
        className="result-text"
        id="resultText"
        spellCheck="false"
        onInput={(e) => setContext(e.target.textContent)}
      >
        {result.context}
      </p>
      <div className="result-footer">
        <div>
          <button
            className="delete-button"
            onClick={() => deleteContext(result.id)}
          >
            Obriši
          </button>
          <button
            className="delete-button"
            onClick={() => updateContext({ id: result.id, text: context })}
          >
            Ažuriraj
          </button>
        </div>
        <span className="score">Sličnost: {result.score}</span>
      </div>
    </div>
  );
};

export default Result;
