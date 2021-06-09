import { Box } from '@material-ui/core';
import React, { useState } from 'react';
import { Joystick } from 'react-joystick-component';
import useWebSocket from 'react-use-websocket';

const JoystickController = () => {
  const [socketUrl] = useState('ws://3f7672ac3108.ngrok.io/joystick_ws');
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
        ></Joystick>
      </Box>
    </div>
  );
};

export default JoystickController;
