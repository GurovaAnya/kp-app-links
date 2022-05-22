import React, {useState} from "react";
import Input from "@mui/material/Input";
import Button from "@mui/material/Button";
import {Checkbox, FormControlLabel} from "@mui/material";

export const SideMenu = ({filter, restore}) => {
    const [classes, setClasses] = useState(".-1");
    const [showImplicit, setShowImplicit] = useState(true);
    const [show0, setShow0] = useState(true);
    const [show1, setShow1] = useState(true);
    const [show2, setShow2] = useState(true);
    const [showNone, setShowNone] = useState(true);

    return <div>
        <Input
            value={classes}
            onChange={(val) => setClasses(val.target.value)}
        />
        <Button onClick={() => filter(classes)}>Remove</Button>
        <Button onClick={() => restore(classes)}>Restore</Button>
        <StyleCheckbox
            styleId={".implicit"}
            show={showImplicit}
            setShow={setShowImplicit}
            restore={restore}
            filter={filter}
            label={"Показывать неявные ссылки"}
        />
        <StyleCheckbox
            styleId=".0"
            show={show0}
            setShow={setShow0}
            restore={restore}
            filter={filter}
            label={"А принят в соотвествии с Б"}
        />
        <StyleCheckbox
            styleId=".1"
            show={show1}
            setShow={setShow1}
            restore={restore}
            filter={filter}
            label={"А регулируется Б"}
        />
        <StyleCheckbox
            styleId=".2"
            show={show2}
            setShow={setShow2}
            restore={restore}
            filter={filter}
            label={"А вносит изменения в Б"}
        />
        <StyleCheckbox
            styleId=".none"
            show={showNone}
            setShow={setShowNone}
            restore={restore}
            filter={filter}
            label={"Не задано"}
        />
    </div>
}

const StyleCheckbox = ({styleId, show, setShow, restore, filter, label}) => {
    return (
        <div>
            <FormControlLabel
                value={label}
                label={label}
                control={
                    <Checkbox
                        value={show}
                        checked={show}
                        onChange={(event, checked) => {
                            if (checked)
                                restore(styleId);
                            else
                                filter(styleId);
                            setShow(checked);
                        }
                        }

                    />}
            />
        </div>
    );
}