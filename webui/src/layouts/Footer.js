import React from 'react';
import { css } from '@emotion/react';
import { ReactComponent as GithubIcon } from '../assets/github.svg';

const Footer = () => {
  return (
    <footer id="footer">
      <nav>
        <div>
            {new Date().getFullYear()} &copy; <a href="https://danielhand.io" target="_blank">Dan Hand (@dsgnr)</a>
        </div>
        <div>
          <a
            href="https://www.digitalocean.com/?refcode=b54817e033c8&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge"
          >
            <img
                height="36"
                src="https://web-platforms.sfo2.digitaloceanspaces.com/WWW/Badge%203.svg"
                alt="DigitalOcean Referral Badge"
            />
          </a>
          <a
            href='https://ko-fi.com/U7U3FUX17'
            target='_blank'
        >
            <img
                height='36'
                src='https://cdn.ko-fi.com/cdn/kofi3.png?v=3'
                border='0'
                alt='Buy Me a Coffee at ko-fi.com' />
          </a>
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
