/** @type {import('jest').Config} */
module.exports = {
    testEnvironment: "jsdom",
    roots: ["<rootDir>/src"],
    testMatch: ["**/__tests__/**/*.test.js", "**/*.test.js"],
    testPathIgnorePatterns: ["/node_modules/", "setup.js"],
    moduleFileExtensions: ["js"],
    setupFilesAfterEnv: ["<rootDir>/src/__tests__/setup.js"],
    verbose: true,
};
