import axios from 'axios';
import { API_URL } from './config';

const API_BASE = API_URL;

const FALLBACK_TEMPLATES = [
  'Polyhedron',
  'blue',
  'green',
  'silver_stone',
  'gradation_green',
  'yellow_subhan'
];

const api = {
  uploadPdf: async (file: File) => {
    const formData = new FormData();
    formData.append('pdf', file);
    
    try {
      const response = await axios.post(`${API_BASE}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error uploading PDF:', error);
      throw error;
    }
  },
  
  getTemplates: async () => {
    try {
      const response = await axios.get(`${API_BASE}/templates`);
      const data = response.data;
      if (Array.isArray(data)) {
        return data.map(t => (typeof t === 'string' ? t : t.name)).filter(Boolean);
      }
      return FALLBACK_TEMPLATES;
    } catch (error) {
      return FALLBACK_TEMPLATES;
    }
  },
  
  generateNotes: async (fileId: string, selectedTopics: string[], genConfig: any) => {
    try {
      const response = await axios.post(`${API_BASE}/generate`, { fileId, selectedTopics, generation_config: genConfig });
      return response.data;
    } catch (error) {
      console.error('Error generating notes:', error);
      throw error;
    }
  },

  // Use FormData to avoid CORS preflight and backends expecting form fields
  generateSummary: async (fileId: string, summaryType: string, genConfig: any) => {
    const formData = new FormData();
    formData.append('fileId', fileId);
    formData.append('summaryType', summaryType);
    formData.append('generation_config', JSON.stringify(genConfig));

    try {
      const response = await axios.post(`${API_BASE}/summary`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      return response.data;
    } catch (error: any) {
      // Surface clearer error when server returns HTML (e.g., 404 page)
      const status = error?.response?.status;
      const contentType = error?.response?.headers?.['content-type'] || '';
      if (status && typeof error?.response?.data === 'string' && contentType.includes('text/html')) {
        throw new Error(`Request failed with status ${status} (HTML response). Is the /summary route implemented?`);
      }
      console.error('Error generating summary:', error);
      throw error;
    }
  },

  generateSlides: async (fileId: string, selectedTopics: string[], title: string, template: string, genConfig: any) => {
    try {
      const response = await axios.post(`${API_BASE}/slides`, { fileId, selectedTopics, title, template, generation_config: genConfig });
      return response.data;
    } catch (error) {
      console.error('Error generating slides:', error);
      throw error;
    }
  },

  rewriteDocument: async (fileId: string) => {
    try {
      const response = await axios.post(`${API_BASE}/rewrite`, { fileId });
      return response.data;
    } catch (error) {
      console.error('Error rewriting document:', error);
      throw error;
    }
  },
  
  checkProgress: async (taskId: string) => {
    try {
      const response = await axios.get(`${API_BASE}/progress/${taskId}`);
      return response.data;
    } catch (error) {
      console.error('Error checking progress:', error);
      throw error;
    }
  },
  
  download: async (taskId: string, fallbackFilename = 'download') => {
    try {
      const response = await axios.get(`${API_BASE}/download/${taskId}`, {
        responseType: 'blob'
      });

      let filename = fallbackFilename;
      const disposition = response.headers['content-disposition'];
      if (disposition) {
        const match = disposition.match(/filename\*=UTF-8''([^;\n]+)/) || disposition.match(/filename="?([^";\n]+)/);
        if (match && match[1]) {
          filename = decodeURIComponent(match[1].replace(/"/g, ''));
        }
      } else {
        const contentType = response.headers['content-type'] || '';
        if (contentType.includes('application/pdf')) {
          if (!filename.endsWith('.pdf')) filename += '.pdf';
        } else if (contentType.includes('presentation')) {
          if (!filename.endsWith('.pptx')) filename += '.pptx';
        }
      }

      const blob = new Blob([response.data]);
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      return true;
    } catch (error) {
      console.error('Error downloading file:', error);
      throw error;
    }
  }
};

export default api;
