import React, {useCallback, useState} from 'react'
import {useDropzone} from 'react-dropzone';
import '../../node_modules/react-dropzone/examples/theme.css'
import axios from 'axios'
import { Dimmer, Loader, Image, Segment } from 'semantic-ui-react'

function Basic(props) {
    const onDrop = useCallback(acceptedFiles => {
        console.log(acceptedFiles)
        var form = new FormData();
        form.append('file', acceptedFiles[0]);
        setDimmer(dimmerOn => true);
        axios.post('http://127.0.0.1:5000/upload', form, '').then((res)=>{
            console.log(res.data);
        document.getElementById("displayImage").setAttribute('visibility', 'visible')
        document.getElementById("displayImage").setAttribute("src", res.data.data);
        setDimmer(dimmerOn => false);
    });      
      }, [])

    const {acceptedFiles, getRootProps, getInputProps} = useDropzone({onDrop});
    const [dimmerOn, setDimmer] = useState(false);
      console.log(dimmerOn)
  
    return (
        <div>
        <Dimmer active = {dimmerOn}>
        <Loader />
        </Dimmer>
      <section className="container" >
       
        <div {...getRootProps({className: 'dropzone'})} >
          <input {...getInputProps()} />
          <p>Drag 'n' drop some files here, or click to select files</p>
        </div>
        <aside>
        </aside>
      </section>
     <img id="displayImage" style={{ position: 'absolute', left: '25%', top: '15%', width: '200px', height: '600px'}} ></img>
      </div>
    );
  }
  
  <Basic />
  
export {Basic};