// Module 5: Treatment Assessment & Recommendations
// Main application logic for questionnaire, scoring, and treatment matching

class PainAssessment {
  constructor() {
    this.questionnaire = null;
    this.treatments = null;
    this.responses = {};
    this.currentSectionIndex = 0;
    this.dimensionScores = {};
    
    this.init();
  }

  async init() {
    try {
      // Load questionnaire and treatment data
      await this.loadData();
      
      // Render first section
      this.renderSections();
      this.showSection(0);
      
      // Setup event listeners
      this.setupEventListeners();
      
      // Update progress
      this.updateProgress();
    } catch (error) {
      console.error('Initialization error:', error);
      this.showError('Failed to load assessment. Please refresh the page.');
    }
  }

  async loadData() {
    try {
      // Load questionnaire JSON
      const questionnaireResponse = await fetch('Backend/data/module5_questionnaire.json');
      const questionnaireData = await questionnaireResponse.json();
      this.questionnaire = questionnaireData.questionnaire;
      
      // Load treatments JSON
      const treatmentsResponse = await fetch('Backend/data/module5_treatments.json');
      const treatmentsData = await treatmentsResponse.json();
      this.treatments = treatmentsData.treatment_pathways;
      
      // Update total sections
      document.getElementById('totalSections').textContent = this.questionnaire.sections.length;
    } catch (error) {
      console.error('Error loading data:', error);
      throw error;
    }
  }

  renderSections() {
    const container = document.getElementById('questionSections');
    container.innerHTML = '';
    
    this.questionnaire.sections.forEach((section, sectionIndex) => {
      const sectionDiv = document.createElement('div');
      sectionDiv.className = 'question-section';
      sectionDiv.id = `section-${sectionIndex}`;
      
      // Section header
      const header = `
        <div class="section-header">
          <h2 class="section-title">${section.title}</h2>
          ${section.description ? `<p class="section-description">${section.description}</p>` : ''}
        </div>
      `;
      
      // Section stem (if present)
      const stem = section.stem ? `<div class="section-stem">${section.stem}</div>` : '';
      
      // Render questions
      const questionsHTML = section.questions.map((question, qIndex) => 
        this.renderQuestion(question, sectionIndex, qIndex)
      ).join('');
      
      sectionDiv.innerHTML = header + stem + questionsHTML;
      container.appendChild(sectionDiv);
    });
  }

  renderQuestion(question, sectionIndex, questionIndex) {
    const questionId = question.id;
    
    let inputHTML = '';
    
    switch (question.type) {
      case 'likert':
        inputHTML = this.renderLikert(question, questionId);
        break;
      case 'slider':
        inputHTML = this.renderSlider(question, questionId);
        break;
      case 'yes_no':
        inputHTML = this.renderYesNo(question, questionId);
        break;
      case 'select':
        inputHTML = this.renderSelect(question, questionId);
        break;
      default:
        inputHTML = '<p>Unknown question type</p>';
    }
    
    return `
      <div class="question-item" data-question-id="${questionId}">
        <div class="question-text">${question.text}</div>
        ${inputHTML}
      </div>
    `;
  }

  renderLikert(question, questionId) {
    const scale = question.scale;
    const options = [];
    
    for (let i = scale.min; i <= scale.max; i++) {
      const label = scale.labels[i] !== undefined ? scale.labels[i] : i;
      const displayLabel = label === '' ? '&nbsp;' : label;
      options.push(`
        <div class="likert-option">
          <input type="radio" name="${questionId}" value="${i}" id="${questionId}_${i}">
          <label for="${questionId}_${i}">${displayLabel}</label>
        </div>
      `);
    }
    
    return `
      <div class="likert-scale">
        ${options.join('')}
      </div>
    `;
  }

  renderSlider(question, questionId) {
    const scale = question.scale;
    return `
      <div class="slider-container">
        <div class="slider-value" id="${questionId}_value">${Math.floor((scale.min + scale.max) / 2)}</div>
        <input 
          type="range" 
          class="slider" 
          name="${questionId}" 
          min="${scale.min}" 
          max="${scale.max}" 
          value="${Math.floor((scale.min + scale.max) / 2)}"
          id="${questionId}"
          oninput="document.getElementById('${questionId}_value').textContent = this.value"
        >
        <div class="likert-labels">
          <span>${scale.labels[scale.min]}</span>
          <span>${scale.labels[scale.max]}</span>
        </div>
      </div>
    `;
  }

