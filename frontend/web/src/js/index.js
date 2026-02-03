/* @format */
/* jshint esversion: 10, globalstrict: true */
/* global axios */
"use strict";

window.onload = () => {
    initializeState();
    setupEventListeners();

    if (!document.getElementById("host").value) {
        loadUserIp();
    }
};

// Reactive state
const state = new Proxy(
    {
        host: "",
        ports: [],
        results: null,
        loading: false,
        error: null,
    },
    {
        set(target, prop, value) {
            target[prop] = value;
            updateView(prop, value);
            return true;
        },
    }
);

function initializeState() {
    state.host = "";
    state.ports = [];
    state.results = null;
    state.loading = false;
    state.error = null;
}

function setupEventListeners() {
    const form = document.getElementById("form");
    const portsInput = document.getElementById("ports");

    // Form submission
    form.addEventListener("submit", handleSubmit);

    // Quick port buttons
    document.querySelectorAll(".quick-port-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
            const port = btn.dataset.port;
            addPort(port);
            btn.classList.add("active");
            setTimeout(() => btn.classList.remove("active"), 200);
        });
    });

    // Validate ports on input
    portsInput.addEventListener("input", () => {
        validatePortsInput();
    });

    // Validate host on input
    document.getElementById("host").addEventListener("input", () => {
        validateHostInput();
    });
}

function handleSubmit(event) {
    event.preventDefault();
    event.stopPropagation();

    const hostValid = validateHostInput();
    const portsValid = validatePortsInput();

    if (!hostValid || !portsValid) {
        return;
    }

    hideError();
    hideResults();
    queryHost();
}

function validateHostInput() {
    const hostInput = document.getElementById("host");
    const hostGroup = hostInput.closest(".form-group");
    const value = hostInput.value.trim();

    // Allow hostname, IPv4, or "me"
    const hostPattern = /^([\w-]+(\.[\w-]+)*|me|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$/;
    const isValid = value && hostPattern.test(value);

    hostGroup.classList.toggle("has-error", !isValid);
    return isValid;
}

function validatePortsInput() {
    const portsInput = document.getElementById("ports");
    const portsGroup = portsInput.closest(".form-group");
    const value = portsInput.value.trim();

    if (!value) {
        portsGroup.classList.add("has-error");
        return false;
    }

    const ports = value.split(",").map((p) => p.trim()).filter(Boolean);
    const isValid = ports.every((p) => {
        const num = parseInt(p, 10);
        return !isNaN(num) && num >= 1 && num <= 65535;
    });

    portsGroup.classList.toggle("has-error", !isValid || ports.length === 0);
    return isValid && ports.length > 0;
}

function addPort(port) {
    const portsInput = document.getElementById("ports");
    const currentPorts = portsInput.value
        .split(",")
        .map((p) => p.trim())
        .filter(Boolean);

    if (!currentPorts.includes(port)) {
        currentPorts.push(port);
        portsInput.value = currentPorts.join(", ");
    }

    validatePortsInput();
}

function loadUserIp() {
    axios
        .get("https://1.1.1.1/cdn-cgi/trace")
        .then((response) => {
            const output = response.data
                .trim()
                .split("\n")
                .map((e) => e.split("="));
            const jsonParsedOutput = Object.fromEntries(output);
            state.host = jsonParsedOutput.ip;
            document.getElementById("host").value = state.host;
        })
        .catch((e) => {
            console.log("Failed to detect IP:", e);
        });
}

function queryHost() {
    const form = document.getElementById("form");
    const host = form.querySelector("#host").value.trim();
    const ports = form
        .querySelector("#ports")
        .value.split(",")
        .map((p) => p.trim())
        .filter(Boolean);

    state.host = host;
    state.loading = true;
    state.error = null;

    axios
        .post("/api/query", { host: host, ports: ports })
        .then((response) => {
            state.results = response.data;
            state.loading = false;
        })
        .catch((error) => {
            state.error =
                error.response?.data?.extra?.map((item) => item.message).join(", ") ||
                error.response?.data?.message ||
                "An unknown error occurred. Please try again.";
            state.loading = false;
        });
}

function updateView(prop, value) {
    const submitBtn = document.getElementById("submit");
    const resultsDiv = document.getElementById("results");
    const errorDiv = document.getElementById("error");

    switch (prop) {
        case "loading":
            submitBtn.classList.toggle("loading", value);
            submitBtn.disabled = value;
            break;

        case "results":
            if (value && !state.error) {
                showResults(value);
            }
            break;

        case "error":
            if (value) {
                showError(value);
            }
            break;
    }
}

function showResults(data) {
    const resultsDiv = document.getElementById("results");
    const resultsHost = document.getElementById("results-host");
    const resultsList = document.getElementById("results-list");

    resultsHost.textContent = data.host;
    resultsList.innerHTML = "";

    data.check.forEach((check) => {
        const item = document.createElement("div");
        item.className = "result-item";

        const isOpen = check.status === true || check.status === "True";
        const statusClass = isOpen ? "open" : "closed";
        const statusText = isOpen ? "Open" : "Closed";

        item.innerHTML = `
            <span class="result-port">Port ${check.port}</span>
            <span class="result-status ${statusClass}">
                <span class="status-dot"></span>
                ${statusText}
            </span>
        `;

        resultsList.appendChild(item);
    });

    resultsDiv.classList.remove("hidden");
}

function hideResults() {
    document.getElementById("results").classList.add("hidden");
}

function showError(message) {
    const errorDiv = document.getElementById("error");
    const errorText = document.getElementById("error-text");

    errorText.textContent = message;
    errorDiv.classList.remove("hidden");
}

function hideError() {
    document.getElementById("error").classList.add("hidden");
}
