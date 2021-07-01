import { Box, makeStyles, Typography } from '@material-ui/core';
import React, { useState } from 'react';
import { Joystick } from 'react-joystick-component';
import useWebSocket from 'react-use-websocket';
import { JOYSTICK_WSS_URL } from '../const';
import KeyboardArrowLeftIcon from '@material-ui/icons/KeyboardArrowLeft';
import KeyboardArrowRightIcon from '@material-ui/icons/KeyboardArrowRight';
import KeyboardArrowUpIcon from '@material-ui/icons/KeyboardArrowUp';
import KeyboardArrowDownIcon from '@material-ui/icons/KeyboardArrowDown';

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    justifyContent: 'center',
    flexWrap: 'wrap',
    marginTop: theme.spacing(2)
  },
  fullWidthFlexItems: {
    flexBasis: '100%'
  },
  joystickContainer: {
    display: 'flex',
    flexWrap: 'nowrap',
    alignItems: 'center'
  },
  joystick: {
    margin: theme.spacing(6)
  },
  title: {
    marginTop: theme.spacing(3)
  }
}));

const JoystickController = () => {
  const [socketUrl] = useState(JOYSTICK_WSS_URL);
  const classes = useStyles();
  const {
    sendMessage
    // lastMessage,
    //  readyState
  } = useWebSocket(socketUrl);

  return (
    <div>
      <Typography variant="h5" className={classes.title}>
        Car movement joystick
      </Typography>
      <Box className={classes.root}>
        <KeyboardArrowUpIcon className={classes.fullWidthFlexItems} />

        <div className={classes.joystickContainer}>
          <KeyboardArrowLeftIcon />
          <div className={classes.joystick}>
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
          </div>
          <KeyboardArrowRightIcon />
        </div>
        <KeyboardArrowDownIcon className={classes.fullWidthFlexItems} />
      </Box>
    </div>
  );
};

export default JoystickController;
