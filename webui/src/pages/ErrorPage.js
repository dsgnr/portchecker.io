import React from 'react';
import { Link } from 'react-router-dom';
import { css } from '@emotion/react';
import { default as TakenSVG } from '../assets/undraw_Taken.svg';
import { palette } from '../styles/palette';
import { useThemeContext } from '../contexts/ThemeContext';
import media from '../styles/media';

const ErrorPageStyle = (isLight) => css`
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  h1 {
    color: red;
    font-size: 3rem;
    font-weight: 600;
    color: ${isLight ? palette.red[6] : palette.red[5]};
  }
  img {
    margin: 1rem auto;
    max-width: 35%;
  }
  a {
    color: ${isLight ? palette.blue[6] : palette.blue[4]};
  }

  ${media.medium} {
    img {
      margin: 2rem auto;
      max-width: 70%;
    }
  }
  ${media.small} {
    h1 {
      font-size: 2.5rem;
    }
    img {
      margin: 2rem auto;
      max-width: 80%;
    }
  }
`;

const ErrorPage = () => {
  const { isLight } = useThemeContext();

  return (
    <div css={[ErrorPageStyle(isLight)]}>
      <h1>Page Not Found.</h1>
      <img src={TakenSVG} alt="" />
      <Link to="/">go Home</Link>
    </div>
  );
};

export default ErrorPage;
