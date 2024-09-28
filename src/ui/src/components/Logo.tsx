import { isMobile } from "react-device-detect";
import ironWatchersLogo from "../assets/iron-watchers-logo.png";
import React from "react";

interface LogoProps {
    className?: string;
}

const Logo: React.FC<LogoProps> = ({ className = "" }) => (
    <div className={className}>
        <img alt="Iron Watchers logo" className={isMobile ? "w-screen" : ""} src={ironWatchersLogo} />
    </div>
);

export default Logo;
