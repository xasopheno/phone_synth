import React, { Component } from 'react';
import ip from '../Server/ip.json';

class Main extends Component {
  constructor(props){
    super(props);
    this.state = {
      open: false,
      data: null,
    };

    this.socket = new WebSocket(`ws://${this.readTextFile()}:5678/`);
  }

  componentWillMount() {
    this.readTextFile()
  }

  readTextFile() {
    return ip.ip
  }


  componentDidMount() {
    this.socket.onopen = () => this.socket.send(JSON.stringify({type: 'greet', payload: 'Hello Mr. Server!'}));
    this.socket.onmessage = ({data}) => this.processData(data);
  }

  processData(data) {
    this.setState({
      ...this.state,
      data: data
    })
  }


  render() {
    return (
      <div className="App">
        <h2>| Phone Synth |</h2>
        <h2 style={styles.random}>{this.state.data}</h2>
      </div>
    );
  }
}

const styles = {
  random: {
    overflowWrap: 'break-word',
    textAlign: 'center',
    color: 'green',
  }
};

export default Main;