// API Configuration for The Chronic Pain Hub
// This file centralizes the backend API URL configuration

// Automatic configuration based on environment
const getApiBase = () => {
  // If running from file:// protocol (directly opened HTML)
  if (window.location.protocol === 'file:') {
    // Use localhost backend
    return 'http://localhost:8000';
  }
  
  // If running from http://localhost or http://127.0.0.1
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    // Use same origin (empty string means relative URLs)
    return '';
  }
  
  // If running from a remote server (e.g., GitHub Pages, ngrok-served HTML)
  // Return the ngrok URL or your production backend URL
  return 'http://localhost:8000';  // ⚠️ CHANGE THIS to your ngrok URL
};

// Export the API base URL
window.API_CONFIG = {
  BASE_URL: getApiBase(),
  
  // You can also manually override the URL here for testing
  // Uncomment and set your ngrok URL:
  // BASE_URL: 'https://your-ngrok-id.ngrok-free.app',
};

console.log('🔧 API Configuration loaded:', window.API_CONFIG.BASE_URL || 'Same origin');
