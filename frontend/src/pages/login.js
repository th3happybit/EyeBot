import React, { useEffect, useState } from 'react';
import {
  Container,
  TextField,
  Box,
  CardContent,
  Card,
  Button,
  Typography,
  FormHelperText
} from '@material-ui/core';
import { API_URL } from '../const';
import axios from 'axios';
import { useHistory } from 'react-router-dom';

const Login = () => {
  const [key, setKey] = useState('');
  const [error, setError] = useState(null);

  const handleChangeKey = (e) => {
    let value = e.target.value;
    setKey(value);
    if (value === '') setError('The key is required');
    else setError('');
  };

  let history = useHistory();

  const handleLogin = async () => {
    if (key !== '')
      axios
        .post(
          API_URL + 'auth/',
          { key },
          {
            headers: {
              'Content-Type': 'application/json'
            }
          }
        )
        .then((res) => {
          localStorage.setItem('key', res.data.key);
          history.push('/stream');
        })
        .catch((err) => {
          setError(err.response.data.detail);
        });
    else setError('The key is required');
  };

  useEffect(() => {
    if (localStorage.getItem('key')) history.push('/stream');
    // eslint-disable-next-line
  }, []);

  return (
    <Container style={{ marginBottom: 100, marginTop: 100 }} maxWidth="sm">
      <Card>
        <CardContent className="">
          <Box
            alignItems="center"
            display="flex"
            justifyContent="space-between"
            mb={3}
          >
            <div style={{ textAlign: 'center', width: '100%' }}>
              <Typography color="textPrimary" gutterBottom variant="h4">
                Authenticate
              </Typography>
            </div>
          </Box>
          <Box flexGrow={1} mt={3}>
            <form>
              <TextField
                variant="outlined"
                label="KEY"
                margin="normal"
                fullWidth
                value={key}
                onChange={handleChangeKey}
              />
              {error && <FormHelperText error>{error}</FormHelperText>}
            </form>
            <Box mt={2}>
              <Button
                color="primary"
                fullWidth
                size="large"
                variant="contained"
                onClick={handleLogin}
              >
                Authenticate
              </Button>
            </Box>
          </Box>
        </CardContent>
      </Card>
    </Container>
  );
};

export default Login;
