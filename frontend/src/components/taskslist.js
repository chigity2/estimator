import React from "react";
import axios from "axios";

export default class TaskList extends React.Component {
    state = {
        tasks: []
    }

    componentDidMount() {
        axios.get('http://192.168.1.74:8000/api/tasks')
          .then(res => {
              const tasks = res.data;
              this.setState({ tasks });
          })
    }

    render() {
        return(
        <ul>
            {
                this.state.tasks
                  .map(task =>
                    <li key={task.id}>{task.title}</li>
                  )
            }
            </ul>
        )
    }
}