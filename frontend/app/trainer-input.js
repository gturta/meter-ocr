import React from 'react'
import FileUpload from './components/file-upload'


export default class TrainerInput extends React.Component{
    constructor(props){
        super(props)
        this.state = {images:[]}
    }
    render(){
        return(
            <div className="input-panel">
                <div className="input-panel-heading">
                    <h3 className="input-panel-title">Input selection</h3>
                </div>
                <div className="input-panel-body">
                    <FileUpload accept="image/*" uploadURL={this.props.uploadURL} 
                        callback={this.props.callback} />
                </div>
            </div>
        )
    }
}
