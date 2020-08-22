import React, { Component } from 'react';
import store from './store';
import { getGeoJson } from './store/actionCreators';

class Filter extends Component {
  constructor(props) {
    super(props);
    this.state = {
      origin: '',
      destination: '',
      hour: '0'
    }

    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(e) {
    e.preventDefault();

    var url = new URL("http://test-env.eba-qeayktdb.us-west-2.elasticbeanstalk.com/api")
    // add get request parameters from this.state
    Object.keys(this.state).forEach((key, value) => { url.searchParams.append(key, this.state[key]) })

    // call redux action creator
    const action = getGeoJson(url);
    store.dispatch(action);
  }

  _getItems() {
    let items = [];         
    for (let i = 0; i < 24; i++) {             
        items.push(<option key={i} value={i}>{i}</option>);
    }
    return items;
  }

  render() {
    return (
      // html form with origin input, destination input, departure time selection, and submit button
      <form onSubmit={this.handleSubmit} id='filterForm'>
        <div className='form-group'>
          <label htmlFor="origin">Enter origin</label>
          <input id="origin" className='form-control form-control-sm' name="origin" type="text" value={this.state.origin} onChange={e => this.setState({origin: e.target.value})} />
          <small class="form-text text-muted">Origin must be in Philadelphia, PA</small>
        </div>

        <div className='form-group'>
          <label htmlFor="destination">Enter destination</label>
          <input id="destination" className='form-control form-control-sm' name="destination" type="text"  value={this.state.destination} onChange={e => this.setState({destination: e.target.value})} />
          <small class="form-text text-muted">Destination must be in Philadelphia, PA</small>
        </div>
        
        <div className='form-group'>
          <label htmlFor="hour">Enter departure time</label>
          <select id="hour" name="hour" className='form-control form-control-sm' onChange={e => this.setState({hour: e.target.value})}>
            {this._getItems()}
          </select>
        </div>

        <button type="submit" class="btn btn-outline-dark btn-sm">Submit</button>
      </form>
    );
  }
}

export default Filter;