'use strict'

import React from 'react'
import ReactDOM from 'react-dom'
import css from "./less/styles.less";

import TrainerInput from './trainer-input'
import TrainerOutput from './trainer-output'

class Trainer extends React.Component{
    constructor(props){
        super(props)
        this.state={
            items:[]
        }
        this.addItem=this.addItem.bind(this)
    }
    render(){
        return(
            <div className="trainer">
                <TrainerInput uploadURL={this.props.dataURL} callback={this.addItem} />
                <TrainerOutput data={this.state.items} dataURL={this.props.dataURL} server={this.props.server} />
            </div>
        )
    }
    addItem(item){
        var items=this.state.items;
        items.push(item);
        this.setState({items:items});
    }
}

ReactDOM.render(
    <Trainer dataURL="http://localhost:5555/image" server="http://localhost:5555" />,
    document.getElementById('react-root')
)
