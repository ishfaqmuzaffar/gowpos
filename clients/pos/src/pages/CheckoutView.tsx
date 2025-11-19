import { FormEvent, useMemo, useState } from 'react';
import { usePOSStore } from '../store/usePOSStore';
import type { Customer, PaymentDetails } from '../types';

const paymentOptions: PaymentDetails['method'][] = ['cash', 'card', 'mobile'];

const CheckoutView = () => {
  const { cart, customers, lookupCustomer, submitCheckout, loading } = usePOSStore();
  const [selectedCustomer, setSelectedCustomer] = useState<Customer | undefined>(undefined);
  const [customerQuery, setCustomerQuery] = useState('');
  const [payments, setPayments] = useState<PaymentDetails[]>([
    { method: 'cash', amount: 0 }
  ]);
  const [status, setStatus] = useState('');

  const total = useMemo(
    () => cart.reduce((sum, item) => sum + item.product.price * item.quantity, 0),
    [cart]
  );

  const handleCustomerSearch = async () => {
    await lookupCustomer(customerQuery);
  };

  const handlePaymentChange = (index: number, updates: Partial<PaymentDetails>) => {
    setPayments((prev) =>
      prev.map((payment, idx) => (idx === index ? { ...payment, ...updates } : payment))
    );
  };

  const addPaymentRow = () => setPayments((prev) => [...prev, { method: 'cash', amount: 0 }]);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setStatus('');
    try {
      const receipt = await submitCheckout({
        cart,
        total,
        customer: selectedCustomer,
        payments
      });
      setStatus(`Transaction successful. Receipt #${receipt}`);
    } catch (err) {
      setStatus((err as Error).message);
    }
  };

  return (
    <section>
      <div className="card">
        <h2>Checkout</h2>
        <p>Total due: ${total.toFixed(2)}</p>
      </div>
      <form className="card form-grid" onSubmit={handleSubmit}>
        <section>
          <h3>Customer</h3>
          <div className="form-grid two">
            <input
              placeholder="Name, email, phone"
              value={customerQuery}
              onChange={(e) => setCustomerQuery(e.target.value)}
            />
            <button className="secondary" type="button" onClick={handleCustomerSearch}>
              Lookup
            </button>
          </div>
          <div className="form-grid">
            {customers.map((customer) => (
              <label key={customer.id} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <input
                  type="radio"
                  name="customer"
                  checked={selectedCustomer?.id === customer.id}
                  onChange={() => setSelectedCustomer(customer)}
                />
                <span>
                  {customer.name}
                  {customer.loyaltyBalance && (
                    <small style={{ marginLeft: '0.5rem', color: '#6b7280' }}>
                      Loyalty: {customer.loyaltyBalance}
                    </small>
                  )}
                </span>
              </label>
            ))}
          </div>
        </section>

        <section>
          <h3>Payments</h3>
          {payments.map((payment, index) => (
            <div key={index} className="form-grid two">
              <select
                value={payment.method}
                onChange={(e) => handlePaymentChange(index, { method: e.target.value as PaymentDetails['method'] })}
              >
                {paymentOptions.map((option) => (
                  <option key={option} value={option}>
                    {option.toUpperCase()}
                  </option>
                ))}
              </select>
              <input
                type="number"
                min={0}
                step="0.01"
                value={payment.amount}
                onChange={(e) => handlePaymentChange(index, { amount: Number(e.target.value) })}
              />
            </div>
          ))}
          <button className="secondary" type="button" onClick={addPaymentRow}>
            Split payment
          </button>
        </section>
        <button className="primary" type="submit" disabled={loading || total === 0}>
          {loading ? 'Sending...' : 'Complete Sale'}
        </button>
        {status && <p className="status-pill warning">{status}</p>}
      </form>
    </section>
  );
};

export default CheckoutView;
