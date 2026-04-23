// API Configuration for The Chronic Pain Hub
// This file centralizes the backend API URL configuration

// Automatic configuration based on environment
const getApiBase = () => {
  // Always use the current origin (works for localhost and ngrok)
  // The Module4_Server.py proxies backend requests through /api/pain-mapping/*
  return window.location.origin;
};

// Export the API base URL
window.API_CONFIG = {
  BASE_URL: getApiBase(),
  
  // You can also manually override the URL here for testing
  // Uncomment and set your ngrok URL:
  // BASE_URL: 'https://your-ngrok-id.ngrok-free.app',
};

console.log('🔧 API Configuration loaded:', window.API_CONFIG.BASE_URL || 'Same origin');
