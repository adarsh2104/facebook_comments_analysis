import React, { Component } from 'react';
import { Row, Col, Input, Button, Label, Table, NavLink } from 'reactstrap';
import axios from 'axios';
import config from '../config/config.js'



class Sugguestions extends React.Component {

    constructor() {
        super();
        this.state = {
            data: []
        };
    }
    componentDidMount() {
        let self = this;
        axios.get(config.SEARCH_SUGGEST)
            .then(function (json) {

                let response_data = json.data
                console.log('=SEARCH_SUGGEST=>', response_data.suggestions)
                self.setState({ data: response_data.suggestions });
            })
            .catch(function (error) {
                console.log(error)
            });
    }
    render() {
        return (<div>
            <h3>Search Suggestions: </h3>
            <ul>
                {this.state.data.map((row, index) => {
                    return (
                        <li key={index} className="suggestions" >
                            {row.keyword}</li>
                        )
                         }
                    )
                }
            </ul>
        </div>);
    }
}

export default Sugguestions;