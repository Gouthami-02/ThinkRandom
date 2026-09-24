const API_BASE_URL = "http://127.0.0.1:8000/api";

export async function loginUser(username, password) {
  const response = await fetch(`${API_BASE_URL}/auth/login/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username,
      password,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Login failed. Please check your credentials."
    );
  }

  return data;
}

export async function registerUser(username, email, password) {
  const response = await fetch(`${API_BASE_URL}/auth/register/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username,
      email,
      password,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Registration failed."
    );
  }

  return data;
}

export async function getDashboard() {
  const token = localStorage.getItem("token");

  const response = await fetch(
    "http://127.0.0.1:8000/api/analytics/dashboard/",
    {
      method: "GET",
      headers: {
        Authorization: `Token ${token}`,
      },
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to load dashboard."
    );
  }

  return data;
}

export async function getRandomTopic() {
  const token = localStorage.getItem("token");

  const response = await fetch(
    "http://127.0.0.1:8000/api/topics/random/",
    {
      method: "GET",
      headers: {
        Authorization: `Token ${token}`,
      },
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to load random topic."
    );
  }

  return data;
}
export async function startPractice(topicId) {
  const token = localStorage.getItem("token");

  const response = await fetch(
    "http://127.0.0.1:8000/api/practice/sessions/",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`,
      },
      body: JSON.stringify({
        topic: topicId,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to start practice."
    );
  }

  return data;
}
export async function completePractice(
  sessionId,
  durationSeconds,
  answer,
  notes,
  score
) {
  const token = localStorage.getItem("token");

  const response = await fetch(
    `http://127.0.0.1:8000/api/practice/sessions/${sessionId}/complete/`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`,
      },
      body: JSON.stringify({
        duration_seconds: durationSeconds,
        answer: answer,
        notes: notes,
        score: score,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to complete practice."
    );
  }

  return data;
}
export async function generateSpeechAnalysis(sessionId) {
  const token = localStorage.getItem("token");

  const response = await fetch(
    `http://127.0.0.1:8000/api/practice/sessions/${sessionId}/analyze/`,
    {
      method: "POST",
      headers: {
        Authorization: `Token ${token}`,
      },
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to generate AI analysis."
    );
  }

  return data;
}

export async function getPracticeHistory() {
  const token = localStorage.getItem("token");

  const response = await fetch(
    "http://127.0.0.1:8000/api/practice/history/",
    {
      method: "GET",
      headers: {
        Authorization: `Token ${token}`,
      },
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Failed to load practice history."
    );
  }

  return data;
}