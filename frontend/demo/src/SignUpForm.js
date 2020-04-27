import React, { Component } from 'react';
import './SignUpForm.css';
import ReactDOM from 'react-dom';
import GoogleLogin from 'react-google-login';
import FacebookLogin from 'react-facebook-login';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';

import $ from 'jquery';

class SignUpForm extends Component {

  constructor(props) {
    super(props);
    this.state={
      name:'',
      email:'',
      password:'',
      re_password: '',
      message:''
    }
  }

  responseGoogle(googleUser) {
    let token = googleUser.getAuthResponse().id_token;
    this.oauthSignUp('google', token);
  }

  responseFacebook(facebookUser) {
    console.log(facebookUser);
    let token = facebookUser['accessToken'];
    this.oauthSignUp('facebook', token);
  } 

  signup() {
    let self = this;
    let params = {
      "name": this.state.name,
      "email": this.state.email,
      "password": this.state.password
    }

    // re-check password
    if (this.state.password != this.state.re_password) {
      let msg = 'please confirm password';
      console.log(msg);
      this.setState({'message': msg});
      return;
    }

    // register
    $.post('http://localhost:5000/register', params).then(function(res) {
      self.signup_success(res);
    });
  }

  login() {
    let self = this;
    let params = {
      "name": this.state.name,
      "password": this.state.password
    }

    // login
    $.post('http://localhost:5000/login', params).then(function(res) {
      self.login_success(res);
    });
  }

  signup_success(res) {
    console.log('Signup success: ' + JSON.stringify(res));
    this.setState({'message': JSON.stringify(res)});
  }

  login_success(res) {
    console.log('Login success: ' + JSON.stringify(res));
    this.setState({'message': JSON.stringify(res)});
  }

  oauthSignUp(provider, token) {
    let self = this;
    $.post('http://localhost:5000/oauth', {
      'provider': provider,
      'token': token
    }).then(function(res) {
      self.signup_success(res);
    });
  }

  render() {
    return (
      <div className="App">
        <div className="response-area">
          {this.state.message}
        </div>
        <GoogleLogin
          clientId="866829961158-20tfm86bf6tr1o38v0kao5kc40f1qbeb.apps.googleusercontent.com"
          buttonText="Sign Up With Google"
          onSuccess={(res) => this.responseGoogle(res)}
          onFailure={(res) => this.responseGoogle(res)}
        />

        <FacebookLogin
          appId="2953105441444557"
          autoLoad={false}
          fields="name,email,picture"
          callback={(res) => this.responseFacebook(res)} 
          textButton="Sign Up With Facebook"
          cssClass="login-form-item"
        />

        <MuiThemeProvider>
          <div>
            <TextField
              className="login-form-textfield"
              hintText="Name"
              onChange = {(event, name) => this.setState({name: name})}
              />
            <TextField
              type="email"
              className="login-form-textfield"
              hintText="Email"
              onChange = {(event, email) => this.setState({email: email})}
              />
            <TextField
              type="password"
              className="login-form-textfield"
              hintText="Password (at least 8 charactors)"
              onChange = {(event, password) => this.setState({password: password})}
              />
            <TextField
              type="password"
              className="login-form-textfield"
              hintText="Re-enter password"
              onChange = {(event, re_password) => this.setState({re_password: re_password})}
              />
            <RaisedButton 
              className="sign-up-button"
              label="Sign Up" 
              primary={true} 
              onClick={(event) => this.signup(event)}
              />
            <RaisedButton 
              className="sign-up-button"
              label="Login" 
              primary={true} 
              onClick={(event) => this.login(event)}
              />
          </div>
        </MuiThemeProvider>
      </div>
    );
  }
}

export default SignUpForm;
