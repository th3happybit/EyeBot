import { Box } from '@material-ui/core';
import React from 'react';
import Iframe from 'react-iframe';
import { CAM_SERVER } from '../const';

const CamFeed = () => {
  return (
    <Box m={2}>
      <Iframe
        url={CAM_SERVER}
        width="640px"
        height="480px"
        id="myId"
        // className="myClassname"
        display="initial"
        position="relative"
      />
    </Box>
  );
};

export default CamFeed;
