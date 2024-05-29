import { Prompt } from "./Prompt";
import { Results } from "./Results";

import { useState } from "react";

const Admin = () => {
  const [results, setResults] = useState([]);

  return (
    <>
      <div className="container">
        <div id="admin-container">
          <div className="admin">
            <Prompt results={results} setResults={setResults} />
            <Results results={results} setResults={setResults} />
          </div>
        </div>
      </div>
    </>
  );
};

export default Admin;
