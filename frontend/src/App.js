import React, { Component } from 'react'
import RouteMap from './RouteMap';
import Filter from './Filter';

class App extends Component {
  render() {
    return (
      <React.Fragment>
        <Filter />
        <RouteMap />
      </React.Fragment>
    );
  }
}

export default App;