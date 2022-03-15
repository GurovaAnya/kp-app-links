import React from "react";
import {DialogContent, DialogTitle, TextField} from "@mui/material";
import Button from "@mui/material/Button";

const AddTextDialog = () => (

    <>
        <DialogTitle>
            Добавить текст законодательного акта
        </DialogTitle>
        <DialogContent>
            <form noValidate>

                <TextField
                    variant="outlined"
                    margin="normal"
                    required
                    fullWidth
                    id="full_text"
                    label="Полное название законодательного акта"
                    name="full_text"
                    autoFocus
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
                />


                <Button type="submit"
                        fullWidth variant="contained"
                        color="primary">
                    Sign In
                </Button>

            </form>
        </DialogContent>
    </>

);

export default AddTextDialog;