import { useState } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { completePractice,generateSpeechAnalysis, } from "../services/api";

function Practice() {
  const { sessionId } = useParams();
  const location = useLocation();
  const navigate = useNavigate();

  const topic = location.state?.topic;

  const [answer, setAnswer] = useState("");
  const [notes, setNotes] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [analysis, setAnalysis] = useState(null);

  const handleComplete = async () => {
    if (!answer.trim()) {
      setError("Please enter your answer before completing practice.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      await completePractice(
        sessionId,
        120,
        answer,
        notes,
        null
      );
      const analysisResult = await generateSpeechAnalysis(sessionId);

      setAnalysis(analysisResult);


    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  if (!topic) {
    return (
      <div className="container py-5">
        <div className="alert alert-warning">
          Practice topic information is not available.
        </div>

        <button
          className="btn btn-primary"
          onClick={() => navigate("/random-topic")}
        >
          Back to Random Topic
        </button>
      </div>
    );
  }

  return (
    <div className="container py-5">

      <div className="text-center mb-5">
        <h1 className="fw-bold">
          Practice Session
        </h1>

        <p className="text-muted">
          Take a moment to think, then write your response.
        </p>
      </div>

      <div className="row justify-content-center">

        <div className="col-lg-9">

          <div className="card shadow-sm border-0 mb-4">
            <div className="card-body p-4">

              <div className="mb-3">

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

              <h2 className="fw-bold">
                {topic.question}
              </h2>

            </div>
          </div>

          {error && (
            <div className="alert alert-danger">
              {error}
            </div>
          )}

          <div className="card shadow-sm border-0 mb-4">
            <div className="card-body p-4">

              <h4 className="fw-bold mb-3">
                Your Answer
              </h4>

              <textarea
                className="form-control"
                rows="8"
                placeholder="Write your response here..."
                value={answer}
                onChange={(event) =>
                  setAnswer(event.target.value)
                }
              />

              <div className="form-text">
                Explain your position clearly and support it
                with relevant points or examples.
              </div>

            </div>
          </div>

          <div className="card shadow-sm border-0 mb-4">
            <div className="card-body p-4">

              <h4 className="fw-bold mb-3">
                Notes
              </h4>

              <textarea
                className="form-control"
                rows="3"
                placeholder="Add any notes about your practice..."
                value={notes}
                onChange={(event) =>
                  setNotes(event.target.value)
                }
              />

            </div>
          </div>

          {analysis && (
  <div className="card shadow-sm border-0 mb-4">
    <div className="card-body p-4">
      <h4 className="fw-bold mb-4">
        AI Communication Analysis
      </h4>

      <div className="row g-3">
        <div className="col-md-3">
          <div className="border rounded p-3 text-center">
            <div className="text-muted">Clarity</div>
            <h3 className="fw-bold">
              {analysis.clarity_score}
            </h3>
          </div>
        </div> 

        <div className="col-md-3">
          <div className="border rounded p-3 text-center">
            <div className="text-muted">Structure</div>
            <h3 className="fw-bold">
              {analysis.structure_score}
            </h3>
          </div>
        </div>

        <div className="col-md-3">
          <div className="border rounded p-3 text-center">
            <div className="text-muted">Vocabulary</div>
            <h3 className="fw-bold">
              {analysis.vocabulary_score}
            </h3>
          </div>
        </div>

        <div className="col-md-3">
          <div className="border rounded p-3 text-center">
            <div className="text-muted">Fluency</div>
            <h3 className="fw-bold">
              {analysis.fluency_score}
            </h3>
          </div>
        </div>
      </div>

      <div className="mt-4">
        <p className="mb-2">
          <strong>Filler Words:</strong>{" "}
          {analysis.filler_word_count}
        </p>

        <h5 className="fw-bold">Feedback</h5>

        <p className="text-muted mb-0">
          {analysis.feedback}
        </p>
      </div>
    </div>
  </div>
)}

          <div className="d-flex gap-3">

            <button
              className="btn btn-outline-secondary"
              onClick={() => navigate("/random-topic")}
            >
              Back
            </button>

            <button
              className="btn btn-primary"
              onClick={handleComplete}
              disabled={loading}
            >
              {loading
                ? "Completing..."
                : "Complete Practice"}
            </button>

          </div>

        </div>

      </div>

    </div>
  );
}

export default Practice;