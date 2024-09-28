import React from "react";
import { isMobile } from "react-device-detect";

import ControlBar from "./ControlBar";
import Logo from "./Logo";

interface HeaderProps {
    className?: string;
}

const desktopClassNames = "flex-row justify-between w-full";
const mobileClassNames = "flex-col";
const defaultClassName =
    " sticky top-0 flex border-solid border-slate-100 border-b-4 items-center " + (isMobile ? mobileClassNames : desktopClassNames);

const Header: React.FC<HeaderProps> = ({ className = "" }) => (
    <div className={className + defaultClassName} style={{ height: isMobile ? "" : "12vh" }}>
        <Logo />
        <ControlBar />
    </div>
);

export default Header;
