import Result from "./Result";
import { deleteContext, updateContext } from "../../services/AdminService";

export const Results = ({ results, setResults }) => {
  const deleteCon = (id) => {
    deleteContext(id)
      .then((res) => {
        setResults(results.filter((r) => r.id != id));
      })
      .catch((err) => {});
  };

  const updateCon = (con) => {
    updateContext(con)
      .then((res) => {})
      .catch((err) => {});
  };
  return (
    <div className="results">
      {results.length > 0 && (
        <>
          <div className="results-list">
            {results.map((res) => {
              return (
                <Result
                  key={res.id}
                  result={res}
                  deleteContext={deleteCon}
                  updateContext={updateCon}
                ></Result>
              );
            })}
          </div>
        </>
      )}
    </div>
  );
};
