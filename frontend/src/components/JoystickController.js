import { Box } from '@material-ui/core';
import React, { useState } from 'react';
import { Joystick } from 'react-joystick-component';
import useWebSocket from 'react-use-websocket';
import { JOYSTICK_WSS_URL } from '../const';

const JoystickController = () => {
  const [socketUrl] = useState(JOYSTICK_WSS_URL);
  const {
    sendMessage
    // lastMessage,
    //  readyState
  } = useWebSocket(socketUrl);

  return (
    <div>
      <Box mt={8} style={{ display: 'flex', justifyContent: 'center' }}>
        <Joystick
          size={200}
          baseColor="#aaa"
          stickColor="#777"
          move={(arg) => {
            sendMessage(JSON.stringify(arg));
          }}
        />
      </Box>
    </div>
  );
};

export default JoystickController;
