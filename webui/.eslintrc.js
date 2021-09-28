module.exports = {
  env: {
    node: true,
    browser: true,
  },
  parser: 'babel-eslint',
  globals: {
    Atomics: 'readonly',
    SharedArrayBuffer: 'readonly',
  },
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 2018,
    sourceType: 'module',
  },
  plugins: ['react', 'prettier'],
  rules: {
    'no-console': 1,
    'no-unused-vars': 0,
    'react/prop-types': 0,
    'react/display-name': 0,
  },
  extends: ['prettier', 'eslint:recommended', 'plugin:react/recommended'],
};
