import { FormEvent, useState } from 'react';
import { usePOSStore } from '../store/usePOSStore';
import type { Product } from '../types';

const ProductSearchView = () => {
  const { products, searchProducts, addToCart, loading } = usePOSStore();
  const [query, setQuery] = useState('');

  const handleSearch = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    await searchProducts(query);
  };

  const renderProduct = (product: Product) => (
    <div key={product.id} className="card" style={{ marginBottom: '1rem' }}>
      <h3>{product.name}</h3>
      <p>
        SKU: {product.sku} · Category: {product.category}
      </p>
      <p>
        <strong>${product.price.toFixed(2)}</strong> · {product.stock} in stock
      </p>
      <button className="primary" onClick={() => addToCart(product)}>
        Add to cart
      </button>
    </div>
  );

  return (
    <section>
      <div className="card">
        <h2>Product Search</h2>
        <form onSubmit={handleSearch} className="form-grid two">
          <input
            placeholder="SKU, name, category"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button className="primary" type="submit" disabled={loading}>
            {loading ? 'Searching…' : 'Search'}
          </button>
        </form>
      </div>
      {products.length === 0 && <p className="card">Search results will appear here.</p>}
      {products.map(renderProduct)}
    </section>
  );
};

export default ProductSearchView;
