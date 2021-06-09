import './App.css';
import React from 'react';
import JoystickController from './components/JoystickController';
import CamFeed from './components/CamFeed';
import CamSlider from './components/CamSlider';

function App() {
  return (
    <div className="App">
      <CamFeed />
      <CamSlider />
      <JoystickController />
    </div>
  );
}

export default App;
