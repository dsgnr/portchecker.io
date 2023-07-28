/* @format */
/* jshint esversion: 10, globalstrict: true */
/* global axios */
"use strict";

window.addEventListener("load", () => {
    load_user_ip();
    const form = document.getElementById("form");
    form.addEventListener("submit", (event) => {
        event.preventDefault();
        event.stopPropagation();
        if (!form.checkValidity()) {
            form.classList.add("was-validated");
            return;
        }
        form.classList.remove("was-validated");
        reset_pending_alert();
        query_host();
    });
});

function pending_results(host) {
    const alert_div = document.getElementById("results");
    alert_div.classList.remove("d-none");
    alert_div.textContent = `Querying ${host}, please wait...`;
}

function reset_pending_alert() {
    const alert_div = document.getElementById("results");
    alert_div.classList.add("d-none", "alert-info");
    alert_div.classList.remove("alert-success", "alert-danger");
    alert_div.replaceChildren();
}

function query_results(data) {
    const alert_div = document.getElementById("results");
    alert_div.classList.remove("d-none");
    const success = data.error === false;
    alert_div.classList.replace("alert-info", success ? "alert-success" : "alert-danger");
    var msg = document.createElement("p");
    if (success) {
        msg.append(`Results for ${data.host}:`);
        var results = document.createElement("ul");
        data.check.forEach(function (check) {
            let res = document.createElement("li");
            let state = document.createElement("span");
            state.classList.add(check.status ? "text-success" : "text-danger");
            state.textContent = check.status;
            let port = document.createElement("span");
            port.innerHTML = `${check.port} - ${state.outerHTML}`;
            res.appendChild(port);
            results.appendChild(res);
        });
        msg.append(results);
    } else {
        msg.append(`ERROR: ${data.msg}`);
    }
    alert_div.innerHTML = msg.outerHTML;
}

function load_user_ip() {
    // Attempts to obtain the users public IP address from
    // Cloudflares DNS to be helpful and prepopulate the form
    axios
        .get("https://1.1.1.1/cdn-cgi/trace")
        .then((response) => {
            let output = response.data
                .trim()
                .split("\n")
                .map((e) => e.split("="));
            let json_parsed_output = Object.fromEntries(output);
            document.getElementById("host").value = json_parsed_output.ip;
        })
        .catch((e) => {
            console.log("error", e);
        });
}

function query_host() {
    const form = document.getElementById("form");
    const host = form.querySelector("#host").value;
    const ports = Array(form.querySelector("#port").value);
    pending_results(host);
    axios
        .post(
            "/api/v1/query",
            { host: host, ports: ports }
        )
        .then((response) => {
            query_results(response.data);
        })
        .catch((error) => {
            query_results(error.response.data);
        });
}
