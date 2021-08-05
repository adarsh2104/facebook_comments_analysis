import React from 'react';
import SearchForm from './components/search_form'
import './static/css/common.css';
class App extends React.Component {
  render() {
    return (
    <div>
      <h1><center>Facebook Comment Analyzer</center></h1>
      <SearchForm />
    </div>);
  }
}

export default App;
