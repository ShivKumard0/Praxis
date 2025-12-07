import React, { useEffect, useState } from 'react';
import { useGlobal } from '../context/GlobalContext';
import { Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
);

const DemandForecast: React.FC = () => {
    const { region } = useGlobal();
    const [data, setData] = useState<any[] | null>(null);
    const [loading, setLoading] = useState(true);
    const [category, setCategory] = useState('Furniture');
    const [subCategory, setSubCategory] = useState('Chairs');

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const res = await fetch(`/api/demand-forecast?region=${region}&category=${category}&sub_category=${subCategory}&days=90`);
                const json = await res.json();
                if (json.error) {
                    console.error(json.error);
                    setData([]);
                } else {
                    setData(json);
                }
            } catch (error) {
                console.error("Failed to fetch forecast", error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [region, category, subCategory]);

    if (loading) return <div>Loading Forecast...</div>;
    if (!data) return <div>Error loading data</div>;

    const labels = data.map((d: any) => d.date);
    const forecastValues = data.map((d: any) => d.forecast);
    const upperCI = data.map((d: any) => d.upper_ci);
    const lowerCI = data.map((d: any) => d.lower_ci);

    const chartData = {
        labels,
        datasets: [
            {
                label: 'Forecast Demand',
                data: forecastValues,
                borderColor: '#3b82f6',
                backgroundColor: '#3b82f6',
                tension: 0.4,
            },
            {
                label: 'Upper CI (95%)',
                data: upperCI,
                borderColor: 'transparent',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                fill: '+1', // Fill to next dataset (Lower CI)
                pointRadius: 0,
            },
            {
                label: 'Lower CI (95%)',
                data: lowerCI,
                borderColor: 'transparent',
                backgroundColor: 'transparent',
                fill: false,
                pointRadius: 0,
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top' as const,
            },
            title: {
                display: true,
                text: `Demand Forecast: ${category} - ${subCategory} (${region})`,
            },
        },
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Quantity'
                }
            }
        }
    };

    return (
        <div className="demand-forecast">
            <div className="controls card">
                <div className="control-group">
                    <label>Category</label>
                    <select value={category} onChange={(e) => setCategory(e.target.value)}>
                        <option value="Furniture">Furniture</option>
                        <option value="Office Supplies">Office Supplies</option>
                        <option value="Technology">Technology</option>
                    </select>
                </div>
                <div className="control-group">
                    <label>Sub-Category</label>
                    <select value={subCategory} onChange={(e) => setSubCategory(e.target.value)}>
                        {category === 'Furniture' && (
                            <>
                                <option value="Bookcases">Bookcases</option>
                                <option value="Chairs">Chairs</option>
                                <option value="Tables">Tables</option>
                            </>
                        )}
                        {category === 'Office Supplies' && (
                            <>
                                <option value="Binders">Binders</option>
                                <option value="Paper">Paper</option>
                                <option value="Storage">Storage</option>
                            </>
                        )}
                        {category === 'Technology' && (
                            <>
                                <option value="Phones">Phones</option>
                                <option value="Accessories">Accessories</option>
                                <option value="Machines">Machines</option>
                            </>
                        )}
                    </select>
                </div>
            </div>

            <div className="card chart-container">
                <Line data={chartData} options={options} />
            </div>

            <style>{`
        .demand-forecast {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }
        .controls {
          display: flex;
          gap: 2rem;
          padding: 1rem 2rem;
        }
        .control-group {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }
        .control-group label {
          font-size: 0.875rem;
          color: var(--text-secondary);
        }
        .control-group select {
          padding: 0.5rem;
          border-radius: 0.375rem;
          border: 1px solid var(--border-color);
          min-width: 200px;
        }
        .chart-container {
          height: 500px;
        }
      `}</style>
        </div>
    );
};

export default DemandForecast;
