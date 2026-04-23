/**
 * API Service for Pain Mapping
 * Connects the React frontend to the Python FastAPI backend
 */

// Use relative URL so it works with ngrok and local development
// The Module4_Server.py will proxy requests to the Backend API (port 8000)
const API_BASE_URL = window.location.origin; // Same origin as frontend

export interface PainMapData {
  session_id: string;
  patient_id?: string | null;
  front_canvas_data?: string;
  back_canvas_data?: string;
  pain_regions: any[];
  overall_intensity: number;
  sensation_breakdown: Record<string, number>;
  total_strokes: number;
}

export interface PainReport {
  report_id: string;
  patient_id?: string | null;
  generated_at: string;
  summary: string;
  pain_regions_summary: any[];
  dominant_sensations: string[];
  neuropathic_probability: string;
  recommended_specialists: string[];
  mapping_data: PainMapData;
}

class PainMappingAPI {
  /**
   * Save pain mapping data to backend
   */
  async savePainMapping(data: PainMapData): Promise<any> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/pain-mapping/save`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error saving pain mapping:', error);
      throw error;
    }
  }

  /**
   * Generate pain report from mapping data
   */
  async generateReport(data: PainMapData): Promise<{ status: string; report: PainReport }> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/pain-mapping/generate-report`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error generating report:', error);
      throw error;
    }
  }

  /**
   * Get pain types configuration
   */
  async getPainTypes(): Promise<any> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/pain-mapping/pain-types`);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching pain types:', error);
      throw error;
    }
  }
}

export const painMappingAPI = new PainMappingAPI();
