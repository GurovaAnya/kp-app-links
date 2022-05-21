import React, {useEffect, useState} from "react";
import {DialogContent, DialogTitle, TextField, Dialog, Button, Select, InputLabel, FormControl} from "@mui/material";
import {MenuItem} from "@material-ui/core";
import "./styles.css"

const AddTextDialog = (props) => {
    const [ontId, setOntId] = useState(null);
    const [info, setInfo] = useState([]);

    useEffect(() => {
    let mounted = true;
    fetch('/api/document/get_all_onts').then(data => data.json()).then(doc => {
      if (mounted){
        setInfo(doc);
        setOntId(doc.next().id)
      }
    })
    return () => mounted = false;
  }, [])

    const handleSubmit = () => {
        fetch('/api/save_and_lem/' + ontId, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            }
        })
            .catch(error => alert(error))
            .then(r => props.onClose())
    }


    return (
        <Dialog
                open={props.isOpen}
                onClose={props.onClose}
                style={{display: 'flex', alignItems: 'center', justifyContent: 'center'}}
            >
            <DialogTitle>
                Выбрать документ
            </DialogTitle>
            <DialogContent>
                <FormControl
                    fullWidth
                    className="select-doc"
                >
                    <InputLabel>Выбрать</InputLabel>
                    <Select
                        label="Выбрать текст"
                        value={ontId}
                        onChange={(event) => setOntId(event.target.value)}
                    >
                        {info.map((value) => {
                            return (
                                <MenuItem value={value.id}>{value.name}</MenuItem>
                            )
                        })}
                    </Select>
                </FormControl>
                <Button
                    fullWidth variant="contained"
                    onClick={handleSubmit}
                >
                    Сохранить
                </Button>

            </DialogContent>
        </Dialog>

    );
}

export default AddTextDialog;