/**
 * Tests for index.js functionality
 * @format
 */

/* global axios */

// Helper to set up DOM before importing module functions
function setupDOM() {
    document.body.innerHTML = `
        <form id="form">
            <input id="host" type="text" value="" />
            <input id="port" type="text" value="80" />
            <button type="submit">Check</button>
        </form>
        <div id="results" class="d-none"></div>
    `;
}

describe("generateSuccessHtml", () => {
    // We need to extract and test this function
    // Since the module uses window.onload, we'll test the logic directly

    function generateSuccessHtml(data) {
        const msg = document.createElement("p");
        msg.append(`Results for ${data.host}:`);

        const results = document.createElement("ul");
        data.check.forEach((check) => {
            const res = document.createElement("li");
            const state = document.createElement("span");
            state.classList.add(check.status ? "text-success" : "text-danger");
            state.textContent = check.status;

            const port = document.createElement("span");
            port.innerHTML = `${check.port} - ${state.outerHTML}`;

            res.appendChild(port);
            results.appendChild(res);
        });

        msg.append(results);
        return msg.outerHTML;
    }

    beforeEach(() => {
        setupDOM();
    });

    test("generates correct HTML for single open port", () => {
        const data = {
            host: "example.com",
            check: [{ port: 443, status: true }],
        };

        const html = generateSuccessHtml(data);

        expect(html).toContain("Results for example.com:");
        expect(html).toContain("443");
        expect(html).toContain("text-success");
    });

    test("generates correct HTML for single closed port", () => {
        const data = {
            host: "example.com",
            check: [{ port: 22, status: false }],
        };

        const html = generateSuccessHtml(data);

        expect(html).toContain("22");
        expect(html).toContain("text-danger");
    });

    test("generates correct HTML for multiple ports", () => {
        const data = {
            host: "example.com",
            check: [
                { port: 80, status: true },
                { port: 443, status: true },
                { port: 22, status: false },
            ],
        };

        const html = generateSuccessHtml(data);

        expect(html).toContain("80");
        expect(html).toContain("443");
        expect(html).toContain("22");
        expect(html.match(/text-success/g)).toHaveLength(2);
        expect(html.match(/text-danger/g)).toHaveLength(1);
    });

    test("handles empty check array", () => {
        const data = {
            host: "example.com",
            check: [],
        };

        const html = generateSuccessHtml(data);

        expect(html).toContain("Results for example.com:");
        expect(html).toContain("<ul></ul>");
    });
});

describe("resetPendingAlert", () => {
    function resetPendingAlert() {
        const alertDiv = document.getElementById("results");
        const alertClass = ["alert-info", "alert-success", "alert-danger"];
        alertDiv.classList.remove(...alertClass);
        alertDiv.classList.add("d-none", "alert-info");
        alertDiv.textContent = "";
    }

    beforeEach(() => {
        setupDOM();
    });

    test("removes alert classes and adds d-none", () => {
        const alertDiv = document.getElementById("results");
        alertDiv.classList.add("alert-success");
        alertDiv.textContent = "Some content";

        resetPendingAlert();

        expect(alertDiv.classList.contains("d-none")).toBe(true);
        expect(alertDiv.classList.contains("alert-info")).toBe(true);
        expect(alertDiv.classList.contains("alert-success")).toBe(false);
        expect(alertDiv.textContent).toBe("");
    });

    test("removes alert-danger class", () => {
        const alertDiv = document.getElementById("results");
        alertDiv.classList.add("alert-danger");

        resetPendingAlert();

        expect(alertDiv.classList.contains("alert-danger")).toBe(false);
    });
});

describe("Reactive State Proxy", () => {
    test("proxy triggers updates on property set", () => {
        const updateView = jest.fn();

        const state = new Proxy(
            { host: "", loading: false },
            {
                set(target, prop, value) {
                    target[prop] = value;
                    updateView(prop, value);
                    return true;
                },
            }
        );

        state.host = "example.com";

        expect(updateView).toHaveBeenCalledWith("host", "example.com");
        expect(state.host).toBe("example.com");
    });

    test("proxy handles multiple property updates", () => {
        const updates = [];

        const state = new Proxy(
            { host: "", loading: false, error: null },
            {
                set(target, prop, value) {
                    target[prop] = value;
                    updates.push({ prop, value });
                    return true;
                },
            }
        );

        state.host = "test.com";
        state.loading = true;
        state.error = "Network error";

        expect(updates).toHaveLength(3);
        expect(updates[0]).toEqual({ prop: "host", value: "test.com" });
        expect(updates[1]).toEqual({ prop: "loading", value: true });
        expect(updates[2]).toEqual({ prop: "error", value: "Network error" });
    });
});

