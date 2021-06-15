import { Box, Grid, Slider } from '@material-ui/core';
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
    <Box mt={4} ml={4} mr={4}>
      <Grid container>
        <Grid item xs={false} md={2} lg={3} />
        <Grid item xs={12} md={8} lg={6}>
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
          />
        </Grid>
        <Grid item xs={false} md={2} lg={3} />
      </Grid>
    </Box>
  );
};

export default CamSlider;
