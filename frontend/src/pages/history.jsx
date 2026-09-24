import { useEffect, useState } from "react";
import { getPracticeHistory } from "../services/api";

function History() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadHistory = async () => {
      try {
        const data = await getPracticeHistory();

        setHistory(data);
        
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    loadHistory();
  }, []);

  if (loading) {
    return (
      <div className="container py-5 text-center">
        <h4>Loading practice history...</h4>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container py-5">
        <div className="alert alert-danger">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="container py-5">
      <div className="mb-5">
        <h1 className="fw-bold">Practice History</h1>
        <p className="text-muted">
          Review your previous practice sessions and scores.
        </p>
      </div>

      {history.length === 0 ? (
        <div className="card shadow-sm border-0">
          <div className="card-body p-5 text-center">
            <h4>No practice history yet.</h4>
            <p className="text-muted">
              Complete a practice session to see it here.
            </p>
          </div>
        </div>
      ) : (
        <div className="row g-4">
{history.map((session) => (
  <div
    className="col-md-6 col-lg-4"
    key={session.id}
  >
    <div className="card shadow-sm border-0 h-100">
      <div className="card-body p-4">

        <div className="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-3">
          <h5 className="fw-bold mb-0">
            Practice #{session.id}
          </h5>

          <span className="badge text-bg-success">
            {session.status}
          </span>
        </div>

        <p className="fw-semibold mb-4 text-break">
          {session.topic_question}
        </p>

        <div className="row g-3 mb-4">
          <div className="col-6">
            <div className="border rounded p-3">
              <small className="text-muted d-block">
                Score
              </small>
              <strong className="fs-5">
                {session.score ?? "Not scored"}
              </strong>
            </div>
          </div>

          <div className="col-6">
            <div className="border rounded p-3">
              <small className="text-muted d-block">
                Duration
              </small>
              <strong className="fs-5">
                {session.duration_seconds ?? 0} sec
              </strong>
            </div>
          </div>
        </div>

        <p className="text-muted small mb-0">
          {new Date(session.started_at).toLocaleString()}
        </p>

      </div>
    </div>
  </div>
))}
        </div>
      )}
      </div>
  );
}

      

export default History;