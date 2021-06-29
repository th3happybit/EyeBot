import { Box, Grid } from '@material-ui/core';
import React, { useRef, useState } from 'react';
import { CAM_SERVER } from '../const';

const CamFeed = () => {
  const ref = useRef();
  const [height] = useState('600px');

  const onLoad = () => {
    // setHeight(ref.current.contentWindow.document.body.scrollHeight + 'px');
  };

  return (
    <Box m={2}>
      <Grid container>
        <Grid item xs={false} md={2} lg={3} />
        <Grid item xs={12} md={8} lg={6}>
          <iframe
            title="cam-feed-iframe"
            ref={ref}
            onLoad={onLoad}
            src={CAM_SERVER}
            width="100%"
            height={height + 'px'}
          />
        </Grid>
        <Grid item xs={false} md={2} lg={3} />
      </Grid>
    </Box>
  );
};

export default CamFeed;