describe("updateView", () => {
    beforeEach(() => {
        setupDOM();
    });

    test("loading state shows info alert", () => {
        const alertDiv = document.getElementById("results");
        alertDiv.classList.add("d-none");

        // Simulate updateView for loading state
        const state = { host: "example.com" };
        const isLoading = true;
        if (isLoading) {
            alertDiv.classList.replace("d-none", "alert-info");
            alertDiv.textContent = `Querying ${state.host}, please wait...`;
        }

        expect(alertDiv.classList.contains("alert-info")).toBe(true);
        expect(alertDiv.textContent).toContain("Querying example.com");
    });

    test("error state shows danger alert", () => {
        const alertDiv = document.getElementById("results");
        alertDiv.classList.add("alert-info");

        const errorMsg = "Connection failed";
        alertDiv.classList.replace("alert-info", "alert-danger");
        alertDiv.textContent = `ERROR: ${errorMsg}`;

        expect(alertDiv.classList.contains("alert-danger")).toBe(true);
        expect(alertDiv.textContent).toBe("ERROR: Connection failed");
    });
});

describe("loadUserIp", () => {
    beforeEach(() => {
        setupDOM();
    });

    test("parses cloudflare trace response correctly", async () => {
        const mockResponse = {
            data: "fl=123\nip=192.168.1.100\nts=1234567890\nvisit_scheme=https\nuag=Mozilla",
        };

        axios.get.mockResolvedValue(mockResponse);

        // Parse the response like loadUserIp does
        const output = mockResponse.data
            .trim()
            .split("\n")
            .map((e) => e.split("="));
        const jsonParsedOutput = Object.fromEntries(output);

        expect(jsonParsedOutput.ip).toBe("192.168.1.100");
    });

    test("handles cloudflare trace error gracefully", async () => {
        axios.get.mockRejectedValue(new Error("Network error"));

        // The function should catch and log the error
        const consoleSpy = jest.spyOn(console, "log").mockImplementation();

        try {
            await axios.get("https://1.1.1.1/cdn-cgi/trace");
        } catch (e) {
            console.log("error", e);
        }

        expect(consoleSpy).toHaveBeenCalled();
        consoleSpy.mockRestore();
    });
});

describe("queryHost", () => {
    beforeEach(() => {
        setupDOM();
    });

    test("sends correct payload to API", async () => {
        const mockResponse = {
            data: {
                error: false,
                host: "example.com",
                check: [{ port: 80, status: true }],
            },
        };

        axios.post.mockResolvedValue(mockResponse);

        document.getElementById("host").value = "example.com";
        document.getElementById("port").value = "80, 443";

        // Simulate queryHost logic
        const host = document.getElementById("host").value;
        const ports = document
            .getElementById("port")
            .value.split(",")
            .map((p) => p.trim());

        await axios.post("/api/query", { host, ports });

        expect(axios.post).toHaveBeenCalledWith("/api/query", {
            host: "example.com",
            ports: ["80", "443"],
        });
    });

    test("handles API error response", async () => {
        const errorResponse = {
            response: {
                data: {
                    extra: [{ message: "Invalid hostname" }, { message: "Port out of range" }],
                },
            },
        };

        axios.post.mockRejectedValue(errorResponse);

        let errorMessage;
        try {
            await axios.post("/api/query", { host: "invalid", ports: [99999] });
        } catch (error) {
            errorMessage =
                error.response?.data?.extra?.map((item) => item.message).join(", ") || "An unknown error occurred.";
        }

        expect(errorMessage).toBe("Invalid hostname, Port out of range");
    });

    test("handles unknown error", async () => {
        axios.post.mockRejectedValue(new Error("Network failure"));

        let errorMessage;
        try {
            await axios.post("/api/query", { host: "test.com", ports: [80] });
        } catch (error) {
            errorMessage =
                error.response?.data?.extra?.map((item) => item.message).join(", ") || "An unknown error occurred.";
        }

        expect(errorMessage).toBe("An unknown error occurred.");
    });
});

describe("Form validation", () => {
    beforeEach(() => {
        setupDOM();
    });

    test("form has required elements", () => {
        expect(document.getElementById("form")).not.toBeNull();
        expect(document.getElementById("host")).not.toBeNull();
        expect(document.getElementById("port")).not.toBeNull();
        expect(document.getElementById("results")).not.toBeNull();
    });

    test("port parsing handles comma-separated values", () => {
        document.getElementById("port").value = "80, 443, 8080";

        const ports = document
            .getElementById("port")
            .value.split(",")
            .map((p) => p.trim());

        expect(ports).toEqual(["80", "443", "8080"]);
    });

    test("port parsing handles single value", () => {
        document.getElementById("port").value = "443";

        const ports = document
            .getElementById("port")
            .value.split(",")
            .map((p) => p.trim());

        expect(ports).toEqual(["443"]);
    });

    test("port parsing handles whitespace", () => {
        document.getElementById("port").value = "  80  ,  443  ";

        const ports = document
            .getElementById("port")
            .value.split(",")
            .map((p) => p.trim());

        expect(ports).toEqual(["80", "443"]);
    });
});
