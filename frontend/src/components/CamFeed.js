import { Box, Grid } from '@material-ui/core';
import React from 'react';
import Iframe from 'react-iframe';
import { CAM_SERVER } from '../const';

const CamFeed = () => {
  return (
    <Box m={2}>
      <Grid container>
        <Grid item xs={false} md={2} lg={3} />
        <Grid item xs={12} md={8} lg={6}>
          <Iframe
            url={CAM_SERVER}
            width="100%"
            height="500px"
            id="myId"
            // className="myClassname"
            display="initial"
            position="relative"
          />
        </Grid>
        <Grid item xs={false} md={2} lg={3} />
      </Grid>
    </Box>
  );
};

export default CamFeed;
