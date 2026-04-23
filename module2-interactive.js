/**
 * Module 2 Interactive Pain Mapping
 * Interactive body pain mapping system
 */

// API Base URL
const API_BASE = window.location.origin.includes('localhost') || window.location.origin.includes('127.0.0.1')
  ? 'http://localhost:8000'
  : window.location.origin;

// Pain types configuration with GIF animations
const PAIN_TYPES = {
  burning: {
    name: 'Burning',
    label: 'Burning sensation',
    color: '#005EB8',
    icon: '/Backend/images/burning.gif',
    staticIcon: '🔥',
    neuropathic: true
  },
  aching: {
    name: 'Aching',
    label: 'Aching pain',
    color: '#F1C40F',
    icon: '/Backend/images/dull.jpg',
    staticIcon: '💪',
    neuropathic: false
  },
  stabbing: {
    name: 'Stabbing',
    label: 'Stabbing pain',
    color: '#E74C3C',
    icon: '/Backend/images/sharp.gif',
    staticIcon: '⚡',
    neuropathic: true
  },
  tingling: {
    name: 'Tingling',
    label: 'Tingling sensation',
    color: '#27AE60',
    icon: '/Backend/images/Tingling.jpg',
    staticIcon: '✨',
    neuropathic: true
  },
  pulsing: {
    name: 'Pulsing',
    label: 'Pulsing sensation',
    color: '#9B59B6',
    icon: '/Backend/images/pulsing.gif',
    staticIcon: '💓',
    neuropathic: false
  },
  radiating: {
    name: 'Radiating',
    label: 'Radiating pain',
    color: '#E67E22',
    icon: '/Backend/images/radiating.gif',
    staticIcon: '📡',
    neuropathic: true
  },
  other: {
    name: 'Other',
    label: 'Other',
    color: '#95A5A6',
    staticIcon: '❓',
    neuropathic: false
  },
  eraser: {
    name: 'Eraser',
    label: 'Eraser',
    color: '#424752',
    staticIcon: '🧹',
    neuropathic: false
  }
};

// Global state
let selectedTool = 'burning';
let isDrawing = false;
let currentView = null;
let strokeCount = {
  burning: 0,
  aching: 0,
  stabbing: 0,
  tingling: 0,
  pulsing: 0,
  radiating: 0,
  other: 0
};
let sessionId = generateSessionId();

// Canvas references
let frontCanvas, backCanvas, frontCtx, backCtx;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  initializeCanvases();
  loadPainTools();
  loadColorLegend();
  setupEventListeners();
  fetchPainTypesFromAPI(); // Optional: get latest from backend
});

function initializeCanvases() {
  frontCanvas = document.getElementById('frontCanvas');
  backCanvas = document.getElementById('backCanvas');
  frontCtx = frontCanvas.getContext('2d');
  backCtx = backCanvas.getContext('2d');
  
  // Set canvas size for high DPI
  const scale = 2;
  frontCanvas.style.width = '100%';
  frontCanvas.style.height = '100%';
  backCanvas.style.width = '100%';
  backCanvas.style.height = '100%';
}

function loadPainTools() {
  const toolsContainer = document.getElementById('paintTools');
  
  Object.entries(PAIN_TYPES).forEach(([type, config]) => {
    const button = document.createElement('button');
    button.className = 'tool-button';
    button.dataset.tool = type;
    
    if (type === selectedTool) {
      button.classList.add('active');
      button.style.backgroundColor = config.color;
    }
    
    // Try to load GIF, fallback to emoji
    if (config.icon) {
      const img = document.createElement('img');
      img.className = 'tool-icon';
      img.src = config.icon;
      img.alt = config.name;
      img.onerror = function() {
        // If image fails to load, show emoji
        this.style.display = 'none';
        const emoji = document.createElement('div');
        emoji.style.fontSize = '28px';
        emoji.textContent = config.staticIcon;
        button.insertBefore(emoji, button.firstChild);
      };
      button.appendChild(img);
    } else {
      const emoji = document.createElement('div');
      emoji.style.fontSize = '28px';
      emoji.textContent = config.staticIcon;
      button.appendChild(emoji);
    }
    
    const label = document.createElement('span');
    label.textContent = config.name;
    button.appendChild(label);
    
    button.addEventListener('click', () => selectTool(type));
    toolsContainer.appendChild(button);
  });
}

