import React, { useState, useEffect } from 'react';

interface Step {
    target: string;
    title: string;
    content: string;
    position: 'top' | 'bottom' | 'left' | 'right';
}

const STEPS: Step[] = [
    {
        target: '.sidebar',
        title: 'Navigation',
        content: 'Access different modules like Profit, Demand, and Inventory here.',
        position: 'right'
    },
    {
        target: '.date-picker',
        title: 'Global Filters',
        content: 'Change the date range to filter data across the entire platform.',
        position: 'bottom'
    },
    {
        target: '.kpi-grid',
        title: 'Key Metrics',
        content: 'View high-level KPIs to get a quick pulse of the business.',
        position: 'bottom'
    }
];

const OnboardingTour: React.FC = () => {
    const [currentStep, setCurrentStep] = useState(0);
    const [isVisible, setIsVisible] = useState(false);
    const [style, setStyle] = useState<React.CSSProperties>({});

    useEffect(() => {
        const hasSeenTour = localStorage.getItem('hasSeenTour');
        if (!hasSeenTour) {
            setIsVisible(true);
        }
    }, []);

    useEffect(() => {
        if (!isVisible) return;

        const step = STEPS[currentStep];
        const element = document.querySelector(step.target);

        if (element) {
            const rect = element.getBoundingClientRect();
            let top = 0;
            let left = 0;

            // Simple positioning logic
            if (step.position === 'right') {
                top = rect.top + 20;
                left = rect.right + 20;
            } else if (step.position === 'bottom') {
                top = rect.bottom + 20;
                left = rect.left;
            }

            setStyle({
                top: `${top}px`,
                left: `${left}px`,
                position: 'fixed',
                zIndex: 1000
            });
        }
    }, [currentStep, isVisible]);

    const handleNext = () => {
        if (currentStep < STEPS.length - 1) {
            setCurrentStep(currentStep + 1);
        } else {
            handleClose();
        }
    };

    const handleClose = () => {
        setIsVisible(false);
        localStorage.setItem('hasSeenTour', 'true');
    };

    if (!isVisible) return null;

    return (
        <>
            <div className="tour-overlay" />
            <div className="tour-tooltip card" style={style}>
                <h4>{STEPS[currentStep].title}</h4>
                <p>{STEPS[currentStep].content}</p>
                <div className="tour-actions">
                    <button className="btn" onClick={handleClose}>Skip</button>
                    <button className="btn btn-primary" onClick={handleNext}>
                        {currentStep === STEPS.length - 1 ? 'Finish' : 'Next'}
                    </button>
                </div>
            </div>
            <style>{`
        .tour-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0, 0, 0, 0.5);
          z-index: 999;
          pointer-events: none; /* Allow clicking through if needed, but usually blocks */
        }
        .tour-tooltip {
          width: 300px;
          animation: fadeIn 0.3s;
        }
        .tour-actions {
          display: flex;
          justify-content: flex-end;
          gap: 0.5rem;
          margin-top: 1rem;
        }
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>
        </>
    );
};

export default OnboardingTour;
