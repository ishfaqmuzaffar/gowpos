import { useMemo } from 'react';
import { usePOSStore } from '../store/usePOSStore';

const CartView = () => {
  const { cart, updateQuantity, removeFromCart } = usePOSStore();
  const total = useMemo(
    () => cart.reduce((sum, item) => sum + item.product.price * item.quantity, 0),
    [cart]
  );

  return (
    <section className="card">
      <h2>Cart</h2>
      {cart.length === 0 && <p>Your cart is empty.</p>}
      {cart.map((item) => (
        <div key={item.product.id} style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ flex: 1 }}>
            <strong>{item.product.name}</strong>
            <p>${item.product.price.toFixed(2)}</p>
          </div>
          <input
            type="number"
            min={1}
            value={item.quantity}
            onChange={(e) => updateQuantity(item.product.id, Number(e.target.value))}
            style={{ width: '80px' }}
          />
          <button className="secondary" onClick={() => removeFromCart(item.product.id)}>
            Remove
          </button>
        </div>
      ))}
      <hr style={{ margin: '1.5rem 0' }} />
      <h3>Total: ${total.toFixed(2)}</h3>
    </section>
  );
};

export default CartView;
