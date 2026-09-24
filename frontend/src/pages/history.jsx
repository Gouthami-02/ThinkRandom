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
                  <div className="mb-3">
                    <span className="badge text-bg-primary me-2">
                      {session.topic_question}
                    </span>
                    <span className="badge text-bg-success">
                      {session.status}
                    </span>
                  </div>

                  <h5 className="fw-bold">
                    Practice #{session.id}
                  </h5>

                  <p className="text-muted mb-2">
                    Score:{" "}
                    <strong>
                      {session.score ?? "Not scored"}
                    </strong>
                  </p>

                  <p className="text-muted mb-2">
                    Duration:{" "}
                    {session.duration_seconds ?? 0} seconds
                  </p>

                  <p className="text-muted small mb-0">
                    {new Date(
                      session.started_at
                    ).toLocaleString()}
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