function loadColorLegend() {
  const legendContainer = document.getElementById('colorLegend');
  
  Object.entries(PAIN_TYPES).forEach(([type, config]) => {
    if (type === 'eraser') return; // Skip eraser in legend
    
    const item = document.createElement('div');
    item.className = 'legend-item';
    
    const colorBox = document.createElement('div');
    colorBox.className = 'legend-color';
    colorBox.style.backgroundColor = config.color;
    
    const text = document.createElement('div');
    text.className = 'legend-text';
    text.innerHTML = `<strong>${config.name}</strong><span>${config.label} ${config.neuropathic ? '(NeuP)' : ''}</span>`;
    
    item.appendChild(colorBox);
    item.appendChild(text);
    legendContainer.appendChild(item);
  });
}

function selectTool(tool) {
  selectedTool = tool;
  
  // Update button states
  document.querySelectorAll('.tool-button').forEach(btn => {
    btn.classList.remove('active');
    btn.style.backgroundColor = '';
    btn.style.color = '#424752';
  });
  
  const activeBtn = document.querySelector(`[data-tool="${tool}"]`);
  if (activeBtn) {
    activeBtn.classList.add('active');
    activeBtn.style.backgroundColor = PAIN_TYPES[tool].color;
    activeBtn.style.color = 'white';
  }
}

function setupEventListeners() {
  // Canvas drawing events - Front
  const frontView = document.getElementById('frontView');
  frontView.addEventListener('mousedown', (e) => startDrawing(e, 'front'));
  frontView.addEventListener('mousemove', (e) => draw(e, 'front'));
  frontView.addEventListener('mouseup', stopDrawing);
  frontView.addEventListener('mouseleave', stopDrawing);
  
  // Canvas drawing events - Back
  const backView = document.getElementById('backView');
  backView.addEventListener('mousedown', (e) => startDrawing(e, 'back'));
  backView.addEventListener('mousemove', (e) => draw(e, 'back'));
  backView.addEventListener('mouseup', stopDrawing);
  backView.addEventListener('mouseleave', stopDrawing);
  
  // Action buttons
  document.getElementById('generateReportBtn').addEventListener('click', generateReport);
  document.getElementById('clearCanvasBtn').addEventListener('click', clearCanvas);
  document.getElementById('saveProgressBtn').addEventListener('click', saveProgress);
  document.getElementById('closeModal').addEventListener('click', closeModal);
  
  // Click outside modal to close
  document.getElementById('reportModal').addEventListener('click', (e) => {
    if (e.target.id === 'reportModal') closeModal();
  });
}

function startDrawing(e, view) {
  if (!selectedTool) return;
  isDrawing = true;
  currentView = view;
  draw(e, view); // Draw immediately on click
}

function draw(e, view) {
  if (!isDrawing || currentView !== view) return;
  
  const canvas = view === 'front' ? frontCanvas : backCanvas;
  const ctx = view === 'front' ? frontCtx : backCtx;
  const wrapper = canvas.closest('.body-canvas-wrapper');
  const rect = wrapper.getBoundingClientRect();
  
  // Calculate relative position
  const x = ((e.clientX - rect.left) / rect.width) * canvas.width;
  const y = ((e.clientY - rect.top) / rect.height) * canvas.height;
  
  if (selectedTool === 'eraser') {
    // Erase mode
    ctx.globalCompositeOperation = 'destination-out';
    ctx.globalAlpha = 1.0;
    ctx.fillStyle = 'rgba(0,0,0,1)';
    ctx.beginPath();
    ctx.arc(x, y, 28, 0, Math.PI * 2);
    ctx.fill();
    ctx.globalCompositeOperation = 'source-over';
  } else {
    // Draw mode
    ctx.globalAlpha = 0.4;
    ctx.fillStyle = PAIN_TYPES[selectedTool].color;
    ctx.beginPath();
    ctx.arc(x, y, 24, 0, Math.PI * 2);
    ctx.fill();
    ctx.globalAlpha = 1.0;
    
    // Track stroke
    strokeCount[selectedTool] = (strokeCount[selectedTool] || 0) + 1;
    updateAnalysis();
  }
}

