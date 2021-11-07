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
            error: false,
            hostError: "",
            portError: "",
            showResults: false,
            host: "",
            ports: "",
            results: [],
            task_id: "",
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
            console.log('error', e)
        })
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
        this.setState({results: [], showResults: false});
        axios.post(api_url, {"host": this.state.host, ports: Array.of(parseInt(this.state.ports))}, {
        headers: {
    'content-type': 'application/json'
  }
        })
        .then((res) => {
            this.setState({error: false, msg: res.data.msg, showResults: true, results: []});
            this.setState(
                {msg: "Completed", showResults: true, results: res.data.results}
            );
        })
        .catch((error) => {
            if (error.response.status === 400) {
                this.setState({error: true, msg: error.response.data.msg});
            } else {
                this.setState({error: true, msg: apierr_msg});
            }
        });
    }

    render() {
        return (
            <div className="home">
              <div className="container">
                <p className="description">
                    portchecker.io is a free utility to check the port status of a given hostname of IP address.
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
                            <input className="input" type="number" placeholder="Port" value={this.state.value} onChange={this.portChange} onKeyUp={this.portChange}/>
                        </div>
                        { this.state.portError ? <span className="form-error">{this.state.portError}</span> : null }
                    </div>
                    <button className="button is-success" onClick={this.submit}>Check</button>
                  </div>

                { this.state.error ?
                    <div className="box error_message">
                    <p>Error: {this.state.msg}</p>
                    </div>
                    : null
                }
                { this.state.showResults ? <div className="box results">
                    {this.state.msg !== "Completed" ? this.state.msg : <p>Results for {this.state.host}:</p>}
                    {this.state.results && this.state.results.check
                    && Object.keys(this.state.results.check).map((key, i) =>
                        <li key={key}>{this.state.results.check[key].port} - {String(this.state.results.check[key].status)}</li>
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
