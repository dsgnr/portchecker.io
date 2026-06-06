/* @format */
// @ts-check
const { defineConfig, devices } = require("@playwright/test");

/**
 * Playwright runs against the running smoke stack (web @ :8080, api @ :8000).
 * The compose stack is brought up by scripts/smoke.sh in CI before this is invoked.
 *
 * For local runs:
 *   docker compose -f docker-compose.smoke.yml up -d --build
 *   npm run --prefix frontend/web browser-tests
 */
module.exports = defineConfig({
    testDir: "./browser-tests",
    timeout: 30_000,
    expect: { timeout: 5_000 },
    fullyParallel: true,
    forbidOnly: !!process.env.CI,
    retries: process.env.CI ? 1 : 0,
    workers: process.env.CI ? 1 : undefined,
    reporter: process.env.CI ? [["github"], ["list"]] : "list",
    use: {
        baseURL: process.env.PLAYWRIGHT_BASE_URL || "http://127.0.0.1:8080",
        trace: "retain-on-failure",
        screenshot: "only-on-failure",
    },
    projects: [
        { name: "chromium", use: { ...devices["Desktop Chrome"] } },
    ],
});
