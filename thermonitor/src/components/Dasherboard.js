import React from 'react'
import { Grid, Header, Image } from 'semantic-ui-react'
import building from '../building.png';
import deleteIcon from '../delete.png';
import modifyIcon from '../modify.png';
import inspectIcon from '../inspect.png';
import curvedlive from '../curvedline.png'
import './css/colGrid.css'
class Dasherboard extends React.Component{
    constructor(props){
        super(props);
    }
    componentDidMount(){
        document.body.style = 'background: royalblue';

    }

    render(){
        return <Grid style ={{width: '100%', backgroundColor: 'royalblue', cursor: 'pointer', position: 'absolute', top: '5rem'}}>
            <Grid.Row width={'100%'} style = {{marginTop: '2rem', left: '8%'}} >
                <Grid.Column width={6}  className={'dashboard-item'} >
                <Grid.Row>
                <Grid.Column width={16}>
                <div >
                <img  className={'dashboard-icon'} src={building}/>
                <h3 style = {{position: 'absolute', left: '35%', bottom: '1%'}}>Add</h3>
                </div>
                </Grid.Column>
                
                </Grid.Row>
                </Grid.Column>
                <Grid.Column width={6} className = {'dashboard-item'} >
                <div>
                <img className={'dashboard-icon'} src={deleteIcon}/>
                <h3 style = {{position: 'absolute', left: '29%', bottom: '1%'}}>Delete</h3>
                </div>
                </Grid.Column>
                </Grid.Row>
                <Grid.Row width={'100%'} style = {{marginTop: '2rem', left: '8%'}}>
                <Grid.Column width={6} className ={'dashboard-item'} >
                <div>
                <img className={'dashboard-icon'} src={modifyIcon}/>
                <h3 style = {{position: 'absolute', left: '30%', bottom: '1%'}}>Modify</h3>

                </div>
                </Grid.Column>
                <Grid.Column width={6} className ={'dashboard-item'} >
                <div>
                <img className={'dashboard-icon'} src={inspectIcon}/>
                <h3 style = {{position: 'absolute', left: '30%', bottom: '1%'}}>Inspect</h3>

                </div>
                </Grid.Column>
                </Grid.Row>
                <Grid.Row >
                    <Grid.Column width={16} style={{left: '10%'}}><h1 style={{color: 'white'}}>performance</h1></Grid.Column>
                    <Grid.Column width={16}>
                    <img  style = {{position: 'absolute', left: '13%', height: '100px', width: '77%'}} src={curvedlive}/>
                    </Grid.Column>
                </Grid.Row> 
        </Grid>
        
    }
}

export default Dasherboard;