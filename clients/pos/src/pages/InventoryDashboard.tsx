import { useEffect } from 'react';
import { usePOSStore } from '../store/usePOSStore';

const InventoryDashboard = () => {
  const { inventory, loadInventory, loading } = usePOSStore();

  useEffect(() => {
    if (inventory.length === 0) {
      void loadInventory();
    }
  }, [inventory.length, loadInventory]);

  return (
    <section className="card">
      <h2>Inventory</h2>
      <button className="secondary" onClick={() => loadInventory()} disabled={loading}>
        {loading ? 'Refreshing…' : 'Refresh'}
      </button>
      <table className="table" style={{ marginTop: '1rem' }}>
        <thead>
          <tr>
            <th>SKU</th>
            <th>Name</th>
            <th>Stock</th>
            <th>Reorder Level</th>
            <th>Supplier</th>
          </tr>
        </thead>
        <tbody>
          {inventory.map((item) => (
            <tr key={item.id}>
              <td>{item.sku}</td>
              <td>{item.name}</td>
              <td>{item.stock}</td>
              <td>
                <span className={`status-pill ${item.stock <= item.reorderLevel ? 'warning' : 'success'}`}>
                  {item.reorderLevel}
                </span>
              </td>
              <td>{item.supplier ?? 'N/A'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
};

export default InventoryDashboard;
