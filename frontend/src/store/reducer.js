import { UPDATE_GEOJSON } from "./actionTypes";

const defaultState = {
  geojson: {}
}

export default (state=defaultState, action) => {
  if (action.type === UPDATE_GEOJSON) {
    const newState = JSON.parse(JSON.stringify(state)); // make a deep copy
    newState.geojson = action.value;
    return newState;
  }

  return state;
}