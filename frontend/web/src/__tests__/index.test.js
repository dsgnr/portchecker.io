/**
 * Tests for the real src/js/index.js module.
 * @format
 */

/* global axios */

function setupDOM() {
    document.body.innerHTML = `
        <form id="form">
            <div class="form-group">
                <input id="host" type="text" value="" />
            </div>
            <div class="form-group">
                <input id="ports" type="text" value="" />
                <button class="quick-port-btn" data-port="80"></button>
            </div>
            <button id="submit" type="submit"></button>
        </form>
        <div id="results" class="hidden">
            <span id="results-host"></span>
            <div id="results-list"></div>
        </div>
        <div id="error" class="hidden">
            <span id="error-text"></span>
        </div>
    `;
}

let app;

beforeEach(() => {
    setupDOM();
    jest.resetModules();
    // Require a fresh copy so the module's internal state is reset per test.
    app = require("../js/index.js");
});

describe("validateHostInput", () => {
    test("accepts a hostname", () => {
        document.getElementById("host").value = "example.com";
        expect(app.validateHostInput()).toBe(true);
    });

    test("accepts an IPv4 address", () => {
        document.getElementById("host").value = "1.1.1.1";
        expect(app.validateHostInput()).toBe(true);
    });

    test("accepts the 'me' keyword", () => {
        document.getElementById("host").value = "me";
        expect(app.validateHostInput()).toBe(true);
    });

    test("rejects an empty host and flags the field", () => {
        document.getElementById("host").value = "";
        expect(app.validateHostInput()).toBeFalsy();
        expect(document.querySelector(".form-group").classList.contains("has-error")).toBe(true);
    });

    test("rejects a host containing a space", () => {
        document.getElementById("host").value = "not a host";
        expect(app.validateHostInput()).toBe(false);
    });
});

describe("validatePortsInput", () => {
    test("accepts comma separated ports in range", () => {
        document.getElementById("ports").value = "80, 443, 8080";
        expect(app.validatePortsInput()).toBe(true);
    });

    test("rejects an empty value", () => {
        document.getElementById("ports").value = "";
        expect(app.validatePortsInput()).toBe(false);
    });

    test("rejects a port above 65535", () => {
        document.getElementById("ports").value = "70000";
        expect(app.validatePortsInput()).toBe(false);
    });

    test("rejects a non-numeric port", () => {
        document.getElementById("ports").value = "abc";
        expect(app.validatePortsInput()).toBe(false);
    });
});

describe("addPort", () => {
    test("appends a new port", () => {
        app.addPort("443");
        expect(document.getElementById("ports").value).toBe("443");
    });

    test("does not duplicate an existing port", () => {
        document.getElementById("ports").value = "80";
        app.addPort("80");
        expect(document.getElementById("ports").value).toBe("80");
    });
});

describe("queryHost", () => {
    test("renders results on success", async () => {
        document.getElementById("host").value = "example.com";
        document.getElementById("ports").value = "80, 443";

        axios.post.mockResolvedValue({
            data: {
                error: false,
                host: "example.com",
                check: [
                    { port: 80, status: true },
                    { port: 443, status: false },
                ],
            },
        });

        await app.queryHost();

        expect(axios.post).toHaveBeenCalledTimes(1);
        expect(document.getElementById("results").classList.contains("hidden")).toBe(false);
        expect(document.getElementById("results-host").textContent).toBe("example.com");
        expect(document.getElementById("results-list").children).toHaveLength(2);
    });

    test("shows joined messages from the API error extra field", async () => {
        document.getElementById("host").value = "example.com";
        document.getElementById("ports").value = "80";

        axios.post.mockRejectedValue({
            response: {
                data: {
                    extra: [{ message: "Invalid hostname" }, { message: "Port out of range" }],
                },
            },
        });

        await app.queryHost();

        expect(document.getElementById("error").classList.contains("hidden")).toBe(false);
        expect(document.getElementById("error-text").textContent).toBe("Invalid hostname, Port out of range");
    });

    test("falls back to a generic message for an unknown error", async () => {
        document.getElementById("host").value = "example.com";
        document.getElementById("ports").value = "80";

        axios.post.mockRejectedValue(new Error("network down"));

        await app.queryHost();

        expect(document.getElementById("error").classList.contains("hidden")).toBe(false);
        expect(document.getElementById("error-text").textContent).toBe("An unknown error occurred. Please try again.");
    });
});

describe("loadUserIp", () => {
    test("parses the cloudflare trace and populates the host field", async () => {
        axios.get.mockResolvedValue({
            data: "fl=123\nip=203.0.113.5\nts=1234567890\nvisit_scheme=https",
        });

        await app.loadUserIp();

        expect(document.getElementById("host").value).toBe("203.0.113.5");
    });

    test("does not throw when the trace request fails", async () => {
        axios.get.mockRejectedValue(new Error("network down"));
        await expect(app.loadUserIp()).resolves.toBeUndefined();
    });
});
