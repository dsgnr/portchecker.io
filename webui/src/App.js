import React from 'react';

import Routes from './routes';
import AppLayout from './layouts/AppLayout';
import ThemeProvider from './contexts/ThemeContext';
import './styles/index.scss';

function App() {
  return (
    <ThemeProvider>
      <AppLayout>
        <Routes />
      </AppLayout>
    </ThemeProvider>
  );
}

export default App;
