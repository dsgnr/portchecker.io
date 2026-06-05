/** @type {import('jest').Config} */
module.exports = {
    testEnvironment: "jsdom",
    roots: ["<rootDir>/src"],
    testMatch: ["**/__tests__/**/*.test.js", "**/*.test.js"],
    testPathIgnorePatterns: ["/node_modules/", "setup.js", "/browser-tests/"],
    moduleFileExtensions: ["js"],
    setupFilesAfterEnv: ["<rootDir>/src/__tests__/setup.js"],
    verbose: true,
    collectCoverageFrom: ["src/js/**/*.js", "!src/js/**/*.min.js"],
};