  renderYesNo(question, questionId) {
    return `
      <div class="yes-no-buttons">
        <button type="button" class="yes-no-button" data-value="yes" data-question="${questionId}">
          Yes
        </button>
        <button type="button" class="yes-no-button" data-value="no" data-question="${questionId}">
          No
        </button>
      </div>
      <input type="hidden" name="${questionId}" id="${questionId}">
    `;
  }

  renderSelect(question, questionId) {
    const options = question.options.map(opt => 
      `<option value="${opt.value}">${opt.label}</option>`
    ).join('');
    
    return `
      <select class="select-dropdown" name="${questionId}" id="${questionId}">
        ${options}
      </select>
    `;
  }

  setupEventListeners() {
    // Navigation buttons
    document.getElementById('nextButton').addEventListener('click', () => this.nextSection());
    document.getElementById('backButton').addEventListener('click', () => this.previousSection());
    document.getElementById('submitButton').addEventListener('click', () => this.submitAssessment());
    
    // Yes/No button handlers
    document.addEventListener('click', (e) => {
      if (e.target.classList.contains('yes-no-button')) {
        const questionId = e.target.dataset.question;
        const value = e.target.dataset.value;
        
        // Remove selected class from siblings
        const siblings = e.target.parentElement.querySelectorAll('.yes-no-button');
        siblings.forEach(btn => btn.classList.remove('selected'));
        
        // Add selected class to clicked button
        e.target.classList.add('selected');
        
        // Set hidden input value
        document.getElementById(questionId).value = value;
      }
    });
    
    // Auto-save responses
    document.getElementById('assessmentForm').addEventListener('change', (e) => {
      if (e.target.name) {
        this.responses[e.target.name] = e.target.value;
      }
    });
  }

