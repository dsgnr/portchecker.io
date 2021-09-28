import React, { useState,useEffect,Component } from 'react';
import { css } from '@emotion/react';
import axios from 'axios';
const api_url = "/api";
const HomePageStyle = css`
* {
  font-size: 14px;
}
p {
  font-size:14px;
}
.container {
  max-width: 960px;
  margin: 150px auto;
}
.description {
  text-align: center;
}
.input {
  box-shadow: inset 0 0.0625em 0.125em rgb(10 10 10 / 5%);
  background-color: #fff;
  border-color: #dbdbdb;
  color: #363636;
  border: 1px solid transparent;
  border-radius: .375em;
  box-shadow: none;
  padding: 15px;
}
.form-group, .form-group input {
    min-width: 100%;
}
.host-group {
    width: calc(60% - 30px);
    display: table;
    margin-right: 20px;
    float: left;
}
.ports-group {
    width: calc(25% - 30px);
    display: table;
    margin-right: 20px;
    float: left;
}
.button {
  width: calc(20% - 30px);
  float:left;
  padding: 15px;
  background-color: #fff;
  border-color: #dbdbdb;
  border-width: 1px;
  color: #363636;
  cursor: pointer;
  justify-content: center;
  text-align: center;
  white-space: nowrap;
  border-radius: .375em;
}

.button.is-success {
  background-color: #48c78e;
  border-color: transparent;
  color: #fff;
}
.form {
  margin-top:50px;
}
.box {
    clear: both;
    padding: 21px 20px;
    margin-top: 50px;
    display: inline-block;
    position: relative;
    width: 100%;
    border-radius: .375em;
}
.results {
    border: 1px solid #888;
}
.error_message{
    border: 1px solid #dc3545;
    background-color: #dc3545;
    opacity: 0.9;
    color: #ececec;
}
.form-error {
    padding: 10px;
    clear: both;
    display: table;
    color: #dc3545;
}
`;

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
        this.ipChange = this.ipChange.bind(this);
        this.submit = this.submit.bind(this);
    }

    componentDidMount() {
      axios.get('https://geolocation-db.com/json/')
        .then((res) => {
            this.setState({host: res.data.IPv4});
        });
    }

    ipChange(event) {
        this.setState(
            {
                error: false,
                hostError: "",
                host: event.target.value,
                results: [],
                msg: "",
                showResults: false
            }
        );
    }

    portChange(event) {
        this.setState(
            {
                error: false,
                portError: "",
                ports: event.target.value,
                results: [],
                msg: "",
                showResults: false
            }
        );
    }

    formErrors() {
        if (!this.state.host) {
            this.setState({hostError: "Host cannot be empty"});
            return true;
        }
        if (!this.state.ports) {
            this.setState({portError: "Port cannot be empty"});
            return true;
        }
        return false;
    }

    poll_delay(ms) {
        return new Promise(resolve => {
            setTimeout(resolve, ms);
        });
    }

    poll_task(task_id) {
        return axios.get(`${api_url}/results/${task_id}`)
        .then(response => {
            if(response.data.results === null || response.data.results.length === 0){
                return this.poll_delay(1000) .then(() => this.poll_task(task_id));
            } else {
                this.setState({showResults: true, results: response.data.results});
                this.setState({msg: "Completed"});
            }
        })
        .catch((error) => {
            console.log(this.state);
            if (error.response) {
                // Request made and server responded
                this.setState({error: true, msg: error.response.data.msg});
            } else if (error.request) {
                // The request was made but no response was received
                this.setState(
                    {
                        error: true,
                        msg: "Something bad happened and we couldn't process the request"
                    }
                );
            } else {
                // Something happened in setting up the request that triggered an Error
                this.setState({error: true, msg: error.message});
            }
        });
    }

    submit() {
        if (this.formErrors()) {
          return false;
        }
        this.setState({results: [], showResults: false});
        axios.post(api_url, {"host": this.state.host, ports: Array.of(parseInt(this.state.ports))})
        .then((res) => {
          this.setState({error: false, msg: res.data.msg, showResults: true, results: []});
          this.poll_task(res.data.task_id);
        })
        .catch((error) => {
            console.log(this.state);
            if (error.response) {
                // Request made and server responded
                this.setState({error: true, msg: error.response.data.msg});
            } else if (error.request) {
                // The request was made but no response was received
                this.setState(
                    {
                        error: true,
                        msg: "Something bad happened and we couldn't process the request"
                    }
                );
            } else {
                // Something happened in setting up the request that triggered an Error
                this.setState({error: true, msg: error.message});
            }
        });
    }

    render() {
        return (
            <div css={[HomePageStyle]}>
              <div className="container">
                <p className="description">
                    portchecker.io is a free utility to check the port status of a given hostname of IP address.
                </p>
                  <div className="form">
                    <div className="input-group host-group">
                        <div className="form-group">
                            <input className="input" type="text" placeholder="Hostame or IP address" defaultValue={this.state.host} onChange={this.ipChange} required/>
                        </div>
                        { this.state.hostError ? <span className="form-error">{this.state.hostError}</span> : null }
                    </div>
                    <div className="input-group ports-group">
                        <div className="form-group">
                            <input className="input" type="number" placeholder="Port" value={this.state.value} onChange={this.portChange} required/>
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
