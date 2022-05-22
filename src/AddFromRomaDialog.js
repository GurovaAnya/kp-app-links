import React, {useEffect, useState} from "react";
import {
    DialogContent,
    DialogTitle,
    TextField,
    Dialog,
    Button,
    Autocomplete
} from "@mui/material";
import "./styles.css"

const AddTextDialog = (props) => {
    const [ontId, setOntId] = useState(null);
    const [info, setInfo] = useState([]);

    useEffect(() => {
        let mounted = true;
        fetch('/api/document/get_all_onts').then(data => data.json()).then(doc => {
          if (mounted){
            setInfo(doc);
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
            .then(props.onClose)
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

                    <Autocomplete
                        sx={{ width: 500 }}
                        options={info.map((value) => {return {"label" : value.name, "id": value.id};})}
                        renderInput={(params) => <TextField {...params} label="Выбрать текст" />}
                        onChange={
                            (event, option) => setOntId(option?.id)}
                        isOptionEqualToValue={(option, value) => option.id === value.id}
                    >

                    </Autocomplete>
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