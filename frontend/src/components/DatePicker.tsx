import React from 'react';
import { useGlobal } from '../context/GlobalContext';
import { Calendar } from 'lucide-react';

const DatePicker: React.FC = () => {
  const { setDateRange } = useGlobal();

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const val = e.target.value;
    const end = new Date();
    let start = new Date();

    if (val === '30') start.setDate(end.getDate() - 30);
    else if (val === '90') start.setDate(end.getDate() - 90);
    else if (val === '365') start.setDate(end.getDate() - 365);
    else {
      start = new Date('2023-01-01'); // All time
    }

    setDateRange({ start, end });
  };

  return (
    <div className="date-picker">
      <Calendar size={16} />
      <select onChange={handleChange} className="date-select">
        <option value="all">All Time</option>
        <option value="30">Last 30 Days</option>
        <option value="90">Last 90 Days</option>
        <option value="365">Last Year</option>
      </select>
      <style>{`
        .date-picker {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          background: var(--bg-body);
          padding: 0.5rem;
          border-radius: 0.375rem;
          border: 1px solid var(--border-color);
        }
        .date-select {
          border: none;
          background: transparent;
          font-family: inherit;
          color: var(--text-primary);
          outline: none;
        }
      `}</style>
    </div>
  );
};

export default DatePicker;
