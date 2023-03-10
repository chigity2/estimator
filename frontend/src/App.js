import React, { Component } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import TaskList from "./components/taskslist";
import BasicExample from "./components/navbar";



class App extends Component {
  render() {
    return (
     <div className="App">
       <BasicExample/>
       <TaskList/>
     </div>
    )
    }
  }
export default App;
