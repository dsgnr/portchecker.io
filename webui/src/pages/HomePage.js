import React, { useState,useEffect,Component } from 'react';
import { css } from '@emotion/react';
import axios from 'axios';
const api_url = "https://api.portchecker.io/v1";
const hosterr_msg = "Host cannot be empty";
const porterr_msg = "Port cannot be empty";
const apierr_msg = "Something bad happened and we couldn't process the request.";

export class HomePage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            pending: false,
            error: false,
            hostError: "",
            portError: "",
            showResults: false,
            host: "",
            ports: parseInt(process.env.DEFAULT_PORT) || "",
            results: [],
            msg: ""
        };
        this.portChange = this.portChange.bind(this);
        this.hostChange = this.hostChange.bind(this);
        this.submit = this.submit.bind(this);
    }

    componentDidMount() {
        // Attempts to obtain the users public IP address from
        // Cloudflares DNS to be helpful and prepopulate the form
        axios.get('https://1.1.1.1/cdn-cgi/trace').then((response) => {
            let output = response.data.trim().split('\n').map(e=>e.split('='));
            let json_parsed_output = Object.fromEntries(output);
            this.setState({host: json_parsed_output.ip});
        })
        .catch((e) => {
            console.log('error', e);
        });
    }

    hostChange(event) {
        this.setState(
            {
                error: false,
                hostError: !event.target.value.length ? hosterr_msg : "",
                host: event.target.value,
                results: [],
                msg: "",
                showResults: false
            }
        );
        if (event.code === "Enter" || event.code === "NumpadEnter") {
            this.submit();
        }
    }

    portChange(event) {
        this.setState(
            {
                error: false,
                portError: !event.target.value.length ? porterr_msg : "",
                ports: event.target.value,
                results: [],
                msg: "",
                showResults: false
            }
        );
        if (event.code === "Enter" || event.code === "NumpadEnter") {
            this.submit();
        }
    }

    formErrors() {
        let hosterr, porterr;
        if (!this.state.host) {
            porterr = true;
            this.setState({hostError: hosterr_msg});
        }
        if (!this.state.ports) {
            hosterr = true;
            this.setState({portError: porterr_msg});
        }
        if (porterr || hosterr) {
            return true;
        }
        return false;
    }

    submit() {
        if (this.formErrors()) {
            return false;
        }
        this.setState(
            {
                results: [],
                pending: true,
                showResults: false,
                msg: `Querying host ${this.state.host}...`
            }
        );
        axios.post(
            api_url,
            {"host": this.state.host, ports: Array.of(parseInt(this.state.ports))},
            {headers: {'content-type': 'application/json'}}
        )
        .then((res) => {
            this.setState(
                {
                    msg: res.data.msg,
                    error: res.data.error,
                    pending: false,
                    showResults: !res.data.error,
                    results: res.data.check
                }
            );
        })
        .catch((error) => {
            if (error.response.status === 400) {
                this.setState({error: true, pending: false, msg: error.response.data.msg});
            } else {
                this.setState({error: true, pending: false, msg: apierr_msg});
            }
        });
    }

    render() {
        return (
            <div className="home">
              <div className="container">
                <p className="description">
                    portchecker.io is a free utility to check the port status of a given hostname or IP address.
                </p>
                  <div className="form">
                    <div className="input-group host-group">
                        <div className="form-group">
                            <input className="input" type="text" placeholder="Hostame or IP address" defaultValue={this.state.host} onChange={this.hostChange} onKeyUp={this.hostChange}/>
                        </div>
                        { this.state.hostError ? <span className="form-error">{this.state.hostError}</span> : null }
                    </div>
                    <div className="input-group ports-group">
                        <div className="form-group">
                            <input className="input" type="number" placeholder="Port" value={this.state.ports} onChange={this.portChange} onKeyUp={this.portChange}/>
                        </div>
                        { this.state.portError ? <span className="form-error">{this.state.portError}</span> : null }
                    </div>
                    <button className="button is-success" onClick={this.submit}>Check</button>
                  </div>

                { this.state.pending ?
                    <div className="box results pending-box">
                    <p>{this.state.msg}</p>
                    </div>
                    : null
                }
                { this.state.error ?
                    <div className="box error-box">
                    <p>Error: {this.state.msg}</p>
                    </div>
                    : null
                }
                { this.state.showResults ?
                    <div className="box results success-box">
                    {this.state.msg !== null ? this.state.msg : <p>Results for {this.state.host}:</p>}
                    {this.state.results && this.state.results
                    && Object.keys(this.state.results).map((key, i) =>
                        <li key={key}>{this.state.results[key].port} - <span className={
                            `${this.state.results[key].status ? "is-true" : "is-false"}`
                        }>
                            {String(this.state.results[key].status)}</span>
                        </li>
                    )}
                    </div>
                    : null
                }
              </div>
            </div>
        )
    };
};

export default HomePage;
