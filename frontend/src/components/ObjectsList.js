import {SvgIcon, Typography} from '@material-ui/core';
import {Chip, makeStyles} from '@material-ui/core';
import React, {useState} from 'react';
import NotInterestedIcon from '@material-ui/icons/NotInterested';
import {OBJECTS_WSS_URL} from '../const';
import useWebSocket from 'react-use-websocket';

const useStyles = makeStyles((theme) => ({
    chip: {
        marginLeft: theme.spacing(3),
        marginTop: theme.spacing(2),
        marginBottom: theme.spacing(2)
    },
    text: {
        marginTop: theme.spacing(2)
    },
    emptyBox: {
        display: 'flex',
        justifyContent: 'center',
        marginTop: theme.spacing(4),
        marginBottom: theme.spacing(4)
    },
    emptyText: {
        marginRight: theme.spacing(1),
        marginLeft: theme.spacing(1)
    }
}));

const ObjectsList = () => {
    const classes = useStyles();
    const [data, setData] = useState([]);
    useWebSocket(OBJECTS_WSS_URL, {
        onMessage: (event) => {
            const lastJsonMessage = JSON.parse(event.data);
            console.log(lastJsonMessage);
            if (lastJsonMessage && data.indexOf(lastJsonMessage.name) == -1) {
                setData([
                    ...data,
                    lastJsonMessage.name
                ]);
            }
        }
    });

    return (
        <div>
            <Typography variant="h5"
                className={
                    classes.text
            }>
                Detected objects
            </Typography>
            {
            !data || data.length == 0 ? (
                <div className={
                    classes.emptyBox
                }>
                    <SvgIcon className={
                        classes.emptyText
                    }>
                        <NotInterestedIcon/>
                    </SvgIcon>
                    <Typography variant="h5" component="h2"
                        className={
                            classes.emptyText
                    }>
                        No object detected
                    </Typography>
                </div>
            ) : (data.map((item) => (
                <Chip key={item}
                    label={item}
                    onDelete={
                        () => {
                            setData([...data.filter((it) => item != it)]);
                        }
                    }
                    className={
                        classes.chip
                    }/>
            )))
        } </div>
    );
};

export default ObjectsList;
