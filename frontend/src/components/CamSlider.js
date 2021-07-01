import { Box, Slider, Typography } from '@material-ui/core';
import React, { useState } from 'react';
import useWebSocket from 'react-use-websocket';
import { CAM_WSS_URL } from '../const';

const CamSlider = () => {
  const [socketUrl] = useState(CAM_WSS_URL);
  const {
    sendMessage
    // lastMessage,
    //  readyState
  } = useWebSocket(socketUrl);
  const [value, setValue] = useState(90);

  return (
    <Box mt={6} ml={6} mr={6} mb={6}>
      <Typography variant="h5">Cam controller</Typography>
      <Slider
        style={{ width: '100%' }}
        getAriaValueText={() => value}
        aria-labelledby="discrete-slider-small-steps"
        step={15}
        marks
        min={0}
        max={180}
        value={value}
        onChangeCommitted={(arg, newValue) => {
          setValue(newValue);
          sendMessage(180 - newValue);
        }}
        onChange={(arg, newValue) => {
          setValue(newValue);
          if (newValue !== value) {
            setValue(newValue);
          }
        }}
        valueLabelDisplay="auto"
        valueLabelFormat={(value) => <>{value} °</>}
      />
    </Box>
  );
};

export default CamSlider;
