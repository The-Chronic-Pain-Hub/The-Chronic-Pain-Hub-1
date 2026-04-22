const API = "http://localhost:8000";

let audioBlob = null;
let mediaRecorder = null;
let recordingChunks = [];
let timerInterval = null;
let seconds = 0;

const fileInput    = document.getElementById("file-input");
const fileSelected = document.getElementById("file-selected");
const uploadZone   = document.getElementById("upload-zone");
const recordBtn    = document.getElementById("record-btn");
const recordLabel  = document.getElementById("record-label");
const recordDot    = document.getElementById("record-dot");
const recordTimer  = document.getElementById("record-timer");
const analyzeBtn   = document.getElementById("analyze-btn");
const resetBtn     = document.getElementById("reset-btn");

// Add spinner animation
const style = document.createElement("style");
style.textContent = `@keyframes spin { to { transform: rotate(360deg); } }`;
document.head.appendChild(style);

// Analyze button hover
analyzeBtn.addEventListener("mouseenter", () => {
  if (!analyzeBtn.disabled) analyzeBtn.style.background = "var(--accent-strong)";
});
analyzeBtn.addEventListener("mouseleave", () => {
  if (!analyzeBtn.disabled) analyzeBtn.style.background = "var(--accent)";
});

// Upload drag and drop
uploadZone.addEventListener("dragover", e => {
  e.preventDefault();
  uploadZone.style.borderColor = "var(--accent-cool)";
  uploadZone.style.background  = "rgba(47,127,125,0.04)";
});
uploadZone.addEventListener("dragleave", () => {
  uploadZone.style.borderColor = "var(--border)";
  uploadZone.style.background  = "transparent";
});
uploadZone.addEventListener("drop", e => {
  e.preventDefault();
  uploadZone.style.borderColor = "var(--border)";
  uploadZone.style.background  = "transparent";
  if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
});

fileInput.addEventListener("change", () => {
  if (fileInput.files[0]) handleFile(fileInput.files[0]);
});

function handleFile(file) {
  audioBlob                  = file;
  fileSelected.style.display = "block";
  fileSelected.textContent   = `✓ ${file.name} (${(file.size/1024/1024).toFixed(1)} MB)`;
  analyzeBtn.disabled        = false;
  analyzeBtn.style.opacity   = "1";
}

// Recording
recordBtn.addEventListener("click", async () => {
  if (mediaRecorder && mediaRecorder.state === "recording") {
    mediaRecorder.stop();
    return;
  }

  const stream    = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder   = new MediaRecorder(stream);
  recordingChunks = [];

  mediaRecorder.ondataavailable = e => recordingChunks.push(e.data);
  mediaRecorder.onstop = () => {
    audioBlob                  = new Blob(recordingChunks, { type: "audio/webm" });
    clearInterval(timerInterval);
    recordTimer.textContent    = `Recording saved (${seconds}s)`;
    recordDot.style.background = "var(--accent)";
    recordLabel.textContent    = "Record Again";
    analyzeBtn.disabled        = false;
    analyzeBtn.style.opacity   = "1";
    stream.getTracks().forEach(t => t.stop());
  };

  mediaRecorder.start();
  recordDot.style.background = "#ef4444";
  recordLabel.textContent    = "Stop Recording";
  seconds                    = 0;
  recordTimer.textContent    = "0s";
  timerInterval = setInterval(() => {
    seconds++;
    recordTimer.textContent = `${seconds}s`;
  }, 1000);
});

// Analyze
analyzeBtn.addEventListener("click", async () => {
  if (!audioBlob) return;

  document.getElementById("input-card").style.display    = "none";
  document.getElementById("empty-state").style.display   = "none";
  document.getElementById("loading-state").style.display = "block";
  document.getElementById("status-chip").textContent     = "Analyzing";

  setTimeout(() => document.getElementById("step1").style.opacity = "1", 500);
  setTimeout(() => document.getElementById("step2").style.opacity = "1", 2000);
  setTimeout(() => document.getElementById("step3").style.opacity = "1", 4000);

  const form = new FormData();
  form.append("file", audioBlob, audioBlob.name || "recording.wav");

  try {
    const res  = await fetch(`${API}/analyze`, { method: "POST", body: form });
    const data = await res.json();
    if (data.error) throw new Error(data.error);
    showResults(data);
  } catch (err) {
    document.getElementById("loading-state").style.display = "none";
    document.getElementById("input-card").style.display    = "block";
    document.getElementById("empty-state").style.display   = "block";
    console.error(err);
    alert("Error: " + err.message + "\n\nMake sure the API is running:\ncd ~/voice-health && python3 -m uvicorn api:app --reload");
  }
});

function showResults(data) {
  document.getElementById("loading-state").style.display = "none";
  document.getElementById("result-state").style.display  = "block";

  const isDepressed = data.prediction === 1;
  document.getElementById("status-chip").textContent = isDepressed ? "Risk Detected" : "No Risk Detected";
  document.getElementById("status-chip").className   = isDepressed
    ? "dashboard-chip" : "dashboard-chip dashboard-chip-cool";

  document.getElementById("result-label").textContent = data.label;
  document.getElementById("conf-value").textContent   = `${Math.round(data.confidence * 100)}%`;
  document.getElementById("dep-pct").textContent      = `${Math.round(data.depression_probability * 100)}%`;
  document.getElementById("nodep-pct").textContent    = `${Math.round(data.no_depression_probability * 100)}%`;

  if (data.reasoning) {
    const reasoningEl = document.getElementById("reasoning-text");
    if (reasoningEl) {
      reasoningEl.textContent                 = data.reasoning;
      reasoningEl.parentElement.style.display = "block";
    }
  }

  setTimeout(() => {
    document.getElementById("dep-bar").style.width   = `${Math.round(data.depression_probability * 100)}%`;
    document.getElementById("nodep-bar").style.width = `${Math.round(data.no_depression_probability * 100)}%`;
  }, 100);
}

// Reset
resetBtn.addEventListener("click", () => {
  document.getElementById("result-state").style.display  = "none";
  document.getElementById("empty-state").style.display   = "block";
  document.getElementById("input-card").style.display    = "block";
  document.getElementById("status-chip").textContent     = "Waiting";
  document.getElementById("status-chip").className       = "dashboard-chip dashboard-chip-sun";
  audioBlob                  = null;
  fileSelected.style.display = "none";
  fileInput.value            = "";
  recordTimer.textContent    = "";
  recordLabel.textContent    = "Start Recording";
  analyzeBtn.disabled        = true;
  analyzeBtn.style.opacity   = "0.4";
  document.getElementById("dep-bar").style.width   = "0%";
  document.getElementById("nodep-bar").style.width = "0%";
});