function stopDrawing() {
  isDrawing = false;
  currentView = null;
}

function updateAnalysis() {
  const total = Object.values(strokeCount).reduce((sum, count) => sum + count, 0);
  if (total === 0) {
    document.getElementById('sensationBreakdown').innerHTML = 
      '<p style="color: #727783; font-size: 12px; text-align: center;">No data mapped yet</p>';
    updateIntensity(0);
    return;
  }
  
  // Calculate percentages
  const breakdown = {};
  Object.keys(strokeCount).forEach(type => {
    if (type !== 'eraser' && strokeCount[type] > 0) {
      breakdown[type] = Math.round((strokeCount[type] / total) * 100);
    }
  });
  
  // Sort by percentage
  const sorted = Object.entries(breakdown).sort((a, b) => b[1] - a[1]);
  
  // Update UI
  const container = document.getElementById('sensationBreakdown');
  container.innerHTML = '';
  
  sorted.forEach(([type, percentage]) => {
    const config = PAIN_TYPES[type];
    const item = document.createElement('div');
    item.className = 'sensation-item';
    item.innerHTML = `
      <div class="sensation-header">
        <div class="sensation-label">
          <div class="sensation-color" style="background-color: ${config.color}"></div>
          <span>${config.name}</span>
        </div>
        <span class="sensation-percentage" style="color: ${config.color}">${percentage}%</span>
      </div>
      <div class="sensation-bar">
        <div class="sensation-fill" style="width: ${percentage}%; background-color: ${config.color}"></div>
      </div>
    `;
    container.appendChild(item);
  });
  
  // Update intensity (simple heuristic based on total strokes)
  const intensity = Math.min(10, (total / 50) * 10).toFixed(1);
  updateIntensity(intensity);
}

function updateIntensity(value) {
  document.getElementById('intensityValue').textContent = value;
  document.getElementById('intensityFill').style.width = `${(value / 10) * 100}%`;
}

function clearCanvas() {
  if (!confirm('Are you sure you want to clear all pain mapping? This cannot be undone.')) {
    return;
  }
  
  frontCtx.clearRect(0, 0, frontCanvas.width, frontCanvas.height);
  backCtx.clearRect(0, 0, backCanvas.width, backCanvas.height);
  
  strokeCount = {
    burning: 0,
    aching: 0,
    stabbing: 0,
    tingling: 0,
    pulsing: 0,
    radiating: 0,
    other: 0
  };
  
  updateAnalysis();
}

async function saveProgress() {
  const painData = collectPainData();
  
  try {
    const response = await fetch(`${API_BASE}/api/pain-mapping/save`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(painData)
    });
    
    const result = await response.json();
    
    if (result.status === 'success') {
      alert('✅ Pain mapping saved successfully!');
    } else {
      alert('❌ Error saving: ' + result.message);
    }
  } catch (error) {
    console.error('Save error:', error);
    alert('❌ Failed to save. Please check your connection.');
  }
}

async function generateReport() {
  const total = Object.values(strokeCount).reduce((sum, count) => sum + count, 0);
  console.log('[Generate Report] strokeCount:', strokeCount);
  console.log('[Generate Report] total strokes:', total);
  
  if (total === 0) {
    alert('Please map some pain areas first before generating a report.');
    return;
  }
  
  const painData = collectPainData();
  console.log('[Generate Report] painData:', painData);
  
  try {
    const response = await fetch(`${API_BASE}/api/pain-mapping/generate-report`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(painData)
    });
    
    const result = await response.json();
    
    if (result.status === 'success') {
      displayReport(result.report);
    } else {
      alert('❌ Error generating report: ' + result.message);
    }
  } catch (error) {
    console.error('Report generation error:', error);
    alert('❌ Failed to generate report. Please check your connection.');
  }
}

