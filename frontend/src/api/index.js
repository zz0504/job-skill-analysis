import request from './request'

export const api = {
  health: () => request.get('/health'),
  
  login: (data) => request.post('/auth/login', data),
  
  register: (data) => request.post('/auth/register', data),
  
  getCurrentUser: () => request.get('/auth/me'),
  
  upload: (formData) => request.post('/upload/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  
  loadTestData: () => request.post('/upload/test-data'),
  
  getJobs: (params) => request.get('/upload/preview/' + params.batch_id, { params }),
  
  cleanData: (batchId) => request.post(`/jobs/clean/${batchId}`),
  
  getCleanStatus: (batchId) => request.get(`/jobs/clean/status/${batchId}`),
  
  getLatestBatch: () => request.get('/batch/latest'),
  
  analyzeKeywords: (batchId, params) => request.post(`/keywords/analyze/${batchId}`, null, { params }),
  
  getKeywords: (params) => request.get('/keywords/', { params }),
  
  getTrend: (params) => request.get('/keywords/trend', { params }),
  
  getMatrix: (params) => request.get('/matrix/', { params }),
  
  getMatrixTable: (params) => request.get('/matrix/table', { params }),
  
  generateReport: (params) => request.post('/report', params)
}
