import React, { useEffect, useState } from 'react';

import JoystickController from '../components/JoystickController';
import CamFeed from '../components/CamFeed';
import CamSlider from '../components/CamSlider';

import { useHistory } from 'react-router';
import axios from 'axios';
import { API_URL } from '../const';
import { CircularProgress } from '@material-ui/core';

const Stream = () => {
  const [loading, setLoading] = useState(true);
  let history = useHistory();
  useEffect(() => {
    const key = localStorage.getItem('key');
    if (!key) history.push('/');
    else {
      axios
        .post(
          API_URL + 'auth/',
          { key },
          { headers: { 'Content-Type': 'application/json' } }
        )
        .then(() => {
          setTimeout(() => {
            setLoading(false);
          }, 1000);
        })
        .catch(() => {
          localStorage.removeItem('key');
          history.push('/');
        });
    }
    // eslint-disable-next-line
  }, []);
  return loading ? (
    <CircularProgress style={{ marginTop: 150 }} />
  ) : (
    <>
      <CamFeed />
      <CamSlider />
      <JoystickController />
    </>
  );
};

export default Stream;