function collectPainData() {
  const total = Object.values(strokeCount).reduce((sum, count) => sum + count, 0);
  const breakdown = {};
  
  Object.keys(strokeCount).forEach(type => {
    if (strokeCount[type] > 0) {
      breakdown[type] = Math.round((strokeCount[type] / total) * 100);
    }
  });
  
  const intensity = Math.min(10, (total / 50) * 10);
  
  return {
    session_id: sessionId,
    patient_id: null,
    front_canvas_data: frontCanvas.toDataURL(),
    back_canvas_data: backCanvas.toDataURL(),
    pain_regions: [], // Can be enhanced to track specific regions
    overall_intensity: parseFloat(intensity.toFixed(1)),
    sensation_breakdown: breakdown,
    total_strokes: total
  };
}

function displayReport(report) {
  const modal = document.getElementById('reportModal');
  const content = document.getElementById('reportContent');
  
  const neuropathicColor = report.neuropathic_probability === 'high' ? '#E74C3C' :
                           report.neuropathic_probability === 'medium' ? '#E67E22' : '#27AE60';
  
  content.innerHTML = `
    <div class="report-section">
      <h3>Summary</h3>
      <p>${report.summary}</p>
    </div>
    
    <div class="report-section">
      <h3>Overall Pain Intensity</h3>
      <p style="font-size: 24px; font-weight: 700; color: #005EB8;">${report.mapping_data.overall_intensity} / 10</p>
    </div>
    
    <div class="report-section">
      <h3>Dominant Sensations</h3>
      <ul class="report-list">
        ${report.dominant_sensations.map(s => `<li>${s}</li>`).join('')}
      </ul>
    </div>
    
    <div class="report-section">
      <h3>Neuropathic Pain Assessment</h3>
      <p>Probability: <strong style="color: ${neuropathicColor}">${report.neuropathic_probability.toUpperCase()}</strong></p>
      <p style="font-size: 12px; color: #727783; margin-top: 8px;">
        ${report.neuropathic_probability === 'high' ? 
          'High probability of neuropathic pain component. Neurological evaluation recommended.' :
          report.neuropathic_probability === 'medium' ?
          'Mixed pain presentation with some neuropathic features.' :
          'Primarily non-neuropathic pain pattern.'}
      </p>
    </div>
    
    <div class="report-section">
      <h3>Recommended Specialists</h3>
      <ul class="report-list">
        ${report.recommended_specialists.map(s => `<li>${s}</li>`).join('')}
      </ul>
    </div>
    
    <div class="report-section">
      <h3>Report ID</h3>
      <p style="font-family: monospace; font-size: 12px; color: #727783;">${report.report_id}</p>
      <p style="font-size: 11px; color: #727783;">Generated: ${new Date(report.generated_at).toLocaleString()}</p>
    </div>
    
    <div class="action-buttons">
      <button class="action-button primary" onclick="window.print()">Print Report</button>
      <button class="action-button secondary" onclick="downloadReport()">Download as JSON</button>
    </div>
  `;
  
  modal.classList.add('show');
}

function closeModal() {
  document.getElementById('reportModal').classList.remove('show');
}

function downloadReport() {
  const report = document.getElementById('reportContent').textContent;
  const blob = new Blob([report], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `pain-report-${sessionId}.txt`;
  a.click();
  URL.revokeObjectURL(url);
}

async function fetchPainTypesFromAPI() {
  try {
    const response = await fetch(`${API_BASE}/api/pain-mapping/pain-types`);
    const result = await response.json();
    
    if (result.status === 'success') {
      console.log('Pain types loaded from API:', result.pain_types);
      // Could update PAIN_TYPES with server data if needed
    }
  } catch (error) {
    console.log('Using local pain types configuration');
  }
}

function generateSessionId() {
  return `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}
