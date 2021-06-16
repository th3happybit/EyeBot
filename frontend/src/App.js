import './App.css';
import React from 'react';
import { Switch, Route, BrowserRouter as Router } from 'react-router-dom';
import Stream from './pages/stream';
import Login from './pages/login';

function App() {
  return (
    <div className="App">
      <Router>
        <Switch>
          <Route path="/stream" exact component={Stream} />
          <Route path="/" exact component={Login} />
        </Switch>
      </Router>
    </div>
  );
}

export default App;
