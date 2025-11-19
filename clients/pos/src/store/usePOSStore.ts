import { create } from 'zustand';
import type {
  CartItem,
  CheckoutPayload,
  Customer,
  DailyReportSummary,
  InventoryItem,
  Product,
  UserProfile
} from '../types';
import { login as loginRequest, register as registerRequest } from '../services/authService';
import { searchProducts as searchProductsRequest, fetchInventory } from '../services/productService';
import { lookupCustomer } from '../services/customerService';
import { fetchReports, postTransaction } from '../services/transactionService';

interface POSState {
  token?: string;
  currentUser?: UserProfile;
  isAuthenticated: boolean;
  loading: boolean;
  error?: string;
  products: Product[];
  inventory: InventoryItem[];
  customers: Customer[];
  cart: CartItem[];
  reports: DailyReportSummary[];
  login: (email: string, password: string) => Promise<void>;
  register: (payload: { email: string; password: string; displayName: string }) => Promise<void>;
  logout: () => void;
  searchProducts: (query: string) => Promise<void>;
  addToCart: (product: Product) => void;
  removeFromCart: (productId: string) => void;
  updateQuantity: (productId: string, quantity: number) => void;
  lookupCustomer: (query: string) => Promise<void>;
  loadInventory: () => Promise<void>;
  submitCheckout: (payload: CheckoutPayload) => Promise<string>;
  loadReports: (businessDate?: string) => Promise<void>;
}

export const usePOSStore = create<POSState>((set, get) => ({
  token: undefined,
  currentUser: undefined,
  isAuthenticated: false,
  loading: false,
  error: undefined,
  products: [],
  inventory: [],
  customers: [],
  cart: [],
  reports: [],
  async login(email, password) {
    set({ loading: true, error: undefined });
    try {
      const response = await loginRequest(email, password);
      set({
        token: response.token,
        currentUser: response.user,
        isAuthenticated: true,
        loading: false
      });
    } catch (error) {
      set({ error: (error as Error).message, loading: false });
      throw error;
    }
  },
  async register(payload) {
    set({ loading: true, error: undefined });
    try {
      const response = await registerRequest(payload);
      set({
        token: response.token,
        currentUser: response.user,
        isAuthenticated: true,
        loading: false
      });
    } catch (error) {
      set({ error: (error as Error).message, loading: false });
      throw error;
    }
  },
  logout() {
    set({ token: undefined, currentUser: undefined, isAuthenticated: false, cart: [] });
  },
  async searchProducts(query) {
    const { token } = get();
    set({ loading: true, error: undefined });
    try {
      const products = await searchProductsRequest(query, token);
      set({ products, loading: false });
    } catch (error) {
      set({ error: (error as Error).message, loading: false });
    }
  },
  addToCart(product) {
    set((state) => {
      const existing = state.cart.find((item) => item.product.id === product.id);
      if (existing) {
        return {
          cart: state.cart.map((item) =>
            item.product.id === product.id
              ? { ...item, quantity: item.quantity + 1 }
              : item
          )
        };
      }
      return { cart: [...state.cart, { product, quantity: 1 }] };
    });
  },
  removeFromCart(productId) {
    set((state) => ({ cart: state.cart.filter((item) => item.product.id !== productId) }));
  },
  updateQuantity(productId, quantity) {
    if (quantity <= 0) {
      set((state) => ({ cart: state.cart.filter((item) => item.product.id !== productId) }));
      return;
    }

    set((state) => ({
      cart: state.cart.map((item) =>
        item.product.id === productId
          ? { ...item, quantity }
          : item
      )
    }));
  },
  async lookupCustomer(query) {
    const { token } = get();
    set({ loading: true, error: undefined });
    try {
      const customers = await lookupCustomer(query, token);
      set({ customers, loading: false });
    } catch (error) {
      set({ error: (error as Error).message, loading: false });
    }
  },
  async loadInventory() {
    const { token } = get();
    set({ loading: true, error: undefined });
    try {
      const inventory = await fetchInventory(token);
      set({ inventory, loading: false });
    } catch (error) {
      set({ error: (error as Error).message, loading: false });
    }
  },
  async submitCheckout(payload) {
    const { token } = get();
    set({ loading: true, error: undefined });
    try {
      const { receiptId } = await postTransaction(payload, token);
      set({ cart: [], loading: false });
      return receiptId;
    } catch (error) {
      const message = (error as Error).message;
      set({ error: message, loading: false });
      throw error;
    }
  },
  async loadReports(businessDate) {
    const { token } = get();
    set({ loading: true, error: undefined });
    try {
      const reports = await fetchReports(businessDate, token);
      set({ reports, loading: false });
    } catch (error) {
      set({ error: (error as Error).message, loading: false });
    }
  }
}));
