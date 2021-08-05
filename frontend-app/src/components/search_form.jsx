// import React from 'react';
// import ReactDOM from 'react-dom';
import React from 'react';
import { Input, Button, Label } from 'reactstrap';
import axios from 'axios';
import config from '../config/config.js'
import SearchResult from './search_result'
import Loader from 'react-loader'
import "react-loader-spinner/dist/loader/css/react-spinner-loader.css";


class SearchForm extends React.Component {
    constructor() {
        super();
        this.state = {
            data: [],
            loaded: true
        };
        this.sendQueryRequest = this.sendQueryRequest.bind(this)
    }

    sendQueryRequest() {
        let self = this;
        const form = document.getElementById("query_form");
        if (form) {
            let query = form.query.value
            if (query) {
                self.setState({ loaded: false });

                axios.post(config.SEARCH_REQUEST + query,
                    {
                        headers: {
                          'Sec-Fetch-Mode': 'cors',
                        }
                    }
                )
                    .then(function (json) {
                        // console.log('==>',json)
                        let response_data = json.data
                        self.setState({ data: response_data.comments, review: response_data.review, query_term: query, loaded: true });
                    })
                    .catch(function (error) {
                        alert('Search Failed !! Please try again with different Keyword');
                        self.setState({ loaded: true });
                    });

            } else {
                alert('Please enter a valid Search Keyword !')
                self.setState({ loaded: true });
            }

        }

    }
    render() {
        return (
            <div>
                <div>
                    <form id='query_form' >
                        <Label className="search_bar">Search Query: <Input name="query" type='text' placeholder="tesla" /></Label>
                        <Button onClick={this.sendQueryRequest}>  Send Request  </Button>

                    </form>

                </div>
                <Loader loaded={this.state.loaded} >
                    <SearchResult comments={this.state.data} review={this.state.review} query_term={this.state.query_term} />
                </Loader>

            </div>
        );

    }
}

export default SearchForm;