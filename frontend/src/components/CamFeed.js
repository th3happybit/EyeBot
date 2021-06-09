import { Box } from '@material-ui/core';
import React from 'react';
import Iframe from 'react-iframe';

const CamFeed = () => {
  return (
    <Box m={2}>
      <Iframe
        url="http://www.youtube.com/embed/xDMP3i36naA"
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
