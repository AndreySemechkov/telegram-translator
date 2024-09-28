import { isMobile } from "react-device-detect";
import React, { useContext } from "react";

import { MainAppContext } from "../context/MainAppContext";
import LabeledSwitch from "./LabeledSwitch";
import LanguageFilters from "./LanguageFilters";
import SearchInput from "./Search";

const desktopClassNames = "flex-row justify-end gap-5 pr-5";
const mobileClassNames = "flex-col gap-2 pb-1";
const className = "flex w-full h-full items-center " + (isMobile ? mobileClassNames : desktopClassNames);

const ControlBar: React.FC = () => {
    const { showMedia, setShowMedia } = useContext(MainAppContext);

    return (
        <div className={className}>
            <div
                className={
                    "flex flex-row w-full gap-5 h-full items-center " + (isMobile ? "justify-center" : "justify-end")
                }
            >
                <LabeledSwitch
                    label={isMobile ? "Media" : "Show Media"}
                    checked={showMedia}
                    onChange={() => setShowMedia((showMedia) => !showMedia)}
                />
                <LanguageFilters />
            </div>
            <SearchInput />
        </div>
    );
};

export default ControlBar;
