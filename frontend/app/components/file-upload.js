"use strict"
import React from 'react'

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
            <div className="file-upload-preview">
                <div className="file-upload-image">
                    <img src={this.state.image} />
                </div>
            </div>
        )
    }
}

class FilePreviews extends React.Component {
    render(){
        var items = this.props.files.map(function(item,index){
            return(<Preview key={index} file={item}/>)
        })
        return(
            <div className="file-upload-previews">
                {items}
            </div>
        )
    }
}

//Props:
//  accept="image/*"
//  uploadURL
export default class FileUpload extends React.Component{
    constructor(props){
        super(props)
        this.state = {files:[]}
    }
    render(){
        return(
            <div className="file-upload">
                <div className="file-upload-select">
                    <div className="file-upload-input">
                        <input type="file" id="add-files" style={{display:'none'}} multiple accept={this.props.accept}
                            onChange={ event => this.setFiles(event.target.files)}/>
                        <button className="file-upload-button" 
                            onClick={ (e) => {$("input#add-files").click(); e.preventDefault()}} />
                    </div>
                    <FilePreviews files={this.state.files}/>
                </div>
                <div className="file-upload-submit">
                    <input type="submit" id="submit" onClick={() => this.handleUpload()}/>
                </div>
            </div>
        )
    }
    setFiles(files){
        var items=[]
        for(var i=0; i<files.length; i++){
            var file = files[i];
 //           var imageType = /^image\//;
 //           if (!imageType.test(file.type)) {
 //               continue;
 //           }
            items.push(file)
        }
        this.setState({files:items})
    }
    handleUpload(){
        for (var i=0; i<this.state.files.length; i++){
            var file = this.state.files[i]
            this.uploadFile(file);
        }
        //clear images
        this.setState({files:[]})
    }

    uploadFile(file){
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
        .done(data => this.props.callback(data))
        .fail(function(xhr, status, errorThrown){
            console.log(status,errorThrown)
        });
    }
}
