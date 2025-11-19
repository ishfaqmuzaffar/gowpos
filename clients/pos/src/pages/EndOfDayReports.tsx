import { FormEvent, useEffect, useState } from 'react';
import { usePOSStore } from '../store/usePOSStore';

const EndOfDayReports = () => {
  const { reports, loadReports, loading } = usePOSStore();
  const [businessDate, setBusinessDate] = useState(() => new Date().toISOString().slice(0, 10));

  useEffect(() => {
    void loadReports();
  }, [loadReports]);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    await loadReports(businessDate);
  };

  return (
    <section className="card">
      <h2>End of Day Reports</h2>
      <form onSubmit={handleSubmit} className="form-grid two" style={{ marginBottom: '1rem' }}>
        <input type="date" value={businessDate} onChange={(e) => setBusinessDate(e.target.value)} />
        <button className="primary" type="submit" disabled={loading}>
          {loading ? 'Loading...' : 'Filter'}
        </button>
      </form>
      <table className="table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Gross Sales</th>
            <th>Net Sales</th>
            <th>Transactions</th>
            <th>Best Seller</th>
          </tr>
        </thead>
        <tbody>
          {reports.map((report) => (
            <tr key={report.id}>
              <td>{report.businessDate}</td>
              <td>${report.grossSales.toFixed(2)}</td>
              <td>${report.netSales.toFixed(2)}</td>
              <td>{report.totalTransactions}</td>
              <td>{report.bestSeller ?? 'N/A'}</td>
            </tr>
          ))}
          {reports.length === 0 && (
            <tr>
              <td colSpan={5}>No data yet.</td>
            </tr>
          )}
        </tbody>
      </table>
    </section>
  );
};

export default EndOfDayReports;
