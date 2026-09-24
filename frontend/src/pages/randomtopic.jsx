import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  getRandomTopic,
  startPractice,
} from "../services/api";

function RandomTopic() {
  const navigate = useNavigate();

  const [topic, setTopic] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadTopic = async () => {
    setLoading(true);
    setError("");

    try {
      const data = await getRandomTopic();
      setTopic(data);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTopic();
  }, []);

  if (loading) {
    return (
      <div className="container py-5 text-center">
        <h4>Finding a random topic...</h4>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container py-5">
        <div className="alert alert-danger">
          {error}
        </div>

        <button
          className="btn btn-primary"
          onClick={loadTopic}
        >
          Try Again
        </button>
      </div>
    );
  }
  const handleStartPractice = async () => {
  try {
    const session = await startPractice(topic.id);

    navigate(`/practice/${session.id}`, {
      state: {
        topic: topic,
      },
    });
  } catch (error) {
    setError(error.message);
  }
};

  return (
    <div className="container py-5">

      <div className="text-center mb-5">
        <h1 className="fw-bold">
          Random Topic
        </h1>

        <p className="text-muted">
          Get a topic and start thinking.
        </p>
      </div>

      <div className="row justify-content-center">

        <div className="col-lg-8">

          <div className="card shadow-sm border-0">

            <div className="card-body p-5">

              <div className="mb-4">
                <span className="badge text-bg-primary me-2">
                  {topic.category}
                </span>

                <span className="badge text-bg-secondary me-2">
                  {topic.difficulty}
                </span>

                <span className="badge text-bg-dark">
                  {topic.topic_type}
                </span>
              </div>

              <h2 className="fw-bold mb-4">
                {topic.question}
              </h2>

              <div className="d-flex gap-3 flex-wrap">

                <button
                  className="btn btn-primary"
                  onClick={loadTopic}
                >
                  🎲 Another Topic
                </button>

                <button
                  className="btn btn-outline-secondary"
                  onClick={handleStartPractice}
                >
                  Start Practice
                </button>

              </div>

            </div>

          </div>

        </div>

      </div>

    </div>
  );
}

export default RandomTopic;