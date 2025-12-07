import React, { useEffect, useState, useRef } from 'react';
import { useGlobal } from '../context/GlobalContext';
import { DollarSign, TrendingUp, Package, Users, Download } from 'lucide-react';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';

interface KPI {
    revenue: number;
    profit: number;
    margin: number;
    volume: number;
}

const Dashboard: React.FC = () => {
    const { dateRange, region } = useGlobal();
    const [kpis, setKpis] = useState<KPI | null>(null);
    const [loading, setLoading] = useState(true);
    const dashboardRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const fetchKPIs = async () => {
            setLoading(true);
            try {
                const start = dateRange.start.toISOString().split('T')[0];
                const end = dateRange.end.toISOString().split('T')[0];
                const res = await fetch(`/api/kpis?start_date=${start}&end_date=${end}&region=${region}`);
                const data = await res.json();
                setKpis(data);
            } catch (error) {
                console.error("Failed to fetch KPIs", error);
            } finally {
                setLoading(false);
            }
        };

        fetchKPIs();
    }, [dateRange, region]);

    const handleExport = async () => {
        if (!dashboardRef.current) return;

        const canvas = await html2canvas(dashboardRef.current);
        const imgData = canvas.toDataURL('image/png');
        const pdf = new jsPDF('p', 'mm', 'a4');
        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pdfHeight = (canvas.height * pdfWidth) / canvas.width;

        pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
        pdf.save('dashboard-report.pdf');
    };

    if (loading) return <div>Loading KPIs...</div>;
    if (!kpis) return <div>Error loading data</div>;

    return (
        <div className="dashboard" ref={dashboardRef}>
            <div className="header-actions" style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '1rem' }}>
                <button className="btn btn-primary" onClick={handleExport} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <Download size={16} /> Export PDF
                </button>
            </div>

            <div className="kpi-grid">
                <div className="card kpi-card">
                    <div className="icon-wrapper revenue"><DollarSign size={24} /></div>
                    <div className="kpi-info">
                        <h3>Total Revenue</h3>
                        <p className="value">${kpis.revenue.toLocaleString()}</p>
                        <span className="trend positive">+12.5% vs last period</span>
                    </div>
                </div>

                <div className="card kpi-card">
                    <div className="icon-wrapper profit"><TrendingUp size={24} /></div>
                    <div className="kpi-info">
                        <h3>Net Profit</h3>
                        <p className="value">${kpis.profit.toLocaleString()}</p>
                        <span className="trend positive">Margin: {kpis.margin}%</span>
                    </div>
                </div>

                <div className="card kpi-card">
                    <div className="icon-wrapper volume"><Package size={24} /></div>
                    <div className="kpi-info">
                        <h3>Sales Volume</h3>
                        <p className="value">{kpis.volume.toLocaleString()}</p>
                        <span className="trend negative">-2.1% vs last period</span>
                    </div>
                </div>

                <div className="card kpi-card">
                    <div className="icon-wrapper customers"><Users size={24} /></div>
                    <div className="kpi-info">
                        <h3>Active Customers</h3>
                        <p className="value">1,245</p>
                        <span className="trend neutral">0% change</span>
                    </div>
                </div>
            </div>

            <div className="charts-section">
                <div className="card chart-card">
                    <h3>Revenue Trend</h3>
                    <div className="placeholder-chart">Chart Placeholder</div>
                </div>
                <div className="card chart-card">
                    <h3>Profit by Category</h3>
                    <div className="placeholder-chart">Chart Placeholder</div>
                </div>
            </div>

            <style>{`
        .kpi-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
          gap: 1.5rem;
          margin-bottom: 2rem;
        }
        .kpi-card {
          display: flex;
          align-items: center;
          gap: 1rem;
        }
        .icon-wrapper {
          width: 48px;
          height: 48px;
          border-radius: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
        }
        .revenue { background-color: var(--color-secondary); }
        .profit { background-color: var(--color-success); }
        .volume { background-color: var(--color-warning); }
        .customers { background-color: var(--color-accent); }
        
        .kpi-info h3 {
          margin: 0;
          font-size: 0.875rem;
          color: var(--text-secondary);
          font-weight: 500;
        }
        .value {
          margin: 0.25rem 0;
          font-size: 1.5rem;
          font-weight: 700;
          color: var(--text-primary);
        }
        .trend {
          font-size: 0.75rem;
          font-weight: 500;
        }
        .positive { color: var(--color-success); }
        .negative { color: var(--color-danger); }
        .neutral { color: var(--text-secondary); }
        
        .charts-section {
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          gap: 1.5rem;
        }
        .chart-card {
          min-height: 300px;
        }
        .placeholder-chart {
          height: 200px;
          background: #f1f5f9;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 0.5rem;
          color: var(--text-secondary);
        }

        @media (max-width: 768px) {
            .charts-section {
                grid-template-columns: 1fr;
            }
        }
      `}</style>
        </div>
    );
};

export default Dashboard;
