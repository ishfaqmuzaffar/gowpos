import { apiClient } from './apiClient';
import type { Product, InventoryItem } from '../types';

export const searchProducts = (query: string, authToken?: string) =>
  apiClient<Product[]>(`/products?query=${encodeURIComponent(query)}`, {
    method: 'GET',
    authToken
  });

export const fetchInventory = (authToken?: string) =>
  apiClient<InventoryItem[]>('/inventory', {
    method: 'GET',
    authToken
  });
