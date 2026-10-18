const main = document.querySelector("#main-content");
const pageLabel = document.querySelector("#page-label");
const toast = document.querySelector("#toast");
const state = {
  page: "dashboard",
  file: null,
  analysis: null,
  formError: "",
  loading: false,
};

const pageNames = {
  dashboard: "Overview",
  analyze: "New analysis",
  history: "Analysis history",
  results: "Analysis report",
};

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  })[character]);
}

function formatDate(value) {
  if (!value) return "Date unavailable";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "Date unavailable";
  return new Intl.DateTimeFormat(undefined, { month: "short", day: "numeric", year: "numeric" }).format(date);
}

function scoreClass(score) {
  if (score >= 70) return "";
  return score >= 45 ? "medium" : "low";
}

function showToast(message, isError = false) {
  toast.textContent = message;
  toast.classList.toggle("is-error", isError);
  toast.classList.add("is-visible");
  window.clearTimeout(showToast.timeout);
  showToast.timeout = window.setTimeout(() => toast.classList.remove("is-visible"), 3600);
}

async function api(path, options = {}) {
  let response;
  try {
    response = await fetch(path, options);
  } catch {
    throw new Error("Cannot reach the API. Start the backend server and try again.");
  }
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = payload.detail;
    const message = typeof detail === "string" ? detail : "The request could not be completed.";
    throw new Error(message);
  }
  return payload;
}

function setPage(page) {
  state.page = page;
  pageLabel.textContent = pageNames[page] || pageNames.dashboard;
  document.querySelectorAll(".nav-item").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.page === (page === "results" ? "history" : page));
  });
  if (page === "dashboard") void renderDashboard();
  if (page === "analyze") renderAnalyze();
  if (page === "history") void renderHistory();
  if (page === "results") renderResult();
}

function renderDashboard() {
  main.innerHTML = `
    <section class="page-heading greeting">
      <div><div class="eyebrow">YOUR CAREER WORKSPACE</div><h1>Make your next move count.</h1>
      <p class="intro">Get a clearer picture of how your resume lines up with the role you want, and find practical ways to strengthen it.</p></div>
      <button class="button button-primary" type="button" data-page="analyze"><span aria-hidden="true">＋</span> Start an analysis</button>
    </section>
    <section class="stats-grid" aria-label="Analysis statistics">
      <article class="stat-card"><span class="stat-icon" aria-hidden="true">▤</span><div class="stat-label">Resumes reviewed</div><div class="stat-value" id="stat-total">—</div><div class="stat-foot">Saved in your workspace</div></article>
      <article class="stat-card"><span class="stat-icon" aria-hidden="true">◉</span><div class="stat-label">Average match score</div><div class="stat-value" id="stat-average">—</div><div class="stat-foot">Across all your analyses</div></article>
      <article class="stat-card"><span class="stat-icon" aria-hidden="true">↗</span><div class="stat-label">Best match score</div><div class="stat-value" id="stat-highest">—</div><div class="stat-foot">Your strongest role match</div></article>
    </section>
    <section class="dashboard-grid">
      <article class="panel">
        <div class="panel-heading"><h2>Recent analyses</h2><button class="text-button" type="button" data-page="history">View all <span aria-hidden="true">→</span></button></div>
        <div class="recent-list" id="recent-list"><div class="loading-state">Loading your analyses…</div></div>
      </article>
      <article class="panel quick-card">
        <span class="quick-icon" aria-hidden="true">✳</span>
        <h2>A better fit starts with a clear picture.</h2>
        <p>Compare your resume with a job description to see your strengths, skill gaps, and ideas for your next edit.</p>
        <button class="button button-primary button-small" type="button" data-page="analyze">Analyze a resume <span aria-hidden="true">→</span></button>
      </article>
    </section>`;

  Promise.all([api("/api/dashboard/stats"), api("/api/history")])
    .then(([stats, records]) => {
      if (state.page !== "dashboard") return;
      document.querySelector("#stat-total").textContent = stats.total_analyses;
      document.querySelector("#stat-average").textContent = `${stats.average_score}%`;
      document.querySelector("#stat-highest").textContent = `${stats.highest_score}%`;
      const recent = records.slice(0, 5);
      const list = document.querySelector("#recent-list");
      list.innerHTML = recent.length ? recent.map((record) => `
        <div class="recent-row">
          <div class="recent-file"><span class="file-mark">CV</span><div class="file-details">
            <strong title="${escapeHtml(record.filename)}">${escapeHtml(record.filename)}</strong>
            <span>${escapeHtml(record.job_title || "Target role")} · ${escapeHtml(formatDate(record.created_at))}</span>
          </div></div>
          <span class="score-badge ${scoreClass(record.score)}">${escapeHtml(record.score)}%</span>
          <button class="row-arrow" type="button" data-open-analysis="${record.id}" aria-label="View analysis" title="View analysis">→</button>
        </div>`).join("") : `<div class="empty-state"><strong>Your workspace is ready.</strong>Run your first resume analysis to see your results here.</div>`;
    })
    .catch((error) => {
      const list = document.querySelector("#recent-list");
      if (list) list.innerHTML = `<div class="empty-state"><strong>Could not load your analyses.</strong>${escapeHtml(error.message)} <button class="text-button" type="button" data-page="dashboard">Try again</button></div>`;
      showToast(error.message, true);
    });
}

