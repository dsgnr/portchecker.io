import React, { createContext, useContext, useState, useCallback, useMemo } from 'react';

const ThemeContext = createContext();

export const useThemeContext = () => useContext(ThemeContext);

export default ({ children }) => {
  const isThemed = localStorage.getItem('theme') || 'light';
  const [theme, setTheme] = useState(isThemed);
  const isLight = useMemo(() => theme === 'light', [theme]);
  const toggleTheme = useCallback(() => {
    setTheme(prev => (prev === 'light' ? 'dark' : 'light'));
  }, []);
  localStorage.setItem("theme", theme);

  return (
    <ThemeContext.Provider value={{ theme, isLight, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};
