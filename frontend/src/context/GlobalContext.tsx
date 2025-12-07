import React, { createContext, useContext, useState } from 'react';

interface GlobalContextType {
    dateRange: { start: Date; end: Date };
    setDateRange: (range: { start: Date; end: Date }) => void;
    region: string;
    setRegion: (region: string) => void;
}

const GlobalContext = createContext<GlobalContextType | undefined>(undefined);

export const GlobalProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [dateRange, setDateRange] = useState({
        start: new Date('2023-01-01'),
        end: new Date('2025-12-31')
    });
    const [region, setRegion] = useState('All');

    return (
        <GlobalContext.Provider value={{ dateRange, setDateRange, region, setRegion }}>
            {children}
        </GlobalContext.Provider>
    );
};

export const useGlobal = () => {
    const context = useContext(GlobalContext);
    if (!context) {
        throw new Error('useGlobal must be used within a GlobalProvider');
    }
    return context;
};
