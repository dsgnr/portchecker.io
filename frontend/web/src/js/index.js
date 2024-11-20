/* @format */
/* jshint esversion: 10, globalstrict: true */
/* global axios */
"use strict";

window.onload = () => {
    initializeState();
    loadUserIp();

    const form = document.getElementById("form");
    form.addEventListener("submit", (event) => {
        event.preventDefault();
        event.stopPropagation();

        if (!form.checkValidity()) {
            form.classList.add("was-validated");
            return;
        }

        form.classList.remove("was-validated");
        resetPendingAlert();
        queryHost();
    });
};

// Reactive state object
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
            updateView(prop, value); // Trigger view updates
            return true;
        },
    }
);

function initializeState() {
    // Initialize the default state
    state.host = "";
    state.ports = [];
    state.results = null;
    state.loading = false;
    state.error = null;
}

// Update view based on state changes
function updateView(prop, value) {
    const alertDiv = document.getElementById("results");
    switch (prop) {
        case "loading":
            if (value) {
                alertDiv.classList.replace("d-none", "alert-info");
                alertDiv.textContent = `Querying ${state.host}, please wait...`;
            }
            break;

        case "results":
            if (value) {
                const success = !state.error;
                alertDiv.classList.replace("alert-info", success ? "alert-success" : "alert-danger");
                alertDiv.innerHTML = success ? generateSuccessHtml(value) : `ERROR: ${state.error}`;
            }
            break;

        case "error":
            if (value) {
                alertDiv.classList.replace("alert-info", "alert-danger");
                alertDiv.textContent = `ERROR: ${value}`;
            }
            break;

        default:
            break;
    }
}

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

function resetPendingAlert() {
    const alertDiv = document.getElementById("results");
    const alertClass = ["alert-info", "alert-success", "alert-danger"];
    alertDiv.classList.remove(...alertClass);
    alertDiv.classList.add("d-none", "alert-info");
    alertDiv.textContent = "";
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
            state.host = jsonParsedOutput.ip; // Update reactive state
            document.getElementById("host").value = state.host;
        })
        .catch((e) => {
            console.log("error", e);
        });
}

function queryHost() {
    const form = document.getElementById("form");
    const host = form.querySelector("#host").value;
    const ports = form
        .querySelector("#port")
        .value.split(",")
        .map((p) => p.trim());

    state.loading = true; // Trigger "loading" state
    state.error = null;

    axios
        .post("/api/query", { host: host, ports: ports })
        .then((response) => {
            state.results = response.data; // Update reactive state with results
            state.loading = false;
        })
        .catch((error) => {
            state.error =
                error.response?.data?.extra?.map((item) => item.message).join(", ") || "An unknown error occurred.";
            state.loading = false;
        });
}
