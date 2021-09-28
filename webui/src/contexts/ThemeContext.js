import React, { createContext, useContext, useState, useCallback, useMemo } from 'react';

const ThemeContext = createContext();

export const useThemeContext = () => useContext(ThemeContext);

export default ({ children }) => {
  const [theme, setTheme] = useState('light');

  const isLight = useMemo(() => theme === 'light', [theme]);

  const toggleTheme = useCallback(() => {
    setTheme(prev => (prev === 'light' ? 'dark' : 'light'));
  }, []);

  return (
    <ThemeContext.Provider value={{ theme, isLight, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};
