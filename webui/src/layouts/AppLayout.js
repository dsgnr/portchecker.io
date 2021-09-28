import React from 'react';
import { Global, css } from '@emotion/react';

import Header from './Header';
import Footer from './Footer';

import colorMap from '../styles/palette';
import { useThemeContext } from '../contexts/ThemeContext';

const globalStyle = (theme) => css`
  body {
    ${colorMap.base[theme]}
    transition-duration: 0.3s;
    transition-timing-function: ease;
    transition-property: border, background, color;
  }
`;

const AppLayout = ({ children }) => {
  const { theme } = useThemeContext();

  return (
    <>
      <Global styles={[globalStyle(theme)]} />
      <Header />
      <main>{children}</main>
      <Footer />
    </>
  );
};

export default AppLayout;
