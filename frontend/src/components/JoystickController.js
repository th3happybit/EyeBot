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
            sendMessage(
              JSON.stringify({ x: Math.ceil(arg.x), y: Math.ceil(arg.y) })
            );
          }}
          stop={() => {
            sendMessage(JSON.stringify({ x: '0', y: '0' }));
          }}
        />
      </Box>
    </div>
  );
};

export default JoystickController;
