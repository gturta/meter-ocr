import React from 'react'
import ImagePreviews from './image-previews'
import css from 'bootstrap/dist/css/bootstrap.min.css'


export default class TrainerInput extends React.Component{
    constructor(props){
        super(props)
        this.state = {images:[]}
    }
    render(){
        return(
            <div className="panel panel-default">
                <div className="panel-heading">
                    <h3 className="panel-title">Input selection</h3>
                </div>
                <div className="panel-body">
                    <div className="row">
                        <div className="col-sm-2">
                            <input type="file" id="add-files" style={{display:'none'}} multiple accept="image/*"
                                onChange={ event => this.setImages(event.target.files)}/>
                            <button className="btn btn-default" 
                                onClick={ (e) => {$("input#add-files").click(); e.preventDefault()}} >
                                <img src="/img/img-add.svg"/>
                            </button>
                        </div>
                        <div className="col-sm-10">
                            <ImagePreviews images={this.state.images}/>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-sm-12">
                            <input type="submit" id="submit" onClick={() => this.handleUpload()}/>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
    setImages(files){
        var items=[]
        for(var i=0; i<files.length; i++){
            var file = files[i];
            var imageType = /^image\//;
            if (!imageType.test(file.type)) {
                continue;
            }
            items.push(file)
        }
        this.setState({images:items})
    }
    handleUpload(){
        for (var i=0; i<this.state.images.length; i++){
            var file = this.state.images[i]
            this.uploadImage(file);
        }
        //clear images
        this.setState({images:[]})
    }

    uploadImage(file){
        var formData = new FormData()
        formData.append('file', file)
        $.ajax({
            url: this.props.uploadURL,
            type: "POST",
            //headers: {'Authorization':'Basic ' + btoa(AUTH_TOKEN+':'+'UNUSED')},
            contentType: false,
            processData: false,
            data: formData
        })
        .done(function(data){
            console.log("Image upload done: "+data)
        })
        .fail(function(xhr, status, errorThrown){
            console.log(status,errorThrown)
        });
    }
}
