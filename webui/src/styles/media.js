export const mediaQuery = (maxWidth) => `
  @media (max-width: ${maxWidth}px)
`;

export default {
  xxlarge: mediaQuery(1920),
  xlarge: mediaQuery(1440),
  large: mediaQuery(1200),
  medium: mediaQuery(1024),
  small: mediaQuery(768),
  xsmall: mediaQuery(375),
  custom: mediaQuery,
};
