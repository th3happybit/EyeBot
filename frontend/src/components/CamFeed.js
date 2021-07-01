import { Box } from '@material-ui/core';
import React, { useEffect, useState } from 'react';
import { CAM_SERVER, IFRAME_RATIO } from '../const';
import useIframeContentHeight from '../utils/useIframeContentHeight';

const CamFeed = () => {
  const [
    iframeRef
    // iframeHeight
  ] = useIframeContentHeight();

  const [height, setHeight] = useState(IFRAME_RATIO.height);

  const resetheight = () => {
    let windowWidth = document.getElementById('cam-feed-iframe').clientWidth;
    setHeight((IFRAME_RATIO.height * windowWidth) / IFRAME_RATIO.width);
  };

  useEffect(() => {
    window.addEventListener('resize', resetheight);

    return () => {
      window.removeEventListener('resize', resetheight);
    };
  });

  return (
    <Box>
      <iframe
        ref={iframeRef}
        // height={iframeHeight}
        height={height}
        width="100%"
        onLoad={resetheight}
        src={CAM_SERVER}
        id="cam-feed-iframe"
        title="cam-feed-iframe"
        frameBorder="0"
        allowFullScreen
      />
    </Box>
  );
};

export default CamFeed;
