import React, { Component } from 'react';
import { Map, TileLayer, Polyline} from 'react-leaflet'
import store from './store'


class RouteMap extends Component {

  constructor(props) {
    super(props);
    this.state = store.getState();

    this.handleStoreChange = this.handleStoreChange.bind(this);
    store.subscribe(this.handleStoreChange);
  }

  handleStoreChange() {
    // when redux store gets updated, component state will be updated as well
    this.setState(store.getState());
  }

  _swap(arr, index1, index2) {
    // swap two elements in an array.
    const temp = arr[index1];
    arr[index1] = arr[index2];
    arr[index2] = temp;
  }

  _geoJsonToMultiPolyline() {
    const geojson = this.state.geojson;
    
    const multiPolyline = [];
    
    // if geojson contains valid information, extract the multipolyline features
    if (geojson['features']) {
      for (let i = 0; i < geojson['features'].length; i++) {
        multiPolyline.push(geojson['features'][i]['geometry']['coordinates']);
      }
      
      for (let i = 0; i < multiPolyline.length; i++) {
        for (let j = 0; j < multiPolyline[i].length; j++) {
          this._swap(multiPolyline[i][j], 0, 1);
        }
      }
    }
    
    // otherwise return an empty array
    return multiPolyline;
  }

  _getCenter(multiPolyline) {
    // if input is undefined or the size of input array is 0, return a default output.
    if (multiPolyline === undefined || multiPolyline.length === 0) {
      return [39.95, -75.16];
    }

    var lat = 0, lng = 0, cnt = 0;

    for (let i = 0; i < multiPolyline.length; i++) {
      for (let j = 0; j < multiPolyline[i].length; j++) {
        lat += multiPolyline[i][j][0];
        lng += multiPolyline[i][j][1];
        cnt++;
      }
    }

    return [lat/cnt, lng/cnt - 0.03];
  }

  render() {
    const multiPolyline = this._geoJsonToMultiPolyline();
    const center = this._getCenter(multiPolyline);

    return (
      <Map center={ center } zoom={13} id='map'>
        <Polyline positions={ multiPolyline } color='red'></Polyline>
        <TileLayer
          url='http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png'
        />
      </Map>
    );
  }
}

export default RouteMap;