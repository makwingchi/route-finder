import { UPDATE_GEOJSON } from './actionTypes'


const updateGeoJson = (data) => ({
  type: UPDATE_GEOJSON,
  value: data
});

export const getGeoJson = (url) => {
  return (dispatch) => {
    fetch(url)
    .then(response => response.json())
    .then(data => {
      const action = updateGeoJson(data);
      dispatch(action);
    });
  }
}