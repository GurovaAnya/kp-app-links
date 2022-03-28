import React, {useState} from "react";
import {DialogContent, DialogTitle, TextField, Dialog, Button} from "@mui/material";

const AddTextDialog = (props) => {
    const [title, setTitle] = useState("");
    const [text, setText] = useState("");

    const handleSubmit = () => {
        fetch('/api/save_and_lem', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                full_name: title,
                text: text
            })
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
                Добавить текст законодательного акта
            </DialogTitle>

            <DialogContent>
                <TextField
                    variant="outlined"
                    margin="normal"
                    required
                    fullWidth
                    id="full_text"
                    label="Полное название законодательного акта"
                    name="full_text"
                    autoFocus
                    value={title}
                    onChange={(event) => setTitle(event.target.value)}
                />

                <TextField
                    variant="outlined"
                    margin="normal"
                    required
                    fullWidth
                    multiline
                    name="text"
                    label="Текст законодательного акта"
                    id="text"
                    value={text}
                    onChange={(event) => setText(event.target.value)}
                />


                <Button
                    fullWidth variant="contained"
                    onClick={handleSubmit}
                    sx={{backgroundColor: "#00d2ca"}}
                >
                    Сохранить
                </Button>

            </DialogContent>
        </Dialog>

    );
}

export default AddTextDialog;