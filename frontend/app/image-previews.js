import React from 'react'
import ReactDOM from 'react-dom'


class Preview extends React.Component {
    constructor(props){
        super(props)
        this.state = {image: null}
        this.getImage(props.file)
    }
    getImage(file){
        var reader = new FileReader();
        reader.onload = function(event){
            this.setState({image: event.target.result})
        }.bind(this)
        reader.readAsDataURL(file);
    }
    render(){
        return (
            <div className="col-sm-2">
                <img className="img-responsive" src={this.state.image} />
            </div>
        )
    }
}

export default class ImagePreviews extends React.Component {
    render(){
        var items = this.props.images.map(function(item,index){
            return(<Preview key={index} file={item}/>)
        })
        return(
            <div className="row">
                {items}
            </div>
        )
    }
}


