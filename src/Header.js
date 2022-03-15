import React, {useState} from "react";

import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from '@mui/material/Typography';
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import Button from "@mui/material/Button";
import AddIcon from '@mui/icons-material/Add';
import {
    Dialog,
} from "@mui/material";
import AddTextDialog from "./AddTextDialog";


export default function Header() {

    const [isAddModalShown, setAddModalShown] = useState(false);

    return (
        <AppBar position="static">
            <Toolbar>
                <IconButton
                    size="large"
                    edge="start"
                    color="inherit"
                    aria-label="menu"
                    sx={{mr: 2}}
                >
                    <MenuIcon/>
                </IconButton>

                <Typography
                    variant="h6"
                    component="div"
                    sx={{flexGrow: 1}}
                >
                    Модуль идентификации связей документов
                </Typography>

                <Button color="inherit">Главная</Button>
                <AddIcon
                    size="large"
                    edge="start"
                    color="inherit"
                    sx={{mr: 2}}
                    onClick={() => setAddModalShown(true)}
                />
            </Toolbar>

            <Dialog
                open={isAddModalShown}
                onClose={() => setAddModalShown(false)}
                style={{display: 'flex', alignItems: 'center', justifyContent: 'center'}}
            >
                <AddTextDialog/>
            </Dialog>
        </AppBar>
    );
}