/* @format */
// @ts-check
const { test, expect } = require("@playwright/test");

/**
 * Browser-driven check against the running smoke stack.
 *
 * The smoke compose file pins ALLOW_PRIVATE=true and runs a "port-target"
 * netcat sidecar listening on 9999, so this submits a real query through the
 * nginx proxy and asserts the rendered results panel.
 */

test.describe("port checker UI", () => {
    test.beforeEach(async ({ page }) => {
        // The page makes a best-effort GET to https://1.1.1.1/cdn-cgi/trace
        // to populate the host input. Block it so the test is deterministic
        // and offline-safe.
        await page.route("**/cdn-cgi/trace", (route) => route.abort());
    });

    test("renders the form", async ({ page }) => {
        await page.goto("/");
        await expect(page).toHaveTitle(/portchecker/i);
        await expect(page.locator("#form")).toBeVisible();
        await expect(page.locator("#host")).toBeVisible();
        await expect(page.locator("#ports")).toBeVisible();
    });

    test("submits a query against the port-target sidecar and shows results", async ({ page }) => {
        await page.goto("/");

        await page.locator("#host").fill("port-target");
        await page.locator("#ports").fill("9999, 9998");

        await page.locator("#submit").click();

        const results = page.locator("#results");
        await expect(results).toBeVisible({ timeout: 10_000 });
        await expect(page.locator("#results-host")).toHaveText("port-target");

        // Both ports rendered.
        const items = page.locator("#results-list .result-item");
        await expect(items).toHaveCount(2);

        // 9999 open, 9998 closed.
        await expect(page.locator("#results-list").getByText("Port 9999")).toBeVisible();
        await expect(page.locator("#results-list").getByText("Port 9998")).toBeVisible();
        await expect(page.locator("#results-list .result-status.open")).toHaveCount(1);
        await expect(page.locator("#results-list .result-status.closed")).toHaveCount(1);
    });

    test("surfaces a validation error for an out-of-range port", async ({ page }) => {
        await page.goto("/");

        await page.locator("#host").fill("port-target");
        await page.locator("#ports").fill("70000");
        await page.locator("#submit").click();

        // Client-side validation marks the field as invalid before submit fires.
        await expect(page.locator("#ports").locator("xpath=ancestor::*[contains(@class,'form-group')]"))
            .toHaveClass(/has-error/);
    });
});
