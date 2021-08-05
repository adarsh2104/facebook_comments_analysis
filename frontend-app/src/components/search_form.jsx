// import React from 'react';
// import ReactDOM from 'react-dom';
import React, { Component } from 'react';
import {Row,Col,Input,Button,Label,Table,NavLink } from 'reactstrap';
import axios from 'axios';
import config from '../config/config.js'
import SearchResult from './search_result'

class SearchForm extends React.Component {
    constructor() {
        super();
        this.state = {
            data :[]
        };
        this.sendQueryRequest = this.sendQueryRequest.bind(this)
    }

    sendQueryRequest(){
        let self = this;
        const form = document.getElementById("query_form");
        if (form){
            let query = form.query.value
            if (query){
            axios.post(config.SEARCH_REQUEST + query)
            .then(function (json) {
                console.log('==>',json)
                let response_data = json.data
                self.setState({data:response_data.comments,review:response_data.review});
            })
            .catch(function (error) {
                console.log(error)
            });

            } else{
                alert('Please enter a valid Search Keyword !')
            }
            
        }

        
    }
    render() {
      return (
          <div>
              <div>
              <form id='query_form'>
              <Label className="search_bar">Search Query: <Input name="query" type='text'/></Label>
              <Button onClick={this.sendQueryRequest}>  Send Request  </Button>
              </form>
              </div>
              <SearchResult comments={this.state.data} review={this.state.review}/>
          </div>
      );
    }
  }
  
  export default SearchForm;