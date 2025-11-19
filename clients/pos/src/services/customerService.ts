import { apiClient } from './apiClient';
import type { Customer } from '../types';

export const lookupCustomer = (search: string, authToken?: string) =>
  apiClient<Customer[]>(`/customers?query=${encodeURIComponent(search)}`, {
    method: 'GET',
    authToken
  });
