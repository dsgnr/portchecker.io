import React from 'react';
import { css } from '@emotion/react';
import { ReactComponent as GithubIcon } from '../assets/github.svg';

const footerStyle = css`
  padding: 40px 16px;
  & > nav {
    margin: 0 auto;
    max-width: 1440px;
    display: flex;
    align-items: center;
    justify-content: space-between;

    svg {
      width: 2rem;
      height: 2rem;
    }
  }
`;

const Footer = () => {
  return (
    <footer css={[footerStyle]}>
      <nav>
        <div>{new Date().getFullYear()} &copy; Dan Hand (@dsgnr)</div>
        <div>
          <a
            href="https://github.com/dsgnr/portchecker.io"
            rel="noopener noreferrer"
            target="_blank"
          >
            <GithubIcon className="github" />
          </a>
        </div>
      </nav>
    </footer>
  );
};

export default Footer;
