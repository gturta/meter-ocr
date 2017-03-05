import React from 'react'

class Digit extends React.Component{
    render(){
        return(
            <div className="result-output-digit">
                <div className="digit-img">
                    <img src={this.props.image} />
                </div>
                <div className="digit-ocr">
                    {this.props.digit}
                </div>
                <div className="digit-train-value">
                    <input type="text" placeholder="?" />
                </div>
                <div className="digit-train-submit">
                    <button />
                </div>
            </div>
        );
    }
}

class ProcessedImage extends React.Component{
    constructor(props){
        super(props);
        var digits=new Array(8);
        digits.fill("/img/img-placeholder.svg");
        this.state={
            img: "/img/img-placeholder.svg",
            band: "/img/img-placeholder.svg",
            image_digits: digits,
            identified_digits: new Array(8)
        };
        this.getProcessedData=this.getProcessedData.bind(this);
    }
    render(){
        var digits=[];
        for(var i=0; i<this.state.image_digits.length; i++){
            digits.push(<Digit key={i} 
                            image={this.state.image_digits[i]} 
                            digit={this.state.identified_digits[i]} />);
        }
        return(
            <div className="trainer-output-result">
                <div className="result-input">
                    <div className="result-input-name">
                        <h4>File: {this.props.file}</h4>
                    </div>
                    <div className="result-input-image">
                        <img src={this.state.img}/>
                    </div>
                    <div className="result-input-reload">
                        <button className="reload-button" onClick={this.getProcessedData}/>
                    </div>
                </div>
                <div className="result-output">
                    <div className="result-output-band">
                        <img src={this.state.band} />
                    </div>
                    <div className="result-output-digits">
                        {digits}
                    </div>
                </div>
            </div>
        )
    }
    componentDidMount(){
        this.getProcessedData();
    }

    getProcessedData(){
        $.ajax({
            url:this.props.dataURL+"/"+this.props.file,
            method:'GET'
        })
        .done(data=>{
            //expected: {
            //  img:<path_to_image>,
            //  band:<path_to_image>, 
            //  image_digits:[<path_to_image>, ...<path_to_image>],
            //  identified_digits:[d0,...d8]
            //}
            var processed=JSON.parse(data);
            var digits = processed.image_digits.map(d => {
                if(d.length > 0) return this.props.server+d
                else return "/img/img-placeholder.svg";
            });
            this.setState({
                img: this.props.server+processed.img,
                band: this.props.server+processed.band,
                image_digits: digits,
                identified_digits: processed.identified_digits
            });
        })
    }
}

export default class TrainerOutput extends React.Component{
    render(){
        var items = this.props.data.map( 
            (item,index) => <ProcessedImage key={index} file={item} dataURL={this.props.dataURL} server={this.props.server} />
        );
        return(
            <div className="output-panel">
                <div className="output-panel-heading">
                    <h3 className="output-panel-title">Results</h3>
                </div>
                <div className="output-panel-body">
                    {items}
                </div>
            </div>
        );
    }
}