function renderAnalyze() {
  main.innerHTML = `
    <section class="page-heading">
      <div><div class="eyebrow">TAILORED FEEDBACK</div><h1>Start a new analysis</h1>
      <p>Share a resume and the role you have in mind. We’ll help you see where you stand.</p></div>
    </section>
    <section class="analysis-layout">
      <form class="form-card" id="analysis-form" novalidate>
        <h2 class="form-section-title"><span class="step-number">1</span> Add your resume</h2>
        <p class="form-hint">Choose a PDF or Word document to get started.</p>
        <div class="drop-zone" id="drop-zone">
          <input id="resume-file" type="file" accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document" aria-label="Choose a resume file" />
          <span class="upload-icon" aria-hidden="true">↑</span>
          <span class="drop-title">Drop your resume here or <span>browse files</span></span>
          <span class="drop-subtitle">PDF or DOCX · Max file size 10 MB</span>
        </div>
        <div id="selected-file">${renderSelectedFile()}</div>
        <div class="form-divider"></div>
        <h2 class="form-section-title"><span class="step-number">2</span> Tell us about the role</h2>
        <p class="form-hint">A specific job description gives you more useful feedback.</p>
        <div class="field">
          <label for="job-title">Job title <span class="optional">(optional)</span></label>
          <input id="job-title" name="job_title" maxlength="200" placeholder="e.g. Product Designer" />
        </div>
        <div class="field">
          <label for="job-description">Job description</label>
          <textarea id="job-description" name="job_description" minlength="10" required placeholder="Paste the job description here — include responsibilities, skills, and qualifications…"></textarea>
          <div class="field-footer"><span>At least 10 characters</span><span id="character-count">0 characters</span></div>
        </div>
        ${state.formError ? `<div class="form-error" role="alert">${escapeHtml(state.formError)}</div>` : ""}
        <button class="button button-primary button-wide" id="analyze-button" type="submit" ${state.loading ? "disabled" : ""}>
          ${state.loading ? "Analyzing your resume…" : "Analyze my resume"} <span aria-hidden="true">${state.loading ? "◌" : "→"}</span>
        </button>
        <div class="form-note"><span aria-hidden="true">♧</span><span>Analysis uses local rules by default. If an AI API is configured on the server, extracted resume text and the job description may be sent to that provider.</span></div>
      </form>
      <aside class="analysis-aside">
        <article class="aside-card"><h3>What you’ll get</h3><div class="steps-list">
          <div class="step-row"><span class="step-dot">1</span><span>A match score and resume completeness snapshot.</span></div>
          <div class="step-row"><span class="step-dot">2</span><span>Skills that match the role and skills to consider adding.</span></div>
          <div class="step-row"><span class="step-dot">3</span><span>Practical suggestions, interview prompts, and more.</span></div>
        </div></article>
        <article class="aside-card aside-tip"><h3>A note on your score</h3><p>Your match score is an estimate based on the project’s current analysis logic. It is not an official ATS score or a guarantee of an interview.</p></article>
      </aside>
    </section>`;
  bindAnalysisForm();
}

