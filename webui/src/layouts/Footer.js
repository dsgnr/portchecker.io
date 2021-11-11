import React from 'react';
import { css } from '@emotion/react';
import { ReactComponent as GithubIcon } from '../assets/github.svg';

const Footer = () => {
  return (
    <footer id="footer">
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
