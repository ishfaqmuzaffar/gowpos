import { apiClient } from './apiClient';
import type { CheckoutPayload, DailyReportSummary } from '../types';

export const postTransaction = (payload: CheckoutPayload, authToken?: string) =>
  apiClient<{ receiptId: string }>('/transactions', {
    method: 'POST',
    body: JSON.stringify(payload),
    authToken
  });

export const fetchReports = (businessDate?: string, authToken?: string) => {
  const params = businessDate ? `?businessDate=${encodeURIComponent(businessDate)}` : '';
  return apiClient<DailyReportSummary[]>(`/reports${params}`, {
    method: 'GET',
    authToken
  });
};