function renderSelectedFile() {
  if (!state.file) return "";
  return `<div class="selected-file"><span>▤ &nbsp;${escapeHtml(state.file.name)} · ${escapeHtml(formatBytes(state.file.size))}</span><button class="remove-file" type="button" data-remove-file aria-label="Remove selected file">Remove</button></div>`;
}

function formatBytes(bytes) {
  return bytes < 1024 * 1024 ? `${Math.max(1, Math.round(bytes / 1024))} KB` : `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function bindAnalysisForm() {
  const form = document.querySelector("#analysis-form");
  const input = document.querySelector("#resume-file");
  const zone = document.querySelector("#drop-zone");
  const description = document.querySelector("#job-description");
  const count = document.querySelector("#character-count");
  const updateCount = () => { count.textContent = `${description.value.length} characters`; };
  updateCount();
  description.addEventListener("input", updateCount);
  input.addEventListener("change", () => acceptFile(input.files[0]));
  zone.addEventListener("dragover", (event) => {
    event.preventDefault();
    zone.classList.add("is-dragging");
  });
  zone.addEventListener("dragleave", () => zone.classList.remove("is-dragging"));
  zone.addEventListener("drop", (event) => {
    event.preventDefault();
    zone.classList.remove("is-dragging");
    acceptFile(event.dataTransfer.files[0]);
  });
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    void submitAnalysis(form);
  });
}

function acceptFile(file) {
  if (!file) return;
  const extension = file.name.split(".").pop().toLowerCase();
  if (!["pdf", "docx"].includes(extension)) {
    showToast("Please choose a PDF or DOCX file.", true);
    return;
  }
  if (file.size > 10 * 1024 * 1024) {
    showToast("This file is over the 10 MB size limit.", true);
    return;
  }
  state.file = file;
  state.formError = "";
  const selected = document.querySelector("#selected-file");
  if (selected) selected.innerHTML = renderSelectedFile();
}

async function submitAnalysis(form) {
  const description = form.elements.job_description.value.trim();
  if (!state.file) {
    state.formError = "Choose a PDF or DOCX resume before starting the analysis.";
    showFormError(form, state.formError);
    return;
  }
  if (description.length < 10) {
    state.formError = "Enter a job description with at least 10 characters.";
    form.elements.job_description.focus();
    showFormError(form, state.formError);
    return;
  }

  const payload = new FormData();
  payload.append("file", state.file);
  payload.append("job_title", form.elements.job_title.value.trim() || "Target Role");
  payload.append("job_description", description);
  state.loading = true;
  state.formError = "";
  const button = document.querySelector("#analyze-button");
  button.disabled = true;
  button.innerHTML = 'Analyzing your resume… <span aria-hidden="true">◌</span>';

  try {
    state.analysis = await api("/api/analyze", { method: "POST", body: payload });
    state.file = null;
    state.loading = false;
    setPage("results");
    main.focus();
    showToast("Your resume analysis is ready.");
  } catch (error) {
    state.loading = false;
    state.formError = error.message;
    const button = document.querySelector("#analyze-button");
    button.disabled = false;
    button.innerHTML = 'Analyze my resume <span aria-hidden="true">→</span>';
    showFormError(form, state.formError);
    showToast(error.message, true);
  }
}

function showFormError(form, message) {
  let error = form.querySelector(".form-error");
  if (!error) {
    error = document.createElement("div");
    error.className = "form-error";
    error.setAttribute("role", "alert");
    form.querySelector("#analyze-button").before(error);
  }
  error.textContent = message;
}

function renderHistory() {
  main.innerHTML = `
    <section class="page-heading">
      <div><div class="eyebrow">YOUR WORKSPACE</div><h1>Analysis history</h1>
      <p>Revisit your previous role comparisons and reports.</p></div>
      <button class="button button-primary" type="button" data-page="analyze"><span aria-hidden="true">＋</span> New analysis</button>
    </section>
    <div class="panel history-panel" id="history-panel"><div class="loading-state">Loading your analysis history…</div></div>`;
  api("/api/history")
    .then((records) => {
      if (state.page !== "history") return;
      const panel = document.querySelector("#history-panel");
      if (!records.length) {
        panel.innerHTML = `<div class="empty-state"><strong>No analyses yet.</strong>Your saved reports will appear here after you run an analysis.<br><button class="button button-primary button-small" type="button" data-page="analyze" style="margin-top:14px">Start your first analysis</button></div>`;
        return;
      }
      panel.innerHTML = `<table class="history-table"><thead><tr><th>Resume</th><th>Role</th><th>Match score</th><th>Experience</th><th>Date</th><th>Actions</th></tr></thead><tbody>
        ${records.map((record) => `<tr>
          <td><strong>${escapeHtml(record.filename)}</strong><br><span style="color:#98a2a4;font-size:10px">${escapeHtml(record.candidate_name || "Candidate")}</span></td>
          <td>${escapeHtml(record.job_title || "Target role")}</td>
          <td><span class="score-badge ${scoreClass(record.score)}">${escapeHtml(record.score)}%</span></td>
          <td>${escapeHtml(record.experience_level || "—")}</td>
          <td>${escapeHtml(formatDate(record.created_at))}</td>
          <td><div class="history-actions"><button type="button" data-open-analysis="${record.id}">View report</button><button class="delete-button" type="button" data-delete-analysis="${record.id}" data-filename="${escapeHtml(record.filename)}">Delete</button></div></td>
        </tr>`).join("")}
      </tbody></table>`;
    })
    .catch((error) => {
      const panel = document.querySelector("#history-panel");
      if (panel) panel.innerHTML = `<div class="empty-state"><strong>Could not load your history.</strong>${escapeHtml(error.message)}<br><button class="text-button" type="button" data-page="history">Try again</button></div>`;
      showToast(error.message, true);
    });
}

function renderResult() {
  const result = state.analysis;
  if (!result) {
    setPage("dashboard");
    return;
  }
  const score = Math.max(0, Math.min(100, Number(result.score) || 0));
  const matching = Array.isArray(result.matching_skills) ? result.matching_skills : [];
  const missing = Array.isArray(result.missing_skills) ? result.missing_skills : [];
  const sections = result.section_scores && typeof result.section_scores === "object" ? Object.entries(result.section_scores) : [];
  main.innerHTML = `
    <section class="page-heading">
      <div class="result-header"><button class="button button-secondary button-small" type="button" data-page="history" aria-label="Back to history">←</button>
        <div><h1>Your analysis report</h1><p>${escapeHtml(result.filename)} · ${escapeHtml(formatDate(result.created_at))}</p></div>
      </div>
      <button class="button button-secondary" type="button" data-page="analyze">Analyze another <span aria-hidden="true">→</span></button>
    </section>
    <section class="result-layout">
      <div class="result-main">
        <article class="result-card score-overview">
          <div class="score-ring" style="--score:${score}"><div class="score-ring-inner"><strong>${score}</strong><span>match score</span></div></div>
          <div class="score-copy"><div class="eyebrow">YOUR ROLE MATCH</div><h2>${escapeHtml(result.job_title || "Target role")}</h2>
            <p>${score >= 70 ? "Your resume looks well aligned with this role. Review the details below to find ways to make your application even stronger." : score >= 45 ? "There are some promising overlaps with this role. A few focused updates could help your experience stand out." : "This role may need some experience or skills that aren’t clear in your resume yet. Review the suggestions to identify next steps."}</p>
          </div>
        </article>
        <article class="result-card summary-card"><h2>At a glance</h2><p>${escapeHtml(result.summary || "No summary was provided for this analysis.")}</p>
          <div class="result-meta"><span class="meta-pill">Candidate <strong>${escapeHtml(result.candidate_name || "Candidate")}</strong></span><span class="meta-pill">Experience <strong>${escapeHtml(result.experience_level || "Not specified")}</strong></span><span class="meta-pill">Resume completeness <strong>${escapeHtml(result.completeness_score ?? 0)}%</strong></span></div>
        </article>
        ${sections.length ? `<article class="result-card"><h2>Resume section scores</h2><div class="section-score-list">${sections.map(([name, value]) => {
          const percentage = Math.max(0, Math.min(100, Number(value) || 0));
          return `<div class="section-score-row"><span>${escapeHtml(name)}</span><div class="progress-track"><div class="progress-fill" style="width:${percentage}%"></div></div><span class="section-score-value">${percentage}%</span></div>`;
        }).join("")}</div></article>` : ""}
        <div class="two-column-cards">
          <article class="result-card list-card"><h2><span class="heading-dot"></span>Skills that match</h2><div class="chip-list">${matching.length ? matching.map((skill) => `<span class="skill-chip">${escapeHtml(skill)}</span>`).join("") : '<span class="result-disclaimer">No matching skills were identified.</span>'}</div></article>
          <article class="result-card list-card"><h2><span class="heading-dot missing"></span>Skills to consider</h2><div class="chip-list">${missing.length ? missing.map((skill) => `<span class="skill-chip missing">${escapeHtml(skill)}</span>`).join("") : '<span class="result-disclaimer">No missing skills were identified.</span>'}</div></article>
        </div>
        <div class="two-column-cards">
          ${renderListCard("Strengths", result.strengths, "heading-dot")}
          ${renderListCard("Areas to improve", result.weaknesses, "heading-dot missing")}
        </div>
        ${renderListCard("Suggestions for your resume", result.suggestions)}
        ${Array.isArray(result.rewrite_suggestions) && result.rewrite_suggestions.length ? `<article class="result-card"><h2>Rewrite ideas</h2>${result.rewrite_suggestions.map((item) => `<div class="rewrite-item"><span class="rewrite-label">Current</span><p>${escapeHtml(item.original || "")}</p><span class="rewrite-label">Try instead</span><p>${escapeHtml(item.suggested || "")}</p></div>`).join("")}</article>` : ""}
      </div>
      <aside class="result-sidebar">
        ${renderChecklist(result.checklist)}
        ${renderRecommendations(result.course_recommendations)}
        ${renderListCard("Interview practice", result.interview_questions)}
        <p class="result-disclaimer">This is an estimate from the project’s current analysis logic, not an official ATS score or a guarantee of shortlisting.</p>
      </aside>
    </section>`;
}

function renderListCard(title, items, dotClass = "") {
  const list = Array.isArray(items) ? items : [];
  if (!list.length) return "";
  return `<article class="result-card list-card"><h2>${dotClass ? `<span class="${dotClass}"></span>` : ""}${escapeHtml(title)}</h2><ul class="bullet-list ${title === "Areas to improve" ? "warning" : ""}">${list.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul></article>`;
}

function renderChecklist(items) {
  if (!Array.isArray(items) || !items.length) return "";
  return `<article class="result-card"><h2>Resume checklist</h2><div class="checklist">${items.map((item) => `<div class="check-item"><span class="check-icon ${item.passed ? "" : "fail"}">${item.passed ? "✓" : "!"}</span><span>${escapeHtml(item.item || "")}</span></div>`).join("")}</div></article>`;
}

function renderRecommendations(items) {
  if (!Array.isArray(items) || !items.length) return "";
  return `<article class="result-card"><h2>Learning ideas</h2>${items.map((item) => `<div class="recommendation-item"><strong>${escapeHtml(item.topic || "Explore this topic")}</strong><span>${escapeHtml(item.reason || "")}</span></div>`).join("")}</article>`;
}

async function openAnalysis(id) {
  try {
    state.analysis = await api(`/api/analysis/${encodeURIComponent(id)}`);
    setPage("results");
    main.focus();
  } catch (error) {
    showToast(error.message, true);
  }
}

async function deleteAnalysis(id, filename) {
  if (!window.confirm(`Delete the saved analysis for “${filename}”? This cannot be undone.`)) return;
  try {
    await api(`/api/analysis/${encodeURIComponent(id)}`, { method: "DELETE" });
    showToast("Analysis deleted.");
    if (state.page === "history") renderHistory();
    else renderDashboard();
  } catch (error) {
    showToast(error.message, true);
  }
}

document.addEventListener("click", (event) => {
  const pageButton = event.target.closest("[data-page]");
  if (pageButton) {
    if (state.loading) return;
    setPage(pageButton.dataset.page);
    return;
  }
  const removeButton = event.target.closest("[data-remove-file]");
  if (removeButton) {
    state.file = null;
    document.querySelector("#selected-file").innerHTML = "";
    const input = document.querySelector("#resume-file");
    if (input) input.value = "";
    return;
  }
  const openButton = event.target.closest("[data-open-analysis]");
  if (openButton) {
    void openAnalysis(openButton.dataset.openAnalysis);
    return;
  }
  const deleteButton = event.target.closest("[data-delete-analysis]");
  if (deleteButton) void deleteAnalysis(deleteButton.dataset.deleteAnalysis, deleteButton.dataset.filename);
});

setPage("dashboard");
