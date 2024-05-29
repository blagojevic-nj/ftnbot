import { useState } from "react";
import { queryDatabase, addContext } from "../../services/AdminService";

export const Prompt = ({ results, setResults }) => {
  const [query, setQuery] = useState("");

  const queryDb = () => {
    queryDatabase(query)
      .then((res) => {
        setResults(res.data);
        setQuery("");
      })
      .catch((err) => {});
  };

  const addCon = () => {
    addContext(query)
      .then((res) => {
        setResults(res.data);
      })
      .catch((err) => {});
  };

  return (
    <div className="prompt">
      <textarea onChange={(e) => setQuery(e.target.value)} spellCheck="false">
        {query}
      </textarea>
      <div className="buttons">
        <button className="query-button" onClick={queryDb}>
          Pretraži
        </button>
        <button className="add-button" onClick={addCon}>
          Dodaj
        </button>
      </div>
    </div>
  );
};
