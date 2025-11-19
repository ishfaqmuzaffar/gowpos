export type Role = 'cashier' | 'manager' | 'admin';

export interface UserProfile {
  id: string;
  email: string;
  displayName: string;
  role: Role;
}

export interface Product {
  id: string;
  sku: string;
  name: string;
  price: number;
  stock: number;
  category: string;
}

export interface CartItem {
  product: Product;
  quantity: number;
}

export interface Customer {
  id: string;
  name: string;
  email?: string;
  phone?: string;
  loyaltyBalance?: number;
}

export interface InventoryItem extends Product {
  reorderLevel: number;
  supplier?: string;
}

export interface PaymentDetails {
  method: 'cash' | 'card' | 'mobile';
  amount: number;
  reference?: string;
}

export interface CheckoutPayload {
  cart: CartItem[];
  total: number;
  customer?: Customer;
  payments: PaymentDetails[];
}

export interface DailyReportSummary {
  id: string;
  businessDate: string;
  grossSales: number;
  netSales: number;
  totalTransactions: number;
  bestSeller?: string;
}
