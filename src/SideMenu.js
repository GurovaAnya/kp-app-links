import React, {useState} from "react";
import {Box, Checkbox, FormControlLabel} from "@mui/material";
import filter from "cytoscape/src/collection/filter";

export const SideMenu = ({filter, restore}) => {
    const [showImplicit, setShowImplicit] = useState(true);
    const [show0, setShow0] = useState(true);
    const [show1, setShow1] = useState(true);
    const [show2, setShow2] = useState(true);
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

        <ExplicitCheckbox
            show0={show0}
            show1={show1}
            show2={show2}
            showNone={showNone}
            setShow0={setShow0}
            setShow1={setShow1}
            setShow2={setShow2}
            setShowNone={setShowNone}
            filter={filter}
            restore={restore}
            children={

            <Box sx={{ display: 'flex', flexDirection: 'column', ml: 3 }}>
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
                </Box>}/>
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

const ExplicitCheckbox = ({show0, setShow0, show1, setShow1, show2, setShow2, showNone, setShowNone, children, filter, restore}) => {

    const handleParentChange = (event) => {
        const checked = event.target.checked;
        handleChangeAndShow(show0, setShow0, filter, restore, ".0", checked);
        handleChangeAndShow(show1, setShow1, filter, restore, ".1", checked);
        handleChangeAndShow(show2, setShow2, filter, restore, ".2", checked);
        handleChangeAndShow(showNone, setShowNone, filter, restore, ".none", checked);

    }

    const handleChangeAndShow = (show, setShow, filter, restore, id, checked) => {
        if (show === checked)
            return;
        if (show)
            filter(id);
        else
            restore(id);
        setShow(checked);
    }

    return (
    <div>
        <FormControlLabel
            label="Показывать явные ссылки"
            control={
                <Checkbox
                    checked={show0 && show1 && show2 && showNone}
                    indeterminate={!(show0 && show1 && show2 && showNone) && (show0 || show1 || show2 || showNone)}
                    onChange={handleParentChange}
                />
            }
        />
        {children}
    </div>
    );
}