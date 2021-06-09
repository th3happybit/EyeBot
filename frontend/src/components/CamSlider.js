import { Box, Slider } from '@material-ui/core';
import React, { useState } from 'react';
import useWebSocket from 'react-use-websocket';

const CamSlider = () => {
  const [socketUrl] = useState('ws://3f7672ac3108.ngrok.io/joystick_ws');
  const {
    sendMessage
    // lastMessage,
    //  readyState
  } = useWebSocket(socketUrl);
  const [value, setValue] = useState(90);

  return (
    <Box mt={4}>
      <Slider
        style={{ width: '640px' }}
        getAriaValueText={() => value}
        aria-labelledby="discrete-slider-small-steps"
        step={15}
        marks
        min={0}
        max={180}
        value={value}
        onChange={(arg, newValue) => {
          setValue(newValue);
          sendMessage(newValue);
        }}
        valueLabelDisplay="auto"
      />
    </Box>
  );
};

export default CamSlider;
