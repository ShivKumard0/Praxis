import React, { useEffect, useState } from 'react';
import { useGlobal } from '../context/GlobalContext';
import { Bar } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement,
    PointElement,
    LineElement,
    LineController,
    BarController
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement,
    PointElement,
    LineElement,
    LineController,
    BarController
);

const ProfitDiagnostic: React.FC = () => {
    const { dateRange } = useGlobal();
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const start = dateRange.start.toISOString().split('T')[0];
                const end = dateRange.end.toISOString().split('T')[0];
                const res = await fetch(`/api/profit-diagnostic?start_date=${start}&end_date=${end}`);
                const json = await res.json();
                setData(json);
            } catch (error) {
                console.error("Failed to fetch profit data", error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [dateRange]);

    if (loading) return <div>Loading Analysis...</div>;
    if (!data) return <div>Error loading data</div>;

    // Waterfall Chart Config
    const waterfallLabels = data.waterfall.map((d: any) => d.label);
    const waterfallValues = data.waterfall.map((d: any) => d.value);
    const waterfallColors = data.waterfall.map((d: any) =>
        d.type === 'positive' ? '#10b981' : (d.type === 'negative' ? '#ef4444' : '#3b82f6')
    );

    const waterfallChartData = {
        labels: waterfallLabels,
        datasets: [
            {
                type: 'bar' as const,
                label: 'Profit Waterfall',
                data: waterfallValues,
                backgroundColor: waterfallColors,
            },
        ],
    };

    // Pareto Chart Config
    const paretoLabels = data.pareto.slice(0, 10).map((d: any) => d.category);
    const paretoValues = data.pareto.slice(0, 10).map((d: any) => d.profit);
    const paretoCumulative = data.pareto.slice(0, 10).map((d: any) => d.cumulative_percentage);

    const paretoChartData = {
        labels: paretoLabels,
        datasets: [
            {
                type: 'bar' as const,
                label: 'Profit Contribution',
                data: paretoValues,
                backgroundColor: '#3b82f6',
                yAxisID: 'y',
                order: 2
            },
            {
                type: 'line' as const,
                label: 'Cumulative %',
                data: paretoCumulative,
                borderColor: '#f59e0b',
                borderWidth: 2,
                yAxisID: 'y1',
                order: 1
            },
        ],
    };

    return (
        <div className="profit-diagnostic">
            <div className="card chart-container">
                <h3>Profitability Waterfall</h3>
                <p className="subtitle">Breakdown of Revenue to Net Profit</p>
                <div className="chart-wrapper">
                    <Bar data={waterfallChartData} options={{ maintainAspectRatio: false }} />
                </div>
            </div>

            <div className="card chart-container">
                <h3>Pareto Analysis (80/20 Rule)</h3>
                <p className="subtitle">Top Categories Driving Profit</p>
                <div className="chart-wrapper">
                    <Bar
                        data={paretoChartData as any}
                        options={{
                            maintainAspectRatio: false,
                            scales: {
                                y: { type: 'linear', display: true, position: 'left' },
                                y1: { type: 'linear', display: true, position: 'right', grid: { drawOnChartArea: false } },
                            }
                        }}
                    />
                </div>
            </div>

            <style>{`
        .profit-diagnostic {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 1.5rem;
        }
        .chart-container {
          height: 400px;
          display: flex;
          flex-direction: column;
        }
        .chart-wrapper {
          flex: 1;
          position: relative;
        }
        .subtitle {
          color: var(--text-secondary);
          font-size: 0.875rem;
          margin-bottom: 1rem;
        }
      `}</style>
        </div>
    );
};

export default ProfitDiagnostic;
