import React, {useState} from "react";
import {Autocomplete, TextField} from "@mui/material";
import {StyleCheckbox} from "./StyleCheckbox";
import {AllCheckboxes} from "./AllCheckboxes";

export const SideMenu = ({filter, restore, names, focusByName}) => {
    const [showImplicit, setShowImplicit] = useState(true);
    const [show0, setShow0] = useState(true);
    const [show1, setShow1] = useState(true);
    const [show2, setShow2] = useState(true);
    const [show3, setShow3] = useState(true)
    const [showNone, setShowNone] = useState(true);

    return <div>
        <StyleCheckbox
            styleId={".implicit"}
            show={showImplicit}
            setShow={setShowImplicit}
            restore={restore}
            filter={filter}
            label={"Показывать неявные ссылки"}
        />

        <AllCheckboxes show0={show0} show1={show1} show2={show2} show3={show3} showNone={showNone} show={setShow0}
                       show4={setShow1} show5={setShow2} show6={setShow3} showNone1={setShowNone} filter={filter}
                       restore={restore}/>

        <Autocomplete
            className={"side-menu-autocomplete"}
            sx={{width: 300}}
            options={names.map((value) => {
                return {"label": value.data.name, "id": value.data.id};
            })}
            renderInput={(params) => <TextField {...params} label="Выбрать закон"/>}
            onChange={
                (event, option) => focusByName(option?.id)}
            isOptionEqualToValue={(option, value) => option.id === value.id}
        >
        </Autocomplete>
    </div>
}