  showSection(index) {
    // Hide all sections
    const sections = document.querySelectorAll('.question-section');
    sections.forEach(section => section.classList.remove('active'));
    
    // Show current section
    const currentSection = document.getElementById(`section-${index}`);
    if (currentSection) {
      currentSection.classList.add('active');
      this.currentSectionIndex = index;
      
      // Update navigation buttons
      this.updateNavigationButtons();
      
      // Update progress
      this.updateProgress();
      
      // Scroll to top
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  updateNavigationButtons() {
    const backButton = document.getElementById('backButton');
    const nextButton = document.getElementById('nextButton');
    const submitButton = document.getElementById('submitButton');
    
    const totalSections = this.questionnaire.sections.length;
    const isFirstSection = this.currentSectionIndex === 0;
    const isLastSection = this.currentSectionIndex === totalSections - 1;
    
    // Back button
    backButton.style.display = isFirstSection ? 'none' : 'block';
    
    // Next/Submit buttons
    if (isLastSection) {
      nextButton.style.display = 'none';
      submitButton.style.display = 'block';
    } else {
      nextButton.style.display = 'block';
      submitButton.style.display = 'none';
    }
  }

  updateProgress() {
    const totalSections = this.questionnaire.sections.length;
    const currentSection = this.currentSectionIndex + 1;
    const percent = Math.round((currentSection / totalSections) * 100);
    
    document.getElementById('currentSection').textContent = currentSection;
    document.getElementById('progressPercent').textContent = percent;
    document.getElementById('progressFill').style.width = `${percent}%`;
  }

  nextSection() {
    // Validate current section
    if (!this.validateCurrentSection()) {
      this.showError('Please answer all questions in this section before continuing.');
      return;
    }
    
    // Clear error
    this.hideError();
    
    // Move to next section
    const totalSections = this.questionnaire.sections.length;
    if (this.currentSectionIndex < totalSections - 1) {
      this.showSection(this.currentSectionIndex + 1);
    }
  }

  previousSection() {
    if (this.currentSectionIndex > 0) {
      this.showSection(this.currentSectionIndex - 1);
    }
  }

  validateCurrentSection() {
    const currentSection = this.questionnaire.sections[this.currentSectionIndex];
    
    for (const question of currentSection.questions) {
      const input = document.querySelector(`[name="${question.id}"]`);
      
      if (!input || !input.value || input.value === '') {
        return false;
      }
    }
    
    return true;
  }

  showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  hideError() {
    document.getElementById('errorMessage').style.display = 'none';
  }

  async submitAssessment() {
    // Validate last section
    if (!this.validateCurrentSection()) {
      this.showError('Please answer all questions before submitting.');
      return;
    }
    
    // Collect all responses
    this.collectAllResponses();
    
    // Show loading
    document.getElementById('assessmentForm').style.display = 'none';
    document.getElementById('loadingSpinner').style.display = 'block';
    
    // Calculate scores (simulate processing time)
    setTimeout(() => {
      this.calculateDimensionScores();
      this.matchTreatments();
      this.displayResults();
      
      // Hide loading, show results
      document.getElementById('loadingSpinner').style.display = 'none';
      document.getElementById('resultsContainer').classList.add('active');
    }, 2000);
  }

  collectAllResponses() {
    const formData = new FormData(document.getElementById('assessmentForm'));
    this.responses = {};
    
    for (const [key, value] of formData.entries()) {
      this.responses[key] = value;
    }
  }

  calculateDimensionScores() {
    // Initialize dimension scores
    this.dimensionScores = {
      dimension_1: { score: 0, count: 0, name: 'Pain Severity' },
      dimension_2: { score: 0, count: 0, name: 'Emotional Distress' },
      dimension_3: { score: 0, count: 0, name: 'Sleep & Function' },
      dimension_4: { score: 0, count: 0, name: 'Pain Interference' },
      dimension_5: { score: 0, count: 0, name: 'Cultural & Social Context' },
      dimension_6: { score: 0, count: 0, name: 'Treatment Preferences' }
    };
    
    // Process each section and question
    this.questionnaire.sections.forEach(section => {
      section.questions.forEach(question => {
        const response = this.responses[question.id];
        if (response !== undefined && question.scoring) {
          const scoring = question.scoring;
          const dimension = scoring.dimension;
          const weight = scoring.weight || 1.0;
          
          // Get numeric value
          let numericValue = parseFloat(response);
          
          // Handle yes/no responses
          if (question.type === 'yes_no') {
            numericValue = scoring.values[response] || 0;
          }
          
          // Apply reverse scoring if specified
          if (scoring.reverse) {
            const scale = question.scale;
            numericValue = (scale.max - numericValue) + scale.min;
          }
          
          // Normalize to 0-100 scale
          const scale = question.scale;
          let normalizedScore = 0;
          
          if (scale && scale.max && scale.min !== undefined) {
            normalizedScore = ((numericValue - scale.min) / (scale.max - scale.min)) * 100;
          } else {
            normalizedScore = numericValue;
          }
          
          // Add weighted score to dimension
          if (this.dimensionScores[dimension]) {
            this.dimensionScores[dimension].score += normalizedScore * weight;
            this.dimensionScores[dimension].count += weight;
          }
        }
      });
    });
    
    // Calculate average scores
    Object.keys(this.dimensionScores).forEach(dimension => {
      const dimData = this.dimensionScores[dimension];
      if (dimData.count > 0) {
        dimData.average = Math.round(dimData.score / dimData.count);
      } else {
        dimData.average = 0;
      }
    });
  }

  matchTreatments() {
    this.recommendedTreatments = [];
    
    // Calculate match score for each treatment
    this.treatments.pathways.forEach(pathway => {
      const matchScore = this.calculateTreatmentMatch(pathway);
      
      this.recommendedTreatments.push({
        pathway: pathway,
        matchScore: matchScore
      });
    });
    
    // Sort by match score (descending)
    this.recommendedTreatments.sort((a, b) => b.matchScore - a.matchScore);
    
    // Take top 3 recommendations
    this.recommendedTreatments = this.recommendedTreatments.slice(0, 3);
  }

  calculateTreatmentMatch(pathway) {
    let totalScore = 0;
    const rules = pathway.matching_rules;
    
    // Process primary indicators
    if (rules.primary_indicators) {
      rules.primary_indicators.forEach(indicator => {
        const dimensionScore = this.dimensionScores[indicator.dimension]?.average || 0;
        
        if (this.meetsThreshold(dimensionScore, indicator.threshold)) {
          totalScore += indicator.weight;
        }
      });
    }
    
    // Process secondary indicators
    if (rules.secondary_indicators) {
      rules.secondary_indicators.forEach(indicator => {
        const dimensionScore = this.dimensionScores[indicator.dimension]?.average || 0;
        
        if (this.meetsThreshold(dimensionScore, indicator.threshold)) {
          totalScore += indicator.weight;
        }
      });
    }
    
    // Check special conditions for multidisciplinary program
    if (rules.special_conditions) {
      const dim1 = this.dimensionScores.dimension_1?.average || 0;
      const dim2 = this.dimensionScores.dimension_2?.average || 0;
      const dim3 = this.dimensionScores.dimension_3?.average || 0;
      const dim4 = this.dimensionScores.dimension_4?.average || 0;
      
      // Multiple high dimensions
      const highDimensions = [dim1, dim2, dim3, dim4].filter(score => score >= 70).length;
      
      if (highDimensions >= 3 || (dim1 >= 75 && dim4 >= 75) || (dim2 >= 70 && dim3 <= 30)) {
        totalScore = 100; // Override for complex cases
      }
    }
    
    return Math.min(totalScore, 100); // Cap at 100
  }

  meetsThreshold(score, threshold) {
    switch (threshold) {
      case 'very_low':
        return score >= 0 && score <= 25;
      case 'low':
        return score >= 26 && score <= 40;
      case 'low_to_moderate':
        return score >= 41 && score <= 60;
      case 'moderate':
        return score >= 61 && score <= 75;
      case 'moderate_to_high':
        return score >= 67 && score <= 85;
      case 'high':
        return score >= 67 && score <= 100;
      case 'any':
        return true;
      default:
        // Handle specific thresholds
        return score >= 50; // Default moderate
    }
  }

  displayResults() {
    // Display dimension scores
    this.displayDimensionScores();
    
    // Display treatment recommendations
    this.displayRecommendations();
  }

  displayDimensionScores() {
    const container = document.getElementById('dimensionScores');
    container.innerHTML = '';
    
    Object.keys(this.dimensionScores).forEach(dimensionKey => {
      const dimension = this.dimensionScores[dimensionKey];
      
      const card = document.createElement('div');
      card.className = 'dimension-card';
      card.innerHTML = `
        <div class="dimension-name">${dimension.name}</div>
        <div class="dimension-score">${dimension.average}/100</div>
        <div class="dimension-bar">
          <div class="dimension-bar-fill" style="width: ${dimension.average}%"></div>
        </div>
      `;
      
      container.appendChild(card);
    });
  }

  displayRecommendations() {
    const container = document.getElementById('recommendationsList');
    container.innerHTML = '';
    
    this.recommendedTreatments.forEach((recommendation, index) => {
      const pathway = recommendation.pathway;
      const matchScore = recommendation.matchScore;
      
      const card = document.createElement('div');
      card.className = 'recommendation-card';
      
      // Benefits list
      const benefitsList = pathway.expected_benefits
        .map(benefit => `<li>${benefit}</li>`)
        .join('');
      
      // Resources list
      const resourcesList = pathway.resources
        .map(resource => `<li>${resource}</li>`)
        .join('');
      
      card.innerHTML = `
        <div class="recommendation-header">
          <div>
            <div class="recommendation-category">${pathway.category}</div>
            <h3 class="recommendation-title">${pathway.name}</h3>
            <div class="evidence-badge">${pathway.evidence_level}</div>
          </div>
          <div class="match-score">${matchScore}% Match</div>
        </div>
        
        <p class="recommendation-description">${pathway.description}</p>
        
        <div class="recommendation-details">
          <div class="detail-section">
            <div class="detail-title">Duration & Format</div>
            <div class="detail-content">
              ${pathway.duration}<br>
              <strong>Available as:</strong> ${pathway.modality.join(', ')}
            </div>
          </div>
          
          <div class="detail-section">
            <div class="detail-title">Expected Benefits</div>
            <div class="detail-content">
              <ul>${benefitsList}</ul>
            </div>
          </div>
          
          <div class="detail-section">
            <div class="detail-title">How to Access</div>
            <div class="detail-content">
              <ul>${resourcesList}</ul>
            </div>
          </div>
          
          ${pathway.contraindications.length > 0 ? `
            <div class="detail-section" style="background: rgba(208, 2, 27, 0.05);">
              <div class="detail-title" style="color: #d0021b;">Important Considerations</div>
              <div class="detail-content">
                <ul>${pathway.contraindications.map(c => `<li>${c}</li>`).join('')}</ul>
              </div>
            </div>
          ` : ''}
        </div>
      `;
      
      container.appendChild(card);
    });
  }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new PainAssessment();
});
