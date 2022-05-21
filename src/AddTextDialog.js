import React, {useState} from "react";
import {DialogContent, DialogTitle, TextField, Dialog, Button} from "@mui/material";
import axios from "axios";
import {Input} from "@material-ui/core";

const AddTextDialog = (props) => {
    const [text, setText] = useState("");
    const [file, setFile] = useState(File.prototype);

    const handleSubmit = () => {
        fetch('/api/ont_from_text', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text
            })
        })
            .catch(error => alert(error))
            .then(r => props.onClose())
    }

    const handleDocumentLoad = (e) => {
        const formData = new FormData();
        console.log(file);

		// formData.append('file', e.target.files[0]);
        formData.append('file', file);
        const config = {
            headers: {
                'Accept': '*/*',
                'Content-Type': 'multipart/form-data',
            }
        }
        axios.post("/api/save_file", formData,config)
                    .then(r => props.onClose());
    }

    return (
        <Dialog
                open={props.isOpen}
                onClose={props.onClose}
                style={{display: 'flex', alignItems: 'center', justifyContent: 'center'}}
            >
            <DialogTitle>
                Добавить онтологию
            </DialogTitle>
            <DialogContent>
                <TextField
                    variant="outlined"
                    margin="normal"
                    required
                    fullWidth
                    multiline
                    name="text"
                    // label="Онтология в формате owl"
                    id="text"
                    value={text}

                    onChange={(event) => setText(event.target.value)}
                />

                {/*<input*/}
                {/*    id="input_owl"*/}
                {/*            accept=".owl"*/}
                {/*            style={{ display: 'none' }}*/}
                {/*            type="file"*/}
                {/*            // name="file"*/}
                {/*            // hidden*/}
                {/*            onChange={(e) => setFile(e.target.files[0])}*/}
                {/*        />*/}

                {/*<label htmlFor="input_owl">*/}
                    <Input accept=".owl"
                           id="input_owl"
                           type="file"
                           onChange={(e) => setFile(e.target.files[0])}/>
                    {/*<Button htmlFor="input_owl" component="span">*/}
                    {/*    Загрузить документ из файла*/}
                    {/*</Button>*/}
                {/*</label>*/}


                <Button
                    fullWidth variant="contained"
                    onClick={handleDocumentLoad}
                >
                    Сохранить
                </Button>

            </DialogContent>
        </Dialog>

    );
}

export default AddTextDialog;