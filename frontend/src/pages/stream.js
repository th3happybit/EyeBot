import React, { useEffect, useState } from 'react';

import JoystickController from '../components/JoystickController';
import CamFeed from '../components/CamFeed';
import CamSlider from '../components/CamSlider';

import { useHistory } from 'react-router';
import axios from 'axios';
import { API_URL } from '../const';
import {
  Button,
  CircularProgress,
  Toolbar,
  Typography,
  AppBar,
  makeStyles,
  Grid,
  Card
} from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    flexDirection: 'column',
    flexWrap: 'nowrap',
    height: '100vh',
    minHeight: '600px'
  },
  container: {
    backgroundColor: '#eee',
    flexGrow: 1
  },
  menuButton: {
    marginRight: theme.spacing(2)
  },
  title: {
    flexGrow: 1
  },
  controllersContainer: {
    marginTop: theme.spacing(4),
    marginLeft: theme.spacing(4),
    marginRight: theme.spacing(4),
    borderRadius: '20px'
  },
  centerElements: {
    display: 'flex',
    justifyContent: 'center'
  },
  //  TODO: remove this styles later
  border: {
    // border: '5px solid red'
  },
  elementBorder: {
    // border: '5px solid green'
  }
}));

const Stream = () => {
  const [loading, setLoading] = useState(true);
  let history = useHistory();
  const classes = useStyles();
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
    <div className={classes.root}>
      <AppBar className={classes.border} position="static">
        <Toolbar>
          <img src="./logo.png" alt="logo" style={{ height: '50px' }} />
          <Typography variant="h6" className={classes.title}>
            Control panel
          </Typography>
          <Button
            color="inherit"
            onClick={() => {
              localStorage.clear();
              history.push('/');
            }}
          >
            Logout
          </Button>
        </Toolbar>
      </AppBar>
      <Grid container className={classes.container}>
        <Grid item xs={12} md={6} className={classes.border}>
          <Card className={classes.controllersContainer}>
            <CamFeed className={classes.border} />
          </Card>
        </Grid>
        <Grid item xs={12} md={6} className={classes.border}>
          <Card className={classes.controllersContainer}>
            <JoystickController className={classes.elementBorder} />
            <CamSlider className={classes.elementBorder} />
          </Card>
        </Grid>
      </Grid>
    </div>
  );
};

export default Stream;

{
  /* <CamFeed />
<JoystickController /> */
}
