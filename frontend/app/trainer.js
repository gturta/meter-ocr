import React from 'react'
import ReactDOM from 'react-dom'
import 'bootstrap/dist/js/bootstrap'

import TrainerInput from './trainer-input'
import TrainerOutput from './trainer-output'

class Trainer extends React.Component{
    render(){
        return(
            <div className="trainer">{this.props.children}</div>
            )
    }
}

ReactDOM.render(
        <Trainer>
            <TrainerInput uploadURL="http://localhost:5555/image" />
            <TrainerOutput/>
        </Trainer>,
        document.getElementById('react-root')
        )
