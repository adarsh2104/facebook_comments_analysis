import React, { Component } from 'react';
import {Row,Col,Input,Button,Label,Table,NavLink } from 'reactstrap';
import Sugguestions from './suggestions'


class SearchForm extends React.Component {
    constructor() {
        super();
        this.state = {
        };
    }
    render(props) {
        {console.log('this.props',this.props.comments)}
        if (this.props.comments.length > 0) {
            return (
                <div>
                    <h2>Search Result For </h2>
                    <h3>Total Results: {this.props.comments.length}</h3>
                    <h3>Review: <span style={{color:this.props.review === 'Positive'?'Green':'Yellow'}}>{this.props.review}</span> </h3>
                
                    <Table id='result_table'>
                        <thead id="result_table_head">
                            <tr>
                                <th>Comment</th>
                                <th>Compound</th>
                                <th>Positive</th>
                                <th>Negative</th>
                                <th>Neutral</th>
                            </tr>
                        </thead>
                        <tbody>
                            {this.props.comments.map((row, index) => {
                                return (
                                    <tr key={index} className=" performance_row">
                                        <td className=" performance_col">{row.comment}</td>
                                        <td className=" performance_col">{row.compound}</td>
                                        <td className=" performance_col">{row.pos}</td>
                                        <td className=" performance_col">{row.neg}</td>
                                        <td className=" performance_col">{row.neu}</td>
                                    </tr>

                                )
                            }
                            )
                            }
                        </tbody>
                    </Table>
                </div>
            );
        } else
        return (
          <div>
    
            <h1>Please Make a Query Request</h1>
            <Sugguestions />
          </div>
        )
    }
  }
  
  export default SearchForm;