import { useEffect, useState } from "react";
import { getDashboard } from "../services/api";

function Dashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        const data = await getDashboard();
        setDashboard(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    loadDashboard();
  }, []);

  if (loading) {
    return (
      <div className="container mt-5 text-center">
        <h4>Loading dashboard...</h4>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-5">
        <div className="alert alert-danger">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="container py-5">

      <div className="mb-5">
        <h1 className="fw-bold">
          ThinkRandom Dashboard
        </h1>

        <p className="text-muted">
          Track your practice and improve your communication skills.
        </p>
      </div>

      <div className="row g-4 mb-5">

        <div className="col-md-4">
          <div className="card shadow-sm border-0 h-100">
            <div className="card-body">
              <p className="text-muted mb-1">
                Total Practices
              </p>
              <h2 className="fw-bold">
                {dashboard.total_practices}
              </h2>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card shadow-sm border-0 h-100">
            <div className="card-body">
              <p className="text-muted mb-1">
                Completed
              </p>
              <h2 className="fw-bold">
                {dashboard.completed_practices}
              </h2>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card shadow-sm border-0 h-100">
            <div className="card-body">
              <p className="text-muted mb-1">
                Average Score
              </p>
              <h2 className="fw-bold">
                {dashboard.average_score}
              </h2>
            </div>
          </div>
        </div>

      </div>

      <div className="row g-4">

        <div className="col-md-7">
          <div className="card shadow-sm border-0">
            <div className="card-body">

              <h4 className="fw-bold mb-4">
                Category Performance
              </h4>

              {dashboard.category_performance.length === 0 ? (
                <p className="text-muted">
                  Complete some practices to see your performance.
                </p>
              ) : (
                dashboard.category_performance.map((item) => (
                  <div
                    key={item.category}
                    className="mb-3"
                  >
                    <div className="d-flex justify-content-between">
                      <span>{item.category}</span>
                      <strong>
                        {item.average_score}
                      </strong>
                    </div>

                    <div className="progress mt-2">
                      <div
                        className="progress-bar"
                        role="progressbar"
                        style={{
                          width: `${item.average_score}%`,
                        }}
                      >
                        {item.average_score}%
                      </div>
                    </div>
                  </div>
                ))
              )}

            </div>
          </div>
        </div>

        <div className="col-md-5">
          <div className="card shadow-sm border-0">
            <div className="card-body">

              <h4 className="fw-bold mb-4">
                Focus Area
              </h4>

              {dashboard.weakest_category ? (
                <>
                  <p className="text-muted">
                    Your current weakest category is:
                  </p>

                  <h3>
                    {dashboard.weakest_category.category}
                  </h3>

                  <p className="mt-3 mb-0">
                    Average score:
                    {" "}
                    <strong>
                      {dashboard.weakest_category.average_score}
                    </strong>
                  </p>
                </>
              ) : (
                <p className="text-muted">
                  Complete a practice session to identify
                  your focus area.
                </p>
              )}

            </div>
          </div>
        </div>

      </div>

    </div>
  );
}

export default Dashboard;