import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { css } from '@emotion/react';

import { ReactComponent as LogoIcon } from '../assets/zap.svg';
import { ReactComponent as SunIcon } from '../assets/sun.svg';
import { ReactComponent as MoonIcon } from '../assets/moon.svg';
import media from '../styles/media';
import { palette } from '../styles/palette';
import { useThemeContext } from '../contexts/ThemeContext';

const headerStyle = (isLight) => css`
  ${media.medium} {
    height: 50px;
  }

  & > nav {
    svg {
      color: ${isLight ? 'inherit' : palette.yellow[4]};
      fill: ${isLight ? palette.yellow[6] : palette.yellow[4]};
    }
  }
`;

const Header = () => {
  const { pathname } = useLocation();
  const { isLight, toggleTheme } = useThemeContext();

  return (
    <header css={[headerStyle(isLight)]}>
      <nav>
        <div className="logo">
          <Link to="/" replace={pathname === '/'}>
            portchecker.io
          </Link>
        </div>
        <div>
          {isLight ? (
            <SunIcon className="theme" onClick={toggleTheme} />
          ) : (
            <MoonIcon className="theme" onClick={toggleTheme} />
          )}
        </div>
      </nav>
    </header>
  );
};

export default Header;
