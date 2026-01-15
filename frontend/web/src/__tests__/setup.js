/**
 * Jest setup file - runs before each test file
 */

// Mock axios globally
global.axios = {
    get: jest.fn(),
    post: jest.fn(),
};

// Reset mocks between tests
beforeEach(() => {
    jest.clearAllMocks();
    document.body.innerHTML = "";
